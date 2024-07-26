# -*- coding: utf-8 -*-
"""
@file: autofindway.py
@time: 2024/7/9
@auther: sMythicalBird
"""
import queue
from typing import List, Tuple
from itertools import groupby

import numpy as np
from schema.info import Dirct
from schema import MapComponent, MapInfo
from utils import logger


def bi_bfs(
    matrix: List[List[MapComponent]], start: list[int], goal: list[int]
) -> List[Tuple[MapComponent, Dirct]]:
    # 因为需要记录最短路径及其移动方向，因此分两步
    # 1、终点bfs找全图最短路径,终点找出能来的所有点
    rows, cols = len(matrix), len(matrix[0])
    visited = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j].weight == 0:
                visited[i][j] = -1
    q = queue.Queue()
    q.put(goal)
    step = 1  # 记录步数
    visited[goal[0]][goal[1]] = step
    while not q.empty():
        cur_size = q.qsize()
        step += 1
        while cur_size > 0:
            cur_size -= 1
            (x, y) = q.get()
            neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for x_n, y_n in neighbours:
                if 0 <= y_n < cols and rows > x_n >= 0 == visited[x_n][y_n]:
                    visited[x_n][y_n] = step
                    q.put((x_n, y_n))
    # 2、起点bfs找终点
    # 方向使用wasd表示
    # 返回列表第一个值为事件标签，第二个值为方向
    res: List[Tuple[MapComponent, Dirct]] = []
    (x, y) = start
    step = visited[x][y]
    while step > 0:
        step -= 1
        neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for x_n, y_n in neighbours:
            if 0 <= x_n < rows and 0 <= y_n < cols and visited[x_n][y_n] == step:
                direction = Dirct.up
                if x_n > x:
                    direction = Dirct.down
                elif y_n < y:
                    direction = Dirct.left
                elif y_n > y:
                    direction = Dirct.right
                res.append((matrix[x_n][y_n], direction))
                x, y = x_n, y_n
                break
    return res


# 自动寻路


def auto_find_way(components: MapInfo | List[List[MapComponent]]):
    if isinstance(components, MapInfo):
        components: List[List[MapComponent]] = components.components
    # 找到起点
    # logger.debug(f"地图信息: {components}")
    start: list[int] = [-1, -1]
    for i in range(len(components)):
        for j in range(len(components[i])):
            # 如果权重为-1，则为起点
            if components[i][j].weight == -1:
                start = [i, j]
    # 打平components
    components_list: List[MapComponent] = [
        component for line in components for component in line if component.weight > 0
    ]
    # 按照权重进行分组
    components_group = groupby(components_list, key=lambda component: component.weight)
    components_group = [
        (key, [item for item in group]) for key, group in components_group
    ]
    # 排序 倒序
    components_group = sorted(components_group, key=lambda item: item[0], reverse=True)
    # logger.debug(f"分组信息: {components_group}")
    # 遍历分组
    for key, group in components_group:
        group: List[MapComponent] = list(group)
        # 遍历每个分组 暂存结果
        results = []
        # logger.debug(f"当前分组: {key}, 组内信息: {group}")
        for target in group:
            # logger.debug(f"当前目标: {target}")
            target: MapComponent
            target_position = [target.y, target.x]
            result = bi_bfs(components, start, target_position)
            # logger.debug(f"目标位置: {target_position}, 路径: {result}")
            if result:
                results.append(result)
        # 按照路径长度排序
        results = sorted(results, key=lambda x: len(x))
        if results:
            # logger.debug(f"找到目的地: {results[-1]}")
            # 返回最短路径
            return results[0]
