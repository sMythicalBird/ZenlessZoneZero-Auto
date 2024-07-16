# -*- coding: utf-8 -*-
""" 
@file:      others.py
@time:      2024/7/10 上午2:38
@author:    sMythicalBird
"""

import time
from datetime import datetime
from typing import Dict

import numpy as np
from pydirectinput import press
from schema import MapInfo, Position, info, sec_info, MapComponent
from utils import control, get_map_info, auto_find_way, config, logger
from utils.task import task
from utils.detect.current import find_current

map_name = config.targetMap.Zone
map_level = config.targetMap.Level
logger.debug(f"地图名称: {map_name}, 地图等级: {map_level}")


# 进入地图读取信息
@task.page(name="地图层数", priority=0, target_texts=["背包", "^当前层数"])
def grid_map_1(screen: np.ndarray):
    # 判断是否在进入事件对话，检查是否可以找到自身位置
    k = find_current()
    if not k:
        control.click(1000, 350)
        time.sleep(1)
        return
    map_info = get_map_info(screen)
    if not map_info:
        logger.debug("未识别到地图信息")
        return
    mapWay = auto_find_way(map_info)
    if not mapWay:
        logger.debug("未找到路径")
        return
    (mc, dirct) = mapWay[0]
    press(str(dirct), duration=0.1)
    info.lastDirct = dirct
    # 进战斗时需要计时，未防止战斗多次重置时间，不写在战斗函数中
    info.lastMoveTime = datetime.now()

@task.page(name="选择角色", target_texts=["出战"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("出战")
    control.click(pos.x, pos.y)
    info.entryMapTime = datetime.now() # 进入地图时间
    # 等待加载进入动画，这个时间不能动，防止提前进行地图截取("施工废墟")


@task.page(name="选择副本", target_text="作战机略", target_texts=[map_name])
def select_map(positions: Dict[str, Position]):
    pos = positions.get(map_name)
    control.click(pos.x, pos.y)


@task.page(name="选择副本等级", target_texts=[map_level, "下一步"])
def select_level(positions: Dict[str, Position]):
    pos = positions.get(map_level)
    control.click(pos.x, pos.y)
    time.sleep(2)
    pos = positions.get("下一步")
    control.click(pos.x, pos.y)


@task.page(name="退出", target_texts=["^放弃$", "^暂离$"])
def exit_map(positions: Dict[str, Position]):
    pos = positions.get("^放弃$")
    control.click(pos.x, pos.y)


@task.page(name="结算界面", target_texts=["^完成$", "^执照等级$"])
def settle(positions: Dict[str, Position]):
    pos = positions.get("^完成$")
    control.click(pos.x, pos.y)
