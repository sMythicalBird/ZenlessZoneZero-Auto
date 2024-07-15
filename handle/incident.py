# -*- coding: utf-8 -*-
""" 
@file:      event.py
@time:      2024/7/10 上午2:34
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


# 遇到确定就点击
@task.page(name="确定操作", target_texts=["^确定$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^确定$")
    control.click(pos.x, pos.y)


@task.page(name="确认操作", target_texts=["^确认$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^确认$")
    control.click(pos.x, pos.y)


# 选择类，出现同类持有的选择事件，主要选择鸣徽或者邦布，诡术鸣徽(如果遇到的话)，优先级降低一级，避免与不可触碰之物冲突
@task.page(name="选择_鸣徽或邦布", priority=4, target_texts=["同类持有", "^选择$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^选择$")
    control.click(pos.x, pos.y)


@task.page(name="选择_不可触碰", target_texts=["同类持有", "^选择$", "不可触碰"])
def select_role():
    positions = get_pos("^选择$")
    for pos in positions:
        control.click(pos[0], pos[1])


# 离开类，所有需要离开的情况
@task.page(name="离开操作", target_texts=["^离开$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^离开$")
    control.click(pos.x, pos.y)


@task.page(name="目标位置", target_texts=["关键进展", "^确认继续$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^确认继续$")
    control.click(pos.x, pos.y)
    # 进入战斗


# 5、邦布商人
@task.page(name="邦布商人", target_texts=["^欢迎光临"])
def select_role():
    control.click(1210, 35)


# # 6、防卫军后勤站
# @task.page(name="防卫军后勤站", target_texts=["防卫军后勤站$", "^离开$"])
# def select_role(positions: Dict[str, Position]):
#     pos = positions.get("^离开$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


# @task.page(name="防卫军后勤站_对话", target_texts=["防卫军后勤站$"])
# def select_role():
#     # 点击对话
#     control.click(1000, 350)
#     time.sleep(2)


# # 8、资源回收小组
# @task.page(name="资源回收小组", target_texts=["^离开$"])
# def select_role(positions: Dict[str, Position]):
#     pos = positions.get("^离开$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


# 10、调查协会支援站
@task.page(name="调查协会支援站", target_texts=["协会支援站$", "^不用领取了$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^不用领取了$")
    control.click(pos.x, pos.y)


@task.page(name="调查协会支援站_狡兔屋", target_texts=["协会支援站$", "代理人"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("代理人")
    control.click(pos.x, pos.y)


# 56、馅饼天降, 埋伏加两次对话加鸣徽选择
@task.page(name="馅饼天降", target_texts=["^忍了"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^忍了")
    control.click(pos.x, pos.y)


# 11、呼叫增援，接应和入队分别处理，对话交给地图处理
# @task.page(name="呼叫增援_接应", target_texts=["呼叫增援", "^接应支援代理人$"])
# def select_role(positions: Dict[str, Position]):
#     pos = positions.get("^接应支援代理人$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)
#
#
# @task.page(name="呼叫增援_入队", target_texts=["呼叫增援", "^2号位$"])
# def select_role(positions: Dict[str, Position]):
#     pos = positions.get("^2号位$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


@task.page(name="呼叫增援_不增援", target_texts=["呼叫增援", "^接应支援代理人$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^接应支援代理人$")
    control.click(pos.x, pos.y + 70)


# 选择类
# @task.page(name="鸣徽_选择", target_texts=["同类持有", "^选择$"])
# def select_role(positions: Dict[str, Position]):
#     pos = positions.get("^选择$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


@task.page(name="催化", target_texts=["同类持有", "^催化$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^催化$")
    control.click(pos.x, pos.y)


# # 21、侵蚀扭蛋机
# @task.page(name="侵蚀扭蛋机", target_texts=["古怪装置", "^离开$"])
# def select_role(positions: Dict[str, Position]):
#     pos = positions.get("^离开$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


# # 118、助战邦布
# @task.page(name="助战邦布", target_texts=["^助战邦布$", "^选择$"])
# def select_role(positions: Dict[str, Position]):
#     pos = positions.get("^选择$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


# 下面为其他地图新增


# 投机客
@task.page(name="投机客", target_texts=["投机客", "^不需要借款$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^不需要借款$")
    control.click(pos.x, pos.y)


# 投机客的帮助，不确定是否选项固定，多写几个
@task.page(name="投机客_帮助_回复生命", target_texts=["投机客", "^恢复身体$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^恢复身体$")
    control.click(pos.x, pos.y)


@task.page(name="投机客_帮助_清除压力", target_texts=["投机客", "^清除压力$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^清除压力$")
    control.click(pos.x, pos.y)


# 坍塌的房屋
@task.page(name="坍塌的房屋", target_texts=["坍塌的房屋", "^从塌处离开$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^从塌处离开$")
    control.click(pos.x, pos.y)


# 精锐邦布助手
@task.page(name="精锐邦布助手", target_texts=["邦布助手", "^获得基础礼包$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^获得基础礼包$")
    control.click(pos.x, pos.y)


# 特殊区域 确认继续
@task.page(name="退出特殊区域", target_texts=["^确认继续$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^确认继续$")
    control.click(pos.x, pos.y)


# 降低压力值 回复生命值 获得齿轮硬币
@task.page(name="降低压力值", target_texts=["^获得齿轮硬币$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^获得齿轮硬币$")
    control.click(pos.x, pos.y)
