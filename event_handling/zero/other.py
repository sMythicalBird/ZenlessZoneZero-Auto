# -*- coding: utf-8 -*-
""" 
@file:      other.py
@time:      2024/8/30 上午2:17
@author:    sMythicalBird
"""
import time
from datetime import datetime
from typing import Dict
import numpy as np
from schema import Position
from schema.cfg.info import zero_cfg
from schema.cfg.zero_info import state_zero
from utils import control, logger
from utils.task import task_zero as task

from utils.detect.current import find_current

from utils.zero_api.components import set_weight, get_map_info
from utils.zero_api.auto_find_way import auto_find_way

map_name = zero_cfg.targetMap.Zone
map_level = zero_cfg.targetMap.Level


# 进入地图读取信息
@task.page(
    name="地图层数",
    priority=0,
    target_texts=["背包", "^当前层数"],
    exclude_texts=["特殊区域"],
)
def grid_map(screen: np.ndarray):
    # 判断是否在进入事件对话，检查是否可以找到自身位置
    k = find_current()
    if not k:  # 不在地图中
        control.press("space")
        return
    # 检查离开标志
    if state_zero.exitFlag:
        control.esc()
        return
    # 超过地图最大时间
    if (datetime.now() - state_zero.entryMapTime).total_seconds() > zero_cfg.maxMapTime:
        print("超过地图最大时间")
        logger.debug("长时间处于地图中，退出地图")
        control.esc()
        return
    control.scroll(-5)
    time.sleep(0.5)
    # 零号业绩相关的判断
    # 根据模式判断逻辑
    if zero_cfg.modeSelect == 1:
        if state_zero.stage1flag == 1:  # 向上走
            control.press("w", duration=0.05)
            time.sleep(0.5)
            state_zero.stage1flag = 2
            return
        elif state_zero.stage1flag == 2:
            for i in range(3):
                control.press("w", duration=0.05)
                time.sleep(0.3)
            state_zero.stage1flag = 3
            return
        elif state_zero.stage1flag == 3:
            for i in range(4):
                control.press("w", duration=0.05)
                time.sleep(0.3)
            state_zero.stage1flag = 0
            return
    elif zero_cfg.modeSelect == 3:
        # 快速拿银行
        if state_zero.currentStage == 3:
            control.press("a", duration=0.05)
            time.sleep(0.3)
            control.press("w", duration=0.05)
            time.sleep(0.3)
            return
    elif zero_cfg.modeSelect == 4 or zero_cfg.modeSelect == 2:
        # 快速拿业绩
        if state_zero.currentStage == 2:
            if state_zero.stage2Count > 0:  # 向业绩移动
                state_zero.stage2Count -= 1
                control.press("d", duration=0.05)
                time.sleep(0.3)
                control.press("w", duration=0.05)
                time.sleep(0.3)
                return
            else:  # 当无业绩时才会执行此处逻辑，此时将调整状态，进入下一层
                state_zero.currentStage = 10
                return
        # 业绩拿完后，进入下一层
        elif state_zero.currentStage == 10:
            control.press("s", duration=0.05)
            time.sleep(0.3)
            for i in range(3):
                control.press("a", duration=0.05)
                time.sleep(0.3)
            control.press("w", duration=0.05)
            time.sleep(0.3)
            control.press("a", duration=0.05)
            time.sleep(0.3)
            control.press("w", duration=0.05)
            time.sleep(0.3)
            control.press("w", duration=0.05)
            time.sleep(0.3)
            state_zero.currentStage = 0  # 还原状态
            return

    # 获取地图信息
    map_info = get_map_info(screen)
    if not map_info:
        logger.debug("未识别到地图信息")
        return
    # 寻路
    next_way = auto_find_way(map_info)
    # 在地图但未识别到足够的地图信息做路径搜索
    if not next_way:
        logger.debug("未找到路径")
        return
    (mc, dirct) = next_way  # 获取下一个格子信息和移动方向
    # 炸弹判断:当下一关是战斗且解锁炸弹,炸掉
    print(mc.name)
    if mc.name == "怪物" and state_zero.hasBoom:
        state_zero.hasBoom = False
        control.press("r", duration=0.1)
        time.sleep(1.5)  # 防止炸弹未点出来就跳过
        return
    # 终点类:传送点，暂时离开，boss站,红色路由，将偏移量置0，在boss站之后赋值，控制旧都列车在零号业绩和银行的视角拖拽，当传送之后再还原
    if mc.name == "终点":
        state_zero.currentStage = 0  # 重置偏移量
    if mc.name == "邦布商店":
        if (
            k.x2 > 650 and k.y2 > 550 and dirct.value == "d"
        ):  # 当商店在右下且向右走，则容易挡到终点，加一次判断
            control.press("d", duration=0.1)
            time.sleep(0.5)

    control.press(str(dirct), duration=0.1)
    # 进战斗时需要计时，未防止战斗多次重置时间，不写在战斗函数中
    state_zero.lastMoveTime = datetime.now()


# 炸弹使用
@task.page(name="炸弹", target_texts=["^交叉爆破$", "^使用$"])
def select_map(positions: Dict[str, Position]):
    pos = positions.get("^使用$")
    control.click(pos.x, pos.y)
    time.sleep(1)


@task.page(name="boss关", target_texts=["^完成本次探索最终挑战$"])
def select_map(positions: Dict[str, Position]):
    pos = positions.get("^完成本次探索最终挑战$")
    control.click(pos.x, pos.y)
    time.sleep(1)


@task.page(name="选择角色", target_texts=["出战"])
def action(positions: Dict[str, Position]):
    pos = positions.get("出战")
    control.click(pos.x, pos.y)
    state_zero.entryMapTime = datetime.now()  # 进入地图时间
    state_zero.fightCount += 1  # 战斗次数记录
    state_zero.currentStage = 0  # 进入战斗，无偏移
    state_zero.hasBoom = zero_cfg.hasBoom  # 是否有炸弹
    state_zero.exitFlag = False  # 离开标志
    state_zero.teamMate = zero_cfg.teamMates  # 获取队友数量
    if (
        zero_cfg.modeSelect == 2 or zero_cfg.modeSelect == 4
    ):  # 需要拾取业绩，则将业绩优先级调高
        state_zero.rewardCount = zero_cfg.targetMap.reward_count()  # 获取奖励次数
        set_weight("零号业绩", 10)
    if state_zero.teamMate:  # 需要队友，则将队友优先级调高
        set_weight("呼叫增援", 10)


@task.page(name="选择副本", target_text="作战机略", target_texts=[map_name])
def select_map(positions: Dict[str, Position]):
    pos = positions.get(map_name)
    control.click(pos.x, pos.y)


@task.page(name="选择副本等级", target_texts=[map_level, "下一步"])
def select_level(positions: Dict[str, Position]):
    pos = positions.get(map_level)
    control.click(pos.x, pos.y)
    time.sleep(0.5)
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


# # 全通模式且在旧都列车，拿侵蚀换buff
# if config.modeSelect == 1 and map_name == "旧都列车":
#
#     @task.page(name="假面研究者_换buff", target_texts=["假面研究者", "接受他的好意"])
#     def settle(positions: Dict[str, Position]):
#         pos = positions.get("接受他的好意")
#         control.click(pos.x, pos.y)


# 打不过溜了
@task.page(name="打不过跑路", target_texts=["^退出战斗$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^退出战斗$")
    control.click(pos.x, pos.y)
    time.sleep(2)


# 打不过怪
@task.page(name="打不过怪", target_texts=["^撤退$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^撤退$")
    control.click(pos.x, pos.y)
    time.sleep(2)
