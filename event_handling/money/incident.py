# -*- coding: utf-8 -*-
""" 
@file:      incident.py
@time:      2024/8/30 上午2:23
@author:    sMythicalBird
"""
import time
from typing import Dict
from schema import Position
from utils import control
from utils.task import task_money as task
from .conditional import stage
from pydirectinput import (
    press,
    mouseDown,
    mouseUp,
    keyDown,
    keyUp,
    moveRel,
)
from schema.cfg.zero_info import state_zero


# 选择委托
@task.page(name="选择委托", target_texts=["^战斗委托$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^战斗委托$")
    control.click(pos.x, pos.y)
    time.sleep(0.1)
    control.click(pos.x, pos.y)


# 选择关卡
@task.page(name="选择关卡", target_texts=["真·拿命验收$", "^下一步$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("真·拿命验收$")
    control.click(pos.x, pos.y)
    time.sleep(0.5)
    pos = positions.get("^下一步$")
    control.click(pos.x, pos.y)


@task.page(name="选择关卡_滚动", priority=6, target_texts=["零号空洞的挑战"])
def action():
    time.sleep(0.3)
    control.move_at(1000, 500, 1000, 200)


@task.page(name="选择关卡_滚动", priority=2, target_texts=["关键敌情", "委托详情"])
def action():
    time.sleep(0.3)
    control.move_at(1000, 500, 1000, 200)


@task.page(name="出战", target_texts=["^出战$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^出战$")
    control.click(pos.x, pos.y)
    stage.moneyFightFlag = True  # 更改战斗标志
    state_zero.fightCount += 1  # 战斗次数+1


@task.page(name="出战_等级低", target_texts=["平均等级较低", "出战$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("出战$")
    control.click(pos.x, pos.y)


def money_fight():
    moveRel(250, 0, relative=True)
    time.sleep(0.3)
    keyDown("w")
    keyDown("shift")
    time.sleep(0.1)
    mouseDown()
    time.sleep(0.1)
    mouseUp()
    time.sleep(0.1)
    press("space", duration=0.1)


def money_go(t1: float, t2: float, t3: int):
    time.sleep(t1)
    moveRel(-250, 0, relative=True)
    time.sleep(t2)
    for i in range(t3):
        time.sleep(0.1)
        press("f", duration=0.1)
    keyUp("shift")
    keyUp("w")


# 战斗
@task.page(name="战斗中", target_texts=["^Space$"])
def action():
    time.sleep(0.3)
    # 击碎箱子
    money_fight()
    # 交付任务
    money_go(3.2, 0.8, 5)
    control.esc()  # 若未找到对话则退出


# 高坂对话
@task.page(name="高坂对话", target_texts=["高坂"])
def action(positions: Dict[str, Position]):
    for i in range(5):
        control.press("space", duration=0.1)
        time.sleep(0.1)
        control.press("1", duration=0.1)
        time.sleep(0.1)


# 通关
@task.page(name="通关", priority=2, target_texts=["^完成$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^完成$")
    control.click(pos.x, pos.y)
    stage.moneyFightFlag = False  # 通关后退出战斗标志
    time.sleep(0.1)


# 重新开始
@task.page(name="重新开始", target_texts=["^重新开始$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^重新开始$")
    control.click(pos.x, pos.y)


# 重新开始
@task.page(name="重新开始_确认", target_texts=["是否重新开始战斗", "^确认$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^确认$")
    control.click(pos.x, pos.y)


# 点击HDD
@task.page(name="传送HDD", target_texts=["H.D.D"])
def action(positions: Dict[str, Position]):
    pos = positions.get("H.D.D")
    control.click(pos.x, pos.y)


# 优先级最低，必定可以匹配上，用来跳过一些无用对话,战斗过程中禁用
@task.page(name="默认匹配项", priority=0)
def action():
    if stage.moneyFightFlag:  # 处于战斗状态则跳出不执行
        time.sleep(0.2)
        return
    control.press("space", duration=0.1)
    time.sleep(0.1)


# 传送到HDD并打开
@task.page(name="传送_确认", target_texts=["^确认", "是否传送至该地点"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^确认")
    control.click(pos.x, pos.y)
    time.sleep(2)
    for i in range(3):
        time.sleep(0.2)
        press("f", duration=0.1)


# 不知道有没有用，先留着
@task.page(name="休息_离开", target_texts=["^离开$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^离开$")
    control.click(pos.x, pos.y)
    time.sleep(1)


# 当看到档案架则打开地图开始传送
@task.page(name="选择地图", target_texts=["^影像档案架$"])
def action():
    control.press("m", duration=0.1)


# 领取月卡
@task.page(name="月卡", target_texts=["今日到账"])
def action(positions: Dict[str, Position]):
    pos = positions.get("今日到账")
    control.click(pos.x, pos.y)
    time.sleep(1)
    press("esc", duration=0.1)
    time.sleep(1)
