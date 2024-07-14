# -*- coding: utf-8 -*-
"""
@file: autofindway.py
@time: 2024/7/9
@auther: sMythicalBird
"""
import queue
from typing import List, Tuple

import numpy as np

from schema import MapComponent, MapInfo


def bi_bfs(
    matrix: List[List[MapComponent]], start: list[int], goal: list[int]
) -> List[Tuple[MapComponent, str]]:
    # 因为需要记录最短路径及其移动方向，因此分两步
    # 1、终点bfs找全图最短路径
    rows, cols = len(matrix), len(matrix[0])
    visited = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j].obstacle:
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
    res: List[Tuple[MapComponent, str]] = []
    (x, y) = start
    step = visited[x][y]
    while step > 0:
        step -= 1
        neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for x_n, y_n in neighbours:
            if 0 <= x_n < rows and 0 <= y_n < cols and visited[x_n][y_n] == step:
                direction = "w"
                if x_n > x:
                    direction = "s"
                elif y_n < y:
                    direction = "a"
                elif y_n > y:
                    direction = "d"
                res.append((matrix[x_n][y_n], direction))
                x, y = x_n, y_n
                break
    return res


# 自动寻路


def auto_find_way(components: MapInfo | List[List[MapComponent]]):
    if isinstance(components, MapInfo):
        components: List[List[MapComponent]] = components.components
    # 找到起点和终点
    start: list[int] = [-1, -1]
    for i in range(len(components)):
        for j in range(len(components[i])):
            if components[i][j].name == "自身位置":
                start = [i, j]
    target: list[int] = [-1, -1]
    for i in range(len(components)):
        for j in range(len(components[i])):
            if components[i][j].name == "目标位置":
                target = [i, j]
    return bi_bfs(components, start, target)
