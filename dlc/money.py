# -*- coding: utf-8 -*-
""" 
@file:      dlc1.py
@time:      2024/7/21 上午12:18
@author:    sMythicalBird
"""
import time
from typing import Dict
from schema import Position
from utils import control
from utils.task import task
from pydirectinput import (
    press,
    click,
    moveTo,
    mouseDown,
    mouseUp,
    keyDown,
    keyUp,
    scroll,
    moveRel,
)

fflag = 0


def money_fight():
    moveRel(110, 0, relative=True)
    time.sleep(0.3)
    keyDown("w")
    keyDown("shift")
    time.sleep(0.1)
    mouseDown()
    time.sleep(0.1)
    mouseUp()
    time.sleep(0.1)
    press("space", duration=0.1)


def money_go(t1: float, t2: float, t3: float):
    time.sleep(t1)
    keyDown("d")
    time.sleep(t2)
    keyUp("d")
    time.sleep(t3)
    keyUp("shift")
    keyUp("w")


# 战斗
@task.page(name="战斗中", target_texts=["^Space$"])
def action(positions: Dict[str, Position]):
    global fflag
    # 击碎箱子
    time.sleep(0.2)
    money_fight()
    # 交付任务
    money_go(3.5, 0.5, 0.5)
    time.sleep(0.3)
    press("f", duration=0.1)
    fflag = 1


# 选择委托
@task.page(name="选择委托", target_texts=["^战斗委托$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^战斗委托$")
    control.click(pos.x, pos.y)


# 选择关卡
@task.page(name="选择关卡", target_texts=["真·拿命验收$", "^下一步$"])
def action(positions: Dict[str, Position]):
    time.sleep(0.3)
    pos = positions.get("真·拿命验收$")
    control.click(pos.x, pos.y)
    time.sleep(0.5)
    pos = positions.get("^下一步$")
    control.click(pos.x, pos.y)


@task.page(name="出战", target_texts=["^出战$"])
def action(positions: Dict[str, Position]):
    global fflag
    time.sleep(0.3)
    pos = positions.get("^出战$")
    control.click(pos.x, pos.y)
    fflag = 0


# 结尾对话
@task.page(name="对话1", target_texts=["不堪一击"], exclude_texts=["确实如此"])
def action():
    press("space", duration=0.1)
    time.sleep(0.2)


@task.page(name="对话2", target_texts=["确实如此", "太脆弱了"])
def action(positions: Dict[str, Position]):
    pos = positions.get("确实如此")
    control.click(pos.x, pos.y)
    time.sleep(0.5)
    press("space", duration=0.1)


# 结尾对话
@task.page(name="对话3", target_texts=["把录像发给我"])
def action():
    press("space", duration=0.1)
    time.sleep(0.2)


# 通关
@task.page(name="通关", target_texts=["^完成$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^完成$")
    control.click(pos.x, pos.y)
    time.sleep(0.3)


@task.page(name="休息_离开", target_texts=["^离开$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^离开$")
    control.click(pos.x, pos.y)


@task.page(name="主界面", target_texts=["^影像档案架$"])
def action():
    time.sleep(1)
    moveRel(400, 0, relative=True)
    time.sleep(1)
    press("w", duration=0.2)
    time.sleep(1)
    moveRel(380, 0, relative=True)
    time.sleep(1)
    press("w", duration=0.8)
    time.sleep(1)
    moveRel(-400, 0, relative=True)
    time.sleep(1)
    press("w", duration=0.3)
    time.sleep(0.3)
    press("f", duration=0.1)


@task.page(name="可能对话", priority=0)
def action():
    global fflag
    if fflag:
        press("space", duration=0.1)
    time.sleep(0.2)
