# -*- coding: utf-8 -*-
""" 
@file:      fight_zero.py
@time:      2024/8/30 上午2:26
@author:    sMythicalBird
"""
import math
import threading
import time
from datetime import datetime
from re import template
from threading import Thread
import cv2
from pydirectinput import press, keyDown, keyUp, mouseDown, mouseUp, moveRel
from utils import (
    control,
    screenshot,
    logger,
)
from utils.task import find_template
from utils.task import task_zero as task
from pathlib import Path
from schema.cfg.info import fight_logic_zero, zero_cfg
from schema.cfg.zero_info import Tactic

from .light_detector import detector
from .combo_detect import combo_detect  # 连携技的判断

img_path = (
    Path(__file__).parent.parent.parent / "resources/img/pic_1080x720/zero/yuan.png"
)
image_to_quan = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)


def waiting_optimization(max_time_seconds):
    max_iterations = int(max_time_seconds / 0.05)  # 假设每次休眠0.05秒
    iteration = 0
    should_return_true = False  # 标志变量

    while iteration < max_iterations:
        if combo_detect(screenshot()):
            should_return_true = True
            break
        time.sleep(0.05)  # 休眠0.05秒
        iteration += 1

    if should_return_true:
        return True
    else:
        return False


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


def technique_full(point="3000"):
    """
    判断终结技是否充满,满了释放终结技
    识别充能是否达到3000
    """
    text = template(str(point))
    img = screenshot()  # 截图
    ocr_Results = task.ocr(img)  # OCR识别
    for ocr_result in ocr_Results:
        if text.search(ocr_result.text):
            return True
    return False


middle_lock = False


def mouse_press(key: str, duration: float):
    """
    鼠标点击
    """
    if key == "middle" and middle_lock:
        ...
    else:
        mouseDown(button=key)
        time.sleep(duration)
        mouseUp(button=key)


keyboard_map = {"down": keyDown, "up": keyUp}
mouse_map = {"down": mouseDown, "up": mouseUp}


def key_press(key: str, duration: float):
    """
    键盘点击
    """
    keyDown(key=key)
    time.sleep(duration)
    keyUp(key=key)


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


def detector_task(
    run_flag: threading.Event,
    execute_tactic_event: threading.Event,
    detector_task_event: threading.Event,
):
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
        global middle_lock
        middle_lock = False  # 锁定鼠标中键
        if combo_attack:
            middle_lock = True
            execute_tactic_event.clear()  # 阻塞战斗，如果有的话
            logger.debug(f"进入连携技模式")
            while waiting_optimization(1.5):
                mouse_press("left", 0.05)
                mouse_press("left", 0.05)
            logger.debug(f"退出连携技模式")
            execute_tactic_event.set()  # 释放战斗
        # 终结技检测优先于检测光效
        if detector_task_event.is_set():
            if results["yellow"]["rect"]:
                execute_tactic_event.clear()  # 阻塞战斗，如果有的话
                logger.debug(f"进入黄光战斗模式")
                for tactic in fight_logic_zero.tactics["黄光"].get_cur_logic():
                    for _ in range(tactic.repeat):
                        execute_tactic(tactic)
                        if tactic.delay:
                            time.sleep(tactic.delay)
                execute_tactic_event.set()  # 释放战斗
            elif results["red"]["rect"]:
                execute_tactic_event.clear()  # 阻塞战斗，如果有的话
                logger.debug(f"进入红光战斗模式")
                for tactic in fight_logic_zero.tactics["红光"].get_cur_logic():
                    for _ in range(tactic.repeat):
                        execute_tactic(tactic)
                        if tactic.delay:
                            time.sleep(tactic.delay)
                execute_tactic_event.set()  # 释放战斗


# 定义战斗逻辑
def fight_login(
    run_flag: threading.Event,
    execute_tactic_event: threading.Event,
    fighting_flag: threading.Event,
    detector_task_event: threading.Event,
):
    """
    进入战斗
    """
    while run_flag.is_set():
        fighting_flag.wait()  # 是否继续战斗
        execute_tactic_event.wait()  # 等待光效检测结束
        mouse_press("middle", 0.05)
        threshold = 0.9
        # 检测在场角色
        cur_character = current_character(threshold)
        while cur_character == "默认":  # 未找到角色头像(可能被其他动画挡住了),等待0.2s
            time.sleep(0.2)
            threshold = threshold - 0.1
            cur_character = current_character(threshold)
        logger.debug(f"进入{cur_character}战斗模式")

        # 获取当前角色战斗逻辑
        fight_tactics = fight_logic_zero.tactics[cur_character].get_cur_logic()
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

                if tactic.endure:  # 霸体强制连招
                    detector_task_event.clear()
                    execute_tactic(tactic)
                    detector_task_event.set()
                else:
                    execute_tactic(tactic)
                if tactic.delay:
                    time.sleep(tactic.delay)

        execute_tactic_event.wait()  # 防止middle键中断连携技
        mouse_press("middle", 0.05)
        # 每次循环结束时，重置一次案件，防止按键一直按下卡住程序
        keyUp("w")
        keyUp("a")
        keyUp("s")
        keyUp("d")
        keyUp("shift")
        mouseUp(button="left")


def technique_detection(
    run_flag: threading.Event,
    execute_tactic_event: threading.Event,
):
    while run_flag.is_set():
        threshold = 0.9
        execute_tactic_event.wait()
        # 检测在场角色
        cur_character = current_character(threshold)
        while cur_character == "默认":  # 未找到角色头像(可能被其他动画挡住了),等待0.2s
            time.sleep(0.2)
            threshold = threshold - 0.1
            cur_character = current_character(threshold)
        # 判断终结技充满，并选人释放，默认直接释放
        if (
            cur_character == zero_cfg.carry["char"]  # 判断为指定角色
            or zero_cfg.carry["char"]
            not in fight_logic_zero.char_icons  # 未正确配置指定角色(直接释放)
            and technique_full(zero_cfg.carry["point"])  # 判断终结技充满
        ):
            key_press("q", 0.1)
            time.sleep(3)


def current_character(threshold=0.9):
    """
    获取当前角色
    """
    img = screenshot()
    for chara, chara_icon in fight_logic_zero.char_icons.items():
        img_position = find_template(
            img, chara_icon, (0, 0, 200, 120), threshold=threshold
        )
        if img_position is not None:  # 找到角色头像
            return chara
    return "默认"  # 未找到角色头像


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
    # 运行控制
    run_flag = threading.Event()  # 是否允许继续运行
    run_flag.set()

    execute_tactic_event = threading.Event()  # 检测到光效后阻塞战斗逻辑
    detector_task_event = threading.Event()  # 阻塞红黄光检测
    fighting_flag = threading.Event()  # 是否继续战斗
    technique_event = threading.Event()  # 终结技充满事件
    # 启动弹反逻辑
    det_task = Thread(
        target=detector_task, args=(run_flag, execute_tactic_event, detector_task_event)
    )
    det_task.start()

    # 启动战斗逻辑
    fight_task = Thread(
        target=fight_login,
        args=(run_flag, execute_tactic_event, fighting_flag, detector_task_event),
    )
    fight_task.start()

    # 启动终结技检测逻辑
    technique_task = Thread(
        target=technique_detection, args=(run_flag, execute_tactic_event)
    )
    technique_task.start()
    # 开始战斗
    execute_tactic_event.set()
    fighting_flag.set()
    detector_task_event.set()
    while True:
        if not task.is_running():
            run_flag.clear()
            return
        # 检查是否还在战斗,连续判断四次，防止因为战斗动画的原因产生误判退出
        if is_not_fight("Space"):
            time.sleep(1)
            if not task.is_running():
                run_flag.clear()
                return
            if is_not_fight("Space"):
                time.sleep(1)
                if not task.is_running():
                    run_flag.clear()
                    return
                if is_not_fight("Space"):
                    time.sleep(1)
                    if is_not_fight("Space"):
                        run_flag.clear()
                        return  # 退出战斗
        time.sleep(1)  # 每秒检查一次是否还在战斗
