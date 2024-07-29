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
from utils.task import task, find_template
from re import template
from pydirectinput import press, keyDown, keyUp, mouseDown, mouseUp, moveRel
from utils import fightTacticsDict, RootPath
import utils
from schema.config import Tactic
from .light_detector import detector
from threading import Thread
import threading
import cv2

image_path = RootPath / "download" / "yuan.png"
image_to_quan = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)


# Create an event for synchronization
# when 黄光thread execute tactic，block fight_login
execute_tactic_event = threading.Event()


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
        execute_tactic_event.set()  # Signal to suspend fight_login
        if results["yellow"]["rect"]:
            logger.debug(f"进入黄光战斗模式")
            for tactic in fightTacticsDict["黄光"]:
                for _ in range(tactic.repeat):
                    execute_tactic(tactic)
                    if tactic.delay:
                        time.sleep(tactic.delay)
        elif results["red"]["rect"]:
            logger.debug(f"进入红光战斗模式")
            for tactic in fightTacticsDict["红光"]:
                for _ in range(tactic.repeat):
                    execute_tactic(tactic)
                    if tactic.delay:
                        time.sleep(tactic.delay)
        execute_tactic_event.clear()  # Clear signal to resume fight_login


# 定义战斗逻辑
def fight_login(fight_counts: dict):
    """
    进入战斗
    """

    mouse_press("middle", 0.05)
    cur_character = current_character()

    # 5次执行完整逻辑或换人后退出
    for _ in range(5):
        prev_character = cur_character
        fight_tactics = fightTacticsDict[cur_character]
        logger.debug(f"进入{cur_character}战斗模式")
        # 选择攻击模式
        if cur_character in fight_counts:
            if fight_counts[cur_character] >= 2:  # 每两次攻击，释放一次技能
                if cur_character + "技能" in fightTacticsDict:
                    fight_tactics = fightTacticsDict[cur_character + "技能"]
                    logger.debug(f"进入{cur_character}技能战斗模式")
                fight_counts[cur_character] = 0
            else:
                fight_counts[cur_character] += 1
        # 执行攻击
        for tactic in fight_tactics:
            for _ in range(tactic.repeat):
                execute_tactic_event.wait()  # Wait if execute_tactic_event is set
                execute_tactic(tactic)
                if tactic.delay:
                    time.sleep(tactic.delay)
            # 如果人物变动，退出并切换战斗逻辑
            cur_character = current_character()
            if prev_character != cur_character:
                break
    mouse_press("middle", 0.05)
    # return fight_counts


def current_character():
    img = screenshot()
    for chara, chara_icon in utils.characters_icons.items():
        imgPosition = find_template(img, chara_icon, (0, 0, 200, 120), threshold=0.9)
        if imgPosition is not None:
            if chara in fightTacticsDict:
                return chara
    return "默认"


# 地图中自动寻路
def turn():
    cnt = 0  # 记录转向次数
    while True:
        flag = True
        cnt += 1
        if cnt > 4:
            break
        for i in range(10):
            screen = screenshot()
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
            result = cv2.matchTemplate(screen_gray, image_to_quan, cv2.TM_CCOEFF_NORMED)
            # max_val为识别图像左上角坐标
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.8:
                flag = False
                x, y = max_loc
                x += image_to_quan.shape[1] / 2
                y += image_to_quan.shape[0] / 2
                x = int(x)
                if y > 400:
                    moveRel(xOffset=1100, yOffset=0, relative=True)
                time.sleep(0.2)
                x = x - 648
                if -250 < x < 250:
                    x = int(abs(x) ** (1 / 1.28)) * (1 if x > 0 else -1)
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
    num = 1
    # 分别记录不同角色普通战斗模块执行次数，达到一定次数后执行技能战斗模块
    # 若角色技能战斗模块为空，则执行角色普通模块
    fight_counts = {chara: 0 for chara in utils.characters_icons}
    while True:
        fight_time = (datetime.now() - info.lastMoveTime).total_seconds()
        if fight_time > utils.config.maxFightTime:
            control.esc()
            break
        logger.debug(
            f"当前战斗时长{fight_time:.2f}s 剩余战斗时间{utils.config.maxFightTime - fight_time:.2f}s",
        )
        # 检查是否还在战斗,判断两次，防止因为战斗动画的原因产生误判退出
        if is_not_fight("Space"):
            time.sleep(2)
            if is_not_fight("Space"):
                # 防止战斗结束动画放完刚好进入地图，提前走格子出现路径混乱
                detectorFlag = False
                break
        # 判断转向
        if num % 2:
            turn()
        num += 1
        fight_login(fight_counts)


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
