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
from pydirectinput import press, keyDown, keyUp, mouseDown, mouseUp
from utils import config, fightTactics
from schema.config import Tactic
from handle.LightEffectDetector import lightEffectDetector
from threading import Thread


def is_not_fight(text: str):
    text = template(text)
    img = screenshot()  # 截图
    ocr_Results = task.ocr(img)  # OCR识别
    # print(ocr_Results)
    for ocr_result in ocr_Results:
        if text.search(ocr_result.text):
            return False
    return True


def mousePress(key: str, duration: float):
    mouseDown(button=key)
    time.sleep(duration)
    mouseUp(button=key)


keyboard_map = {"down": keyDown, "up": keyUp}
mouse_map = {"down": mouseDown, "up": mouseUp}


def execute_tactic(tactic: Tactic):
    # logger.debug(f"执行战斗策略: {tactic}")
    # 如果没有设置key，只设置了delay，则延迟delay时间
    if tactic.key is None:
        return
    # key 为鼠标操作
    if tactic.key in ["left", "right", "middle"]:
        if tactic.type_ == "press":
            mousePress(tactic.key, tactic.duration)
        else:
            mouse_map[tactic.type_](button=tactic.key)
        return
    # key 为键盘操作
    if tactic.type_ == "press":
        press(tactic.key, duration=tactic.duration)
    else:
        keyboard_map[tactic.type_](tactic.key)


# 检测标志
detector_flag = False


def detector():
    global detector_flag
    while detector_flag:
        img = screenshot()
        # 创建光效检测器实例
        detector = lightEffectDetector(img)
        results = detector.detect_light_effects(rect=True, peri=False)
        if results["yellow"]["rect"]:
            control.press("space")
        elif results["red"]["rect"]:
            control.press("shift")
        print(results)
        time.sleep(0.1)


# 定义战斗逻辑，两次3a1e接q
def fight_login():
    global detector_flag
    detector_flag = True
    Thread(target=detector).start()
    for tactic in fightTactics:
        for _ in range(tactic.repeat):
            execute_tactic(tactic)
            if tactic.delay:
                time.sleep(tactic.delay)
    detector_flag = False


# 战斗逻辑
@task.page(name="战斗中", target_texts=["^Space$"])
def action(positions: Dict[str, Position]):
    # 向前跑一会 触发战斗，如果未触发，则直接退出
    time.sleep(2)
    # print("前进")
    control.head(1)
    # 持续进行战斗，若两分钟后还在当前页面，则战斗地图需要跑图或者练度太低(练度低估计也已经寄了)，那就跑路
    while True:
        fight_time = (datetime.now() - info.lastMoveTime).total_seconds()
        if fight_time > config.maxFightTime:
            control.esc()
            break
        logger.debug(
            f"当前战斗时长{fight_time:.2f}s 剩余战斗时间{config.maxFightTime - fight_time:.2f}s",
        )
        # 检查是否还在战斗,判断两次，防止因为战斗动画的原因产生误判退出
        if is_not_fight("Space"):
            time.sleep(2)
            if is_not_fight("Space"):
                # 防止战斗结束动画放完刚好进入地图，提前走格子出现路径混乱
                break
        fight_login()


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
