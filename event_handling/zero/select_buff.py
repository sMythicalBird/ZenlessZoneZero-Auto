# -*- coding: utf-8 -*-
""" 
@file:      select_buff.py
@time:      2024/8/30 上午2:16
@author:    sMythicalBird
"""
from utils import control, screenshot
from utils.task import task_zero as task
from re import template
from schema.cfg.info import zero_cfg

selBuff = zero_cfg.selBuff  # 选择buff列表


# 选择类，出现同类持有的选择事件，主要选择鸣徽或者邦布，诡术鸣徽(如果遇到的话)，优先级降低一级，避免与不可触碰之物冲突
@task.page(name="选择_鸣徽", target_texts=["同类持有", "^选择$"])
def action():
    img = screenshot()  # 截图
    ocr_Results = task.ocr(img)  # OCR识别
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
    for each in selBuff:
        text = template(each)  # 需要的buff种类
        for ocr_result in ocr_Results:
            if text.search(ocr_result.text):  # 识别到buff种类
                left = ocr_result.position[0] - 30
                right = ocr_result.position[2] + 30
                # 识别到buff种类，选择
                for pos in sel_list:
                    if left < pos[0] < right:  # 点击返回
                        control.click(pos[0], pos[1])
                        return
    for pos in sel_list:  # 防止遇到不可触碰事件
        control.click(pos[0], pos[1])
