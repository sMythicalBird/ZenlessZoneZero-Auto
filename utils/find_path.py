# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: find_path.py
@time: 2024/6/25 下午8:46
@author SuperLazyDog
"""
import heapq

import numpy as np


def heuristic(a: tuple, b: tuple):
    """
    曼哈顿距离启发式
    :param a: 位置a
    :param b: 位置b
    :return: 位置a到位置b的曼哈顿距离
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from: dict, current: tuple, shape: tuple):
    """
    重建从起点到目标的路径
    :param came_from: 保存路径的字典
    :param current: 当前位置
    :param shape: 地图的形状
    :return: 从起点到目标的路径
    """
    path = np.zeros(shape, dtype=int)
    while current in came_from:
        path[current[0], current[1]] = 1
        current = came_from[current]
    path[current[0], current[1]] = 1
    return path


def a_star_search(map_matrix: np.ndarray, start: tuple, goal: tuple) -> dict | None:
    """
    使用A*算法寻找从起点到终点的最短路径。

    :param map_matrix: 二维numpy数组，表示地图，0表示可通行，1表示障碍。
    :param start: 起点的坐标，一个元组。
    :param goal: 终点的坐标，一个元组。
    :return: 如果找到路径，返回从起点到终点的路径记录，否则返回None。
    """
    # 获取地图的行数和列数
    rows, cols = map_matrix.shape
    # 初始化开放列表，用于存储待探索的节点
    open_set = []
    # 将起点加入开放列表，并计算其启发式值
    heapq.heappush(
        open_set, (0 + heuristic(start, goal), 0, start)
    )  # f_score, g_score, position
    # 初始化从起点到各节点的路径记录
    came_from = {}
    # 初始化从起点到各节点的实际代价
    g_score = {start: 0}
    # 初始化从起点到各节点的总代价（实际代价+启发式代价）
    f_score = {start: heuristic(start, goal)}
    # 当开放列表不为空时，继续搜索
    while open_set:
        # 从开放列表中取出代价最小的节点
        _, current_g, current = heapq.heappop(open_set)
        # 如果当前节点是终点，则重构路径并返回
        if current == goal:
            return came_from
        # 遍历当前节点的四个邻居
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)  # 计算邻居节点的坐标
            # 如果邻居节点在地图范围内且不是障碍
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if map_matrix[neighbor[0], neighbor[1]] == 1:
                    continue
                # 计算到达邻居节点的代价
                tentative_g_score = current_g + 1
                # 如果通过当前节点到达邻居节点的代价更小，则更新邻居节点的信息
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(
                        open_set, (f_score[neighbor], tentative_g_score, neighbor)
                    )
    # 如果没有找到路径，则返回None
    return None


class AStarSearch:
    def __init__(self, map_matrix: np.ndarray, start: tuple, goal: tuple):
        self.map_matrix = map_matrix
        self.goal = goal
        self.came_from = a_star_search(map_matrix, start, goal)

    def next_step(self, current) -> tuple | None:
        """
        获取到达目标位置的下一步
        :param current: 当前位置
        :return:
        """
        for key, value in self.came_from.items():
            if value == current:
                return key
        self.came_from = a_star_search(self.map_matrix, current, self.goal)
        if not self.came_from:
            return None
        for key, value in self.came_from.items():
            if value == current:
                return key
        return None

    def get_path(self) -> np.ndarray | None:
        """
        获取从起点到目标的路径
        :return: 从起点到目标的路径
        """
        if not self.came_from:  # 如果没有找到路径，则返回None
            return None
        return reconstruct_path(self.came_from, self.goal, self.map_matrix.shape)

    def __iter__(self):
        return self.came_from

    def __next__(self):
        return self.came_from


if __name__ == "__main__":
    map_matrix = np.array(
        [
            [0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
    )
    start = (0, 0)
    goal = (6, 6)
    path = AStarSearch(map_matrix, start, goal).get_path()
    if path is not None:
        print(path)
    else:
        print("No path found.")
