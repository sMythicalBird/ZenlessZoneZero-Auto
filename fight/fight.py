# -*- coding: utf-8 -*-
""" 
@file:      fight.py
@time:      2024/7/10 上午2:35
@author:    sMythicalBird
"""
import math
import threading
import time
from datetime import datetime
from re import template
from threading import Thread
from typing import Dict
import cv2
from pydirectinput import press, keyDown, keyUp, mouseDown, mouseUp, moveRel
from schema import Position, info
from schema.config import Tactic
from utils import (
    fightTacticsDict,
    RootPath,
    characterIcons,
    config,
    control,
    screenshot,
    logger,
)
from utils.task import task, find_template
from .light_detector import detector
from .combo_detect import combo_detect  # 连携技的判断

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
        combo_attack = combo_detect(img)
        execute_tactic_event.set()  # Signal to suspend fight_login
        if combo_attack:
            mouse_press("left", 0.05)
            time.sleep(0.1)
            mouse_press("left", 0.05)
            time.sleep(0.1)
        elif results["yellow"]["rect"]:
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
                # 切人后切换逻辑，重置所有按键
                keyUp("w")
                keyUp("a")
                keyUp("s")
                keyUp("d")
                mouseUp(button="left")
                break
    mouse_press("middle", 0.05)


def current_character():
    """
    获取当前角色
    """
    img = screenshot()
    for chara, chara_icon in characterIcons.items():
        imgPosition = find_template(img, chara_icon, (0, 0, 200, 120), threshold=0.9)
        if imgPosition is not None:
            if chara in fightTacticsDict:
                return chara
    return "默认"


def calc_angle(x, y, w, h):
    """
    计算圆点坐标与屏幕中心的夹角
    :param x: 圆点横坐标
    :param y: 圆点纵坐标
    :param w: 屏幕宽度
    :param h: 屏幕高度
    :return: 圆点与屏幕中心的夹角
    """
    x0 = w / 2 + 0.5
    y0 = h / 2 + 0.5
    delta_x = x - x0
    delta_y = y0 - y
    angle = math.degrees(math.atan2(delta_y, delta_x))

    return angle


def search_point():
    """
    在屏幕中搜索指定圆点，并返回匹配度和位置
    """
    # 定义屏幕裁剪的区域大小，以减少计算量并提高匹配准确率
    h_crop = 85
    w_crop = 225  # 屏幕裁剪区域高度和宽度，减小计算量，提高匹配准确率
    screen = screenshot()  # 截取当前屏幕
    h, w, _ = screen.shape  # 获取屏幕的宽高
    # 复制并裁剪屏幕图像，以减少计算量并提高匹配准确率
    sub_screen = screen.copy()[h_crop : h - h_crop, w_crop : w - w_crop]
    h1, w1, _ = sub_screen.shape  # 获取裁剪后图像的宽高

    # 将裁剪后的图像转换为灰度图像，以便进行匹配
    sub_screen_gray = cv2.cvtColor(sub_screen, cv2.COLOR_RGB2GRAY)
    # 使用模板匹配方法在灰度图像中寻找匹配区域
    result = cv2.matchTemplate(sub_screen_gray, image_to_quan, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)  # 获取匹配度最高的位置和值
    return h1, w1, max_val, max_loc


def turn():
    """
    地图中自动寻路 适用于地图中的转向
    """
    # 初始化标志变量
    search_count = 0
    # 通过循环调整视角到最高处俯视，以便于计算圆点坐标夹角
    for i in range(3):
        moveRel(xOffset=0, yOffset=300, relative=True, duration=0.2)
    # 进入主循环，直到匹配成功或满足退出条件
    while True:
        search_count += 1  # 尝试次数加1
        h1, w1, max_val, max_loc = search_point()  # 获取匹配度最高的位置和值
        # 如果最大匹配度超过设定阈值，则认为匹配成功
        if max_val > 0.8:
            search_count = 0  # 匹配成功，尝试次数清零
            x, y = max_loc  # 获取匹配区域的左上角坐标
            x += image_to_quan.shape[1] / 2  # 计算匹配区域中心点的x坐标
            y += image_to_quan.shape[0] / 2  # 计算匹配区域中心点的y坐标
            angle = calc_angle(x, y, w1, h1)  # 计算中心点相对于图像中心的夹角
            delta_ang = abs(angle - 90)  # 计算夹角与90度的差值
            # 根据夹角差值的大小，决定横向移动的距离，以调整视角
            sign = int(math.copysign(1, x - w1 / 2))  # 根据中心点位置决定移动方向
            mov_x = (
                400
                if delta_ang > 60
                else 200 if delta_ang > 30 else 100 if delta_ang > 10 else 10
            )
            mov_x *= sign  # 根据sign变量决定移动方向
            # 执行视角调整
            moveRel(xOffset=mov_x, yOffset=0, relative=True, duration=0.2)
            # 如果夹角差值小于等于2度，则认为视角调整成功，退出循环
            if delta_ang <= 2:
                press("w", duration=2)
        else:
            time.sleep(0.05)
            if search_count >= 10:
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
    fight_counts = {chara: 0 for chara in characterIcons}
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
