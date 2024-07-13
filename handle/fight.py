# -*- coding: utf-8 -*-
""" 
@file:      fight.py
@time:      2024/7/10 上午2:35
@author:    sMythicalBird
"""
import time
from typing import Dict
from datetime import datetime
from schema import Position, info
from utils import control, screenshot, logger
from utils.task import task
from re import template
from pydirectinput import press


def is_not_fight(text: str):
    text = template(text)
    img = screenshot()  # 截图
    ocr_Results = task.ocr(img)  # OCR识别
    # print(ocr_Results)
    for ocr_result in ocr_Results:
        if text.search(ocr_result.text):
            return False
    return True


# 定义战斗逻辑，两次3a1e接q
def fight_login():
    control.attack()
    time.sleep(0.5)
    control.attack()
    time.sleep(0.5)
    control.attack()
    time.sleep(0.5)
    press("e", duration=0.1)
    time.sleep(0.5)
    press("space", duration=0.1)
    time.sleep(0.2)
    press("shift", duration=0.1)
    time.sleep(0.2)
    control.attack()
    time.sleep(0.5)
    control.attack()
    time.sleep(0.5)
    control.attack()
    time.sleep(0.5)
    press("e", duration=0.1)
    time.sleep(0.5)
    # press("space", duration=0.1)
    # time.sleep(0.2)
    press("shift", duration=0.1)
    time.sleep(0.2)
    press("q", duration=0.1)
    time.sleep(0.2)


# 战斗逻辑
@task.page(name="战斗中", target_texts=["^Space$"])
def select_role(positions: Dict[str, Position]):
    # 向前跑一会 触发战斗，如果未触发，则直接退出
    time.sleep(2)
    # print("前进")
    control.head(1)
    # 持续进行战斗，若两分钟后还在当前页面，则战斗地图需要跑图或者练度太低(练度低估计也已经寄了)，那就跑路
    while True:
        fight_time = (datetime.now() - info.lastMoveTime).total_seconds()
        if fight_time > 120:
            control.esc()
            break
        logger.debug(
            f"当前战斗时长{fight_time:.2f}s 剩余战斗时间{120 - fight_time:.2f}s",
        )
        # 检查是否还在战斗,判断两次，防止因为战斗动画的原因产生误判退出
        if is_not_fight("Space"):
            time.sleep(2)
            if is_not_fight("Space"):
                # 防止战斗结束动画放完刚好进入地图，提前走格子出现路径混乱
                time.sleep(4)
                break
        # 继续战斗
        # print("战斗中")
        fight_login()


# 打不过溜了
@task.page(name="打不过跑路", target_texts=["^退出战斗$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^退出战斗$")
    control.click(pos.x, pos.y)
    time.sleep(2)
