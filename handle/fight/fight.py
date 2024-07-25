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
from pydirectinput import press, keyDown, keyUp, mouseDown, mouseUp, moveRel
from utils import config, fightTactics, RootPath
from schema.config import Tactic
from .light_detector import detector
from threading import Thread
import cv2

image_path = RootPath / "download" / "yuan.png"
image_to_quan = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)


def is_not_fight(text: str):
    """
    判断是否还在战斗中
    """
    text = template(text)
    img = screenshot()  # 截图
    ocr_Results = task.ocr(img)  # OCR识别
    for ocr_result in ocr_Results:
        if text.search(ocr_result.text):
            return False
    return True


def mouse_press(key: str, duration: float):
    """
    鼠标点击
    """
    mouseDown(button=key)
    time.sleep(duration)
    mouseUp(button=key)


keyboard_map = {"down": keyDown, "up": keyUp}
mouse_map = {"down": mouseDown, "up": mouseUp}


def execute_tactic(tactic: Tactic):
    """
    执行战斗策略
    """
    if tactic.key is None:
        return
    # key 为鼠标操作
    if tactic.key in ["left", "right", "middle"]:
        if tactic.type_ == "press":
            mouse_press(tactic.key, tactic.duration)
        else:
            mouse_map[tactic.type_](button=tactic.key)
        return
    # key 为键盘操作
    if tactic.type_ == "press":
        press(tactic.key, duration=tactic.duration)
    else:
        keyboard_map[tactic.type_](tactic.key)


# 检测标志
detectorFlag = False


def detector_task():
    global detectorFlag
    while detectorFlag:
        img = screenshot()
        # 创建光效检测器实例
        results = detector.detect_light_effects(img)
        if results["yellow"]["rect"]:
            control.press("space", duration=0.1)
        # elif results["red"]["rect"]:
        #     control.press("shift", duration=0.1)


def keyboard_press(key: str, duration: float, interval: float):
    keyDown(key)
    time.sleep(duration)
    keyUp(key)
    time.sleep(interval)


def m_press(key: str, duration: float, interval: float):
    mouseDown(button=key)
    time.sleep(duration)
    mouseUp(button=key)
    time.sleep(interval)


def ef_login():
    for i in range(5):
        keyboard_press("shift", 0.025, 0.05)
        m_press("left", 0.025, 0.1)
        keyboard_press("space", 0.025, 0.05)
        m_press("left", 0.025, 0.025)
        keyboard_press("shift", 0.025, 0.025)
        m_press("left", 0.025, 0.1)
    keyboard_press("2", 0.025, 0.025)


# 定义战斗逻辑，两次3a1e接q
def fight_login():
    """
    进入战斗
    """
    mouse_press("middle", 0.1)
    # ef_login()
    for tactic in fightTactics:
        for _ in range(tactic.repeat):
            execute_tactic(tactic)
            if tactic.delay:
                time.sleep(tactic.delay)


# 地图中自动寻路
def turn():
    while True:
        flag = True
        for i in range(10):
            screen = screenshot()
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
            result = cv2.matchTemplate(screen_gray, image_to_quan, cv2.TM_CCOEFF_NORMED)
            # max_val为识别图像左上角坐标
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.85:
                flag = False
                x, _ = max_loc
                _, y = max_loc
                x += image_to_quan.shape[1] / 2
                y += image_to_quan.shape[0] / 2
                x = int(x)
                if y > 400:
                    moveRel(xOffset=1100, yOffset=0, relative=True)
                time.sleep(0.2)
                x = x - 648
                if abs(x) < 250:
                    if x > 0:
                        x = int(x ** (1 / 1.28))
                    else:
                        x = -int(abs(x) ** (1 / 1.28))
                moveRel(xOffset=x, yOffset=0, relative=True)
                if abs(x) <= 2:
                    press("w", duration=2)
                    break
            time.sleep(0.03)
        if flag:
            break


# 战斗逻辑
@task.page(name="战斗中", target_texts=["^Space$"])
def action():
    # 持续进行战斗，若两分钟后还在当前页面，则战斗地图需要跑图或者练度太低(练度低估计也已经寄了)，那就跑路
    global detectorFlag
    detectorFlag = True
    control.head(1.5)
    Thread(target=detector_task).start()
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
                detectorFlag = False
                break
        # 判断转向
        turn()
        # 执行战斗逻辑
        for i in range(3):
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
