# -*- coding: utf-8 -*-
"""
@file:      fight_only
@time:      2024/9/3 16:03
@author:    sMythicalBird
"""
import threading
import time
from re import template
from threading import Thread
from pydirectinput import press, keyDown, keyUp, mouseDown, mouseUp
from utils import (
    screenshot,
    logger,
)
from utils.task import find_template
from utils.task import task_fight as task
from schema.cfg.info import fight_logic_daily
from schema.cfg.zero_info import Tactic

from .light_detector import detector
from .combo_detect import combo_detect  # 连携技的判断


def is_not_fight(text: str):
    """
    判断是否还在战斗中,检测空格键是否存在
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


def detector_task(run_flag: threading.Event, execute_tactic_event: threading.Event):
    """
    检测光效
    run_flag: 是否允许继续运行战斗
    execute_tactic_event: 检测到光效后阻塞战斗逻辑
    """
    while run_flag.is_set():  # 是否允许继续运行
        img = screenshot()
        # 创建光效检测器实例
        results = detector.detect_light_effects(img)
        combo_attack = combo_detect(img)
        # 连携技和黄光回切人，给战斗一个阻塞来切换战斗逻辑
        if combo_attack:
            execute_tactic_event.clear()  # 阻塞战斗，如果有的话
            logger.debug(f"进入连携技模式")
            mouse_press("left", 0.05)
            time.sleep(0.1)
            mouse_press("left", 0.05)
            time.sleep(0.1)
            execute_tactic_event.set()  # 释放战斗
        elif results["yellow"]["rect"]:
            execute_tactic_event.clear()  # 阻塞战斗，如果有的话
            logger.debug(f"进入黄光战斗模式")
            for tactic in fight_logic_daily.tactics["黄光"].get_cur_logic():
                for _ in range(tactic.repeat):
                    execute_tactic(tactic)
                    if tactic.delay:
                        time.sleep(tactic.delay)
            execute_tactic_event.set()  # 释放战斗
        elif results["red"]["rect"]:
            logger.debug(f"进入红光战斗模式")
            for tactic in fight_logic_daily.tactics["红光"].get_cur_logic():
                for _ in range(tactic.repeat):
                    execute_tactic(tactic)
                    if tactic.delay:
                        time.sleep(tactic.delay)


# 定义战斗逻辑
def fight_login(
    run_flag: threading.Event,
    execute_tactic_event: threading.Event,
    fighting_flag: threading.Event,
):
    """
    进入战斗
    """
    while run_flag.is_set():
        fighting_flag.wait()  # 是否继续战斗
        mouse_press("middle", 0.05)

        # 检测在场角色
        cur_character = current_character()
        if cur_character == "默认":  # 未找到角色头像(可能被其他动画挡住了),等待0.2s
            time.sleep(0.2)
            continue
        logger.debug(f"进入{cur_character}战斗模式")

        # 获取当前角色战斗逻辑
        fight_tactics = fight_logic_daily.tactics[cur_character].get_cur_logic()
        # 执行攻击
        continue_flag = False
        for tactic in fight_tactics:
            if continue_flag:  # 由于切人或其他原因，终止当前战斗逻辑，退出for循环
                break
            for _ in range(tactic.repeat):
                if not execute_tactic_event.is_set():  # 检测到光效后等待
                    continue_flag = True
                    execute_tactic_event.wait()
                    break
                if not fighting_flag.is_set():  # 是否继续战斗
                    continue_flag = True
                    fighting_flag.wait()
                    break
                # 执行逻辑
                execute_tactic(tactic)
                if tactic.delay:
                    time.sleep(tactic.delay)
        # 每次循环结束时，重置一次案件，防止按键一直按下卡住程序
        keyUp("w")
        keyUp("a")
        keyUp("s")
        keyUp("d")
        keyUp("shift")
        mouseUp(button="left")
        mouse_press("middle", 0.05)


def current_character():
    """
    获取当前角色
    """
    img = screenshot()
    for chara, chara_icon in fight_logic_daily.char_icons.items():
        img_position = find_template(img, chara_icon, (0, 0, 200, 120), threshold=0.9)
        if img_position is not None:  # 找到角色头像
            return chara
    return "默认"  # 未找到角色头像


# 战斗逻辑
@task.page(name="战斗中", target_texts=["^Space$"])
def action():
    # 运行控制
    run_flag = threading.Event()  # 是否允许继续运行
    run_flag.set()

    execute_tactic_event = threading.Event()  # 检测到光效后阻塞战斗逻辑
    fighting_flag = threading.Event()  # 是否继续战斗

    # 启动弹反逻辑
    det_task = Thread(target=detector_task, args=(run_flag, execute_tactic_event))
    det_task.start()

    # 启动战斗逻辑
    fight_task = Thread(
        target=fight_login,
        args=(run_flag, execute_tactic_event, fighting_flag),
    )
    fight_task.start()

    # 开始战斗
    execute_tactic_event.set()
    fighting_flag.set()

    while True:
        # 检查是否还在战斗,连续判断四次，防止因为战斗动画的原因产生误判退出
        if is_not_fight("Space"):
            time.sleep(1)
            if is_not_fight("Space"):
                time.sleep(1)
                if is_not_fight("Space"):
                    time.sleep(1)
                    if is_not_fight("Space"):
                        run_flag.clear()
                        return  # 退出战斗
        time.sleep(1)  # 每秒检查一次是否还在战斗


@task.page(name="非战斗状态", priority=0)
def action():
    time.sleep(1)
