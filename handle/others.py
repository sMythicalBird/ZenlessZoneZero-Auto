# -*- coding: utf-8 -*-
""" 
@file:      others.py
@time:      2024/7/10 上午2:38
@author:    sMythicalBird
"""

import time
from datetime import datetime
from typing import Dict
from pydirectinput import press
from schema import MapInfo, Position, info, sec_info, MapComponent
from utils import control, get_map_info, auto_find_way, config, logger
from utils.task import task
from utils.detect.current import find_current

map_name = config.targetMap.Zone
map_level = config.targetMap.Level
logger.debug(f"地图名称: {map_name}, 地图等级: {map_level}")


def get_map(info, m_name: str):
    if m_name == "旧都列车":
        map_info: MapInfo = get_map_info()

        logger.debug(map_info)

        info.mapWay = auto_find_way(map_info)
        # print(info.mapWay)
    elif m_name == "施工废墟":
        for i in range(7):
            info.mapWay.append((MapComponent(name="默认", x=0, y=0, index=-1), "d"))
        # print(info.mapWay)
    info.step = 0


# 进入地图读取信息
@task.page(name="地图层数_1", priority=0, target_texts=["背包", "^当前层数1"])
def grid_map_1():
    # 判断是否在进入事件对话，检查是否可以找到自身位置
    k = find_current()
    if not k:
        control.click(1000, 350)
        time.sleep(2)
        return
    if not info.mapWay:
        # 等待几秒再获取地图，防止刚进入地图动画未加载完成，这行不能再改了
        time.sleep(3)
        get_map(info, map_name)
    if not info.mapWay:
        return False
    (mc, dirct) = info.mapWay[info.step]
    # print("下一站,", mc.name)
    # 撞击次数和方向
    for i in range(mc.hit):
        # logger.debug(f"按下 {dirct} 移动")
        press(dirct, duration=0.1)
        time.sleep(0.3)
    if mc.name == "普通敌人" or mc.name == "精英敌人":
        # print("暂停打怪")
        time.sleep(5)
    time.sleep(2)
    info.step += 1
    # 进战斗时需要计时，未防止战斗多次重置时间，不写在战斗函数中
    info.lastMoveTime = datetime.now()
    if info.step == len(info.mapWay):
        info.reset_way()


@task.page(name="地图层数_2", priority=0, target_texts=["背包", "^当前层数2"])
def grid_map_2():
    # 判断是否在进入事件对话，检查是否可以找到自身位置
    k = find_current()
    if not k:
        control.click(1000, 350)
        time.sleep(2)
        return
    # 加一个延时，避免第一时间进入是按键无法触发
    time.sleep(2)
    # 来到第二层，收集零号业绩，固定路线不能乱动
    if not sec_info.mapWay:
        sec_info.get_way()
    # 按下方向
    press(sec_info.mapWay[sec_info.step], duration=0.1)
    sec_info.step += 1
    if sec_info.step == len(sec_info.mapWay):
        sec_info.reset_way()
        time.sleep(2)
        # 拿到零号业绩后确认
        control.esc()
        time.sleep(1)
        # 探索结束 跑路
        control.esc()
    time.sleep(1)


@task.page(name="选择角色", target_texts=["出战"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("出战")
    control.click(pos.x, pos.y)
    # 等待加载进入动画，这个时间不能动，防止提前进行地图截取("施工废墟")
    time.sleep(16)


@task.page(name="选择副本", target_text="作战机略", target_texts=[map_name])
def select_map(positions: Dict[str, Position]):
    pos = positions.get(map_name)
    control.click(pos.x, pos.y)
    time.sleep(2)


@task.page(name="选择副本等级", target_texts=[map_level, "下一步"])
def select_level(positions: Dict[str, Position]):
    pos = positions.get(map_level)
    control.click(pos.x, pos.y)
    time.sleep(2)
    pos = positions.get("下一步")
    control.click(pos.x, pos.y)
    time.sleep(2)


@task.page(name="退出", target_texts=["^放弃$", "^暂离$"])
def exit_map(positions: Dict[str, Position]):
    pos = positions.get("^放弃$")
    control.click(pos.x, pos.y)
    time.sleep(2)


# @task.page(name="确认退出", target_texts=["^确认$", "返回街区"])
# def confirm_exit(positions: Dict[str, Position]):
#     pos = positions.get("^确认$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


@task.page(name="结算界面", target_texts=["^完成$", "^执照等级$"])
def settle(positions: Dict[str, Position]):
    pos = positions.get("^完成$")
    control.click(pos.x, pos.y)
    time.sleep(2)
