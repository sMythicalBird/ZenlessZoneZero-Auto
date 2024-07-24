# -*- coding: utf-8 -*-
""" 
@file:      selectBuff.py
@time:      2024/7/24 下午3:57
@author:    sMythicalBird
"""
import time
from typing import Dict


from schema import Position
from utils import control, screenshot
from utils.task import task
from re import template


def get_pos(text: str):
    text = template(text)
    img = screenshot()  # 截图
    ocr_Results = task.ocr(img)  # OCR识别
    # print(ocr_Results)
    positions = []
    for ocr_result in ocr_Results:
        if text.search(ocr_result.text):
            # print(ocr_result)
            positions.append(
                [
                    (ocr_result.position[0] + ocr_result.position[2]) / 2,
                    (ocr_result.position[1] + ocr_result.position[3]) / 2,
                ]
            )
    return positions


buff_class = ["冻结", "暴击", "决斗" "闪避"]


# 选择类，出现同类持有的选择事件，主要选择鸣徽或者邦布，诡术鸣徽(如果遇到的话)，优先级降低一级，避免与不可触碰之物冲突
@task.page(name="选择_鸣徽", target_texts=["同类持有", "^选择$"])
def action():
    img = screenshot()  # 截图
    ocr_Results = task.ocr(img)  # OCR识别
    print(ocr_Results)
    sel_text = template("^选择$")
    sel_list = []
    for ocr_result in ocr_Results:
        if sel_text.search(ocr_result.text):  # 识别到选择并记录
            sel_list.append(
                [
                    (ocr_result.position[0] + ocr_result.position[2]) / 2,
                    (ocr_result.position[1] + ocr_result.position[3]) / 2,
                ]
            )
    for each in buff_class:
        text = template(each)  # 需要的buff种类
        for ocr_result in ocr_Results:
            if text.search(ocr_result.text):  # 识别到buff种类
                left = ocr_result.position[0] - 30
                right = ocr_result.position[2] + 30
                # 识别到buff种类，选择
                for pos in sel_list:
                    if pos[0] > left and pos[0] < right:  # 点击返回
                        control.click(pos[0], pos[1])
                        return
    for pos in sel_list:  # 防止遇到不可触碰事件
        control.click(pos[0], pos[1])
        time.sleep(0.1)


@task.page(name="丢弃操作", target_texts=["^丢弃$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^丢弃$")
    control.click(pos.x, pos.y)
