# -*- coding: utf-8 -*-
"""
@file:      incident
@time:      2024/8/30 15:53
@author:    sMythicalBird
"""
import time

from utils.task import task_code as task
from utils import control, logger
from typing import Dict
from schema import Position
from schema.cfg.daily import code_list
from utils import screenshot
from re import template


def get_pos(text: str):
    text = template(text)
    img = screenshot()  # 截图
    ocr_results = task.ocr(img)  # OCR识别
    for ocr_result in ocr_results:
        if text.search(ocr_result.text):
            return ocr_result.position


# 点击更多
@task.page(name="更多", target_texts=["更多", "设置", "邮件"])
def action(positions: Dict[str, Position]):
    pos = positions.get("更多")
    control.click(pos.x, pos.y)
    time.sleep(1)


# 点击兑换码
@task.page(name="点击兑换码", target_texts=["兑换码", "公告", "脱离卡死"])
def action(positions: Dict[str, Position]):
    pos = positions.get("兑换码")
    control.click(pos.x, pos.y)
    time.sleep(1)


# 输入兑换码
@task.page(name="输入兑换码", target_texts=["请输入兑换码", "取消", "^兑换$"])
def action(positions: Dict[str, Position]):
    if code_list.code_cnt == 0:
        logger.debug("兑换码已全部兑换")
        control.press("f12")
        return
    # 获取兑换码
    code = code_list.get_code()
    # 输入兑换码
    pos = positions.get("请输入兑换码")
    logger.debug("点击输入框")
    time.sleep(0.1)
    control.click(pos.x, pos.y)
    time.sleep(0.4)
    # 检测是否已经点击到输入框
    while True:
        position = get_pos("请输入兑换码")
        if position:
            logger.debug("再次点击输入框")
            control.click(position.x, position.y)
            time.sleep(0.4)
        else:
            break
    show_code = "正在输入兑换码:" + code
    logger.debug(show_code)
    for each in code:
        control.press(each, duration=0.1)
        time.sleep(0.1)
    # 点击兑换
    pos = positions.get("^兑换$")
    control.click(pos.x, pos.y)
    time.sleep(2.8)
    control.press("esc", duration=0.1)


# 没东西就一直esc
@task.page(name="返回主界面", priority=0)
def action():
    control.press("esc", duration=0.1)
    time.sleep(1)
