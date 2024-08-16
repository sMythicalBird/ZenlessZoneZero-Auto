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


def bi_bfs(
    matrix: List[List[MapComponent]], start: list[int], goal: list[int]
) -> List[Tuple[MapComponent, Dirct]]:
    # 因为需要记录最短路径及其移动方向，因此分两步
    # 如何解决传送带的问题，有向图搜索很难记录路径
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
        # 队列不为空
        while cur_size > 0:
            cur_size -= 1
            (x, y) = q.get()
            neighbours = queue.Queue()
            neighbours.put((x - 1, y))
            neighbours.put((x, y - 1))
            neighbours.put((x + 1, y))
            neighbours.put((x, y + 1))
            while not neighbours.empty():
                (x_n, y_n) = neighbours.get()
                if 0 <= y_n < cols and rows > x_n >= 0:
                    if matrix[x_n][y_n].tp_id == 0:  # 非传送带不可重复访问
                        if visited[x_n][y_n] != 0:  # 已访问
                            continue
                        visited[x_n][y_n] = step
                        q.put((x_n, y_n))
                    else:
                        # 将传送带的下一个格子送到相邻队列中
                        a, b = x_n, y_n
                        if matrix[x_n][y_n].tp_id == 1:
                            b -= 1
                        elif matrix[x_n][y_n].tp_id == 2:
                            a -= 1
                        elif matrix[x_n][y_n].tp_id == 3:
                            b += 1
                        elif matrix[x_n][y_n].tp_id == 4:
                            a += 1
                        if a == x and b == y:  # 若传送带指向自己则继续感染，否则跳过
                            visited[x_n][y_n] = step
                            proper_pos = [
                                (x_n - 1, y_n),
                                (x_n + 1, y_n),
                                (x_n, y_n - 1),
                                (x_n, y_n + 1),
                            ]
                            for x_n, y_n in proper_pos:
                                if x_n == x and y_n == y:
                                    continue
                                neighbours.put((x_n, y_n))
    # 一步一搜，因此不再需要全路径，每次返回下一步结果即可
    # 2、起点处获取下一步结果
    (x, y) = start
    step = visited[x][y]
    neighbours = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
    for x_n, y_n in neighbours:
        if 0 <= x_n < rows and 0 <= y_n < cols:
            # 找到下一步
            # 缩短距离或遇到传送带
            if (visited[x_n][y_n] == step - 1) or (
                visited[x_n][y_n] == step and matrix[x_n][y_n].tp_id != 0
            ):
                direction = Dirct.up
                if x_n > x:
                    direction = Dirct.down
                elif y_n < y:
                    direction = Dirct.left
                elif y_n > y:
                    direction = Dirct.right
                return [
                    (matrix[x_n][y_n], direction),
                    step,
                ]  # 返回下一个格子信息、移动方向、最大移动距离
    return []  # 找不到路径


def auto_find_way(components: MapInfo | List[List[MapComponent]]):
    # 寻路中所有二位矩阵索引均以线性代数为准
    # 检查输入值是否为MapInfo，取出组件矩阵
    if isinstance(components, MapInfo):
        components: List[List[MapComponent]] = components.components
    # 找到起点
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
    # 按照权重倒序排序
    components_list = sorted(
        components_list, key=lambda component: component.weight, reverse=True
    )
    # 按照权重进行分组
    components_group = groupby(components_list, key=lambda component: component.weight)
    # 遍历分组寻路
    for key, group in components_group:
        group: List[MapComponent] = list(group)
        # 遍历每个分组 暂存结果
        results = []
        for target in group:
            target: MapComponent
            target_position = [target.y, target.x]
            result = bi_bfs(components, start, target_position)
            if result:
                results.append(result)
        # 按照最大搜索步数排序
        results = sorted(results, key=lambda res: res[1])
        if results:
            # 返回下一个格子信息和移动方向
            return results[0][0]
