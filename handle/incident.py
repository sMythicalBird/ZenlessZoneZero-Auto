# -*- coding: utf-8 -*-
""" 
@file:      event.py
@time:      2024/7/10 上午2:34
@author:    sMythicalBird
"""
import time
from typing import Dict

import numpy as np

from schema import Position, info
from utils import control, screenshot, logger, RootPath
from pathlib import Path
from utils.task import task, ImageMatch, find_template
from PIL import Image
from re import template
from utils import config


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


DownloadPath: Path = RootPath / "download"
OptionImgPath = [
    image_path
    for image_path in DownloadPath.glob("*.png")
    if "option" in image_path.stem or image_path.stem == "red_exit"
]
OptionImageMatch = [np.array(Image.open(image_path)) for image_path in OptionImgPath]


# 通用事件点击 优先级最低
@task.page(
    name="通用点击事件",
    priority=1,
    target_texts=["背包", "^当前层数"],
    target_image="tv_spot.png",
)
def action():
    time.sleep(1)
    screen = screenshot()  # 截图
    if any(
        find_template(screen, option_image_match)
        for option_image_match in OptionImageMatch
    ):
        return
    exclude_texts = ["特殊区域"]
    exclude_texts = list(map(lambda x: template(x), exclude_texts))
    results = task.ocr(screen)
    if any(
        exclude_text.search(result.text)
        for exclude_text in exclude_texts
        for result in results
    ):
        return
    for y in range(640, 319, -40):
        control.click(1050, y)
        time.sleep(0.1)


# 遇到确定就点击
@task.page(name="确定操作", target_texts=["^确定$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^确定$")
    control.click(pos.x, pos.y)


@task.page(name="确认操作", target_texts=["^确认$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^确认$")
    control.click(pos.x, pos.y)


# 清除侵蚀效果
@task.page(name="清楚侵蚀效果", target_texts=["^清除$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^清除$")
    control.click(pos.x, pos.y)


# 选择类，出现同类持有的选择事件，主要选择鸣徽或者邦布，诡术鸣徽(如果遇到的话)，优先级降低一级，避免与不可触碰之物冲突
@task.page(name="选择_鸣徽或邦布", priority=4, target_texts=["同类持有", "^选择$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^选择$")
    control.click(pos.x, pos.y)


@task.page(name="选择_不可触碰", target_texts=["同类持有", "^选择$", "不可触碰"])
def action():
    positions = get_pos("^选择$")
    for pos in positions:
        control.click(pos[0], pos[1])


# 离开类，所有需要离开的情况
@task.page(name="离开操作", target_texts=["^离开$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^离开$")
    control.click(pos.x, pos.y)


@task.page(name="目标位置", target_texts=["关键进展", "^确认继续$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^确认继续$")
    info.currentStage = 1
    control.click(pos.x, pos.y)
    # 进入战斗


# 5、邦布商人
@task.page(name="邦布商人", target_texts=["^鸣徽交易$"])
def action():
    control.click(1210, 35)


# @task.page(name="邦布商人", target_texts=["^鸣徽催化$"])
# def action():
#     control.click(1210, 35)


# # 6、防卫军后勤站
# @task.page(name="防卫军后勤站", target_texts=["防卫军后勤站$", "^离开$"])
# def action(positions: Dict[str, Position]):
#     pos = positions.get("^离开$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


# @task.page(name="防卫军后勤站_对话", target_texts=["防卫军后勤站$"])
# def action():
#     # 点击对话
#     control.click(1000, 350)
#     time.sleep(2)


# 8、资源回收小组
@task.page(name="资源回收小组", target_texts=["^让猫又选物资箱$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^让猫又选物资箱$")
    control.click(pos.x, pos.y)
    time.sleep(2)


# 10、调查协会支援站
@task.page(name="调查协会支援站", target_texts=["协会支援站$", "^不用领取了$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^不用领取了$")
    control.click(pos.x, pos.y)


@task.page(name="调查协会支援站_狡兔屋", target_texts=["协会支援站$", "代理人"])
def action(positions: Dict[str, Position]):
    pos = positions.get("代理人")
    control.click(pos.x, pos.y)


# 56、馅饼天降, 埋伏加两次对话加鸣徽选择
@task.page(name="馅饼天降", target_texts=["^忍了"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^忍了")
    control.click(pos.x, pos.y)


# 11、呼叫增援，接应和入队分别处理，对话交给地图处理
# @task.page(name="呼叫增援_接应", target_texts=["呼叫增援", "^接应支援代理人$"])
# def action(positions: Dict[str, Position]):
#     pos = positions.get("^接应支援代理人$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)
#
#
# @task.page(name="呼叫增援_入队", target_texts=["呼叫增援", "^2号位$"])
# def action(positions: Dict[str, Position]):
#     pos = positions.get("^2号位$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


@task.page(name="呼叫增援_不增援", target_texts=["呼叫增援", "^接应支援代理人$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^接应支援代理人$")
    control.click(pos.x, pos.y + 70)


# 选择类
# @task.page(name="鸣徽_选择", target_texts=["同类持有", "^选择$"])
# def action(positions: Dict[str, Position]):
#     pos = positions.get("^选择$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


@task.page(name="催化", target_texts=["同类持有", "^催化$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^催化$")
    control.click(pos.x, pos.y)


# # 21、侵蚀扭蛋机
# @task.page(name="侵蚀扭蛋机", target_texts=["古怪装置", "^离开$"])
# def action(positions: Dict[str, Position]):
#     pos = positions.get("^离开$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


# # 118、助战邦布
# @task.page(name="助战邦布", target_texts=["^助战邦布$", "^选择$"])
# def action(positions: Dict[str, Position]):
#     pos = positions.get("^选择$")
#     control.click(pos.x, pos.y)
#     time.sleep(2)


# 下面为其他地图新增


# 投机客
@task.page(name="投机客", target_texts=["投机客", "^不需要借款$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^不需要借款$")
    control.click(pos.x, pos.y)


# 投机客的帮助，不确定是否选项固定，多写几个
@task.page(name="投机客_帮助_回复生命", target_texts=["投机客", "^恢复身体$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^恢复身体$")
    control.click(pos.x, pos.y)


@task.page(name="投机客_帮助_清除压力", target_texts=["投机客", "^清除压力$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^清除压力$")
    control.click(pos.x, pos.y)


# 坍塌的房屋
@task.page(name="坍塌的房屋", target_texts=["坍塌的房屋", "^从塌处离开$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^从塌处离开$")
    control.click(pos.x, pos.y)


# 精锐邦布助手
@task.page(name="精锐邦布助手", target_texts=["邦布助手", "^获得基础礼包$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^获得基础礼包$")
    control.click(pos.x, pos.y)


# 特殊区域 确认继续
@task.page(name="退出特殊区域", target_texts=["^确认继续$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^确认继续$")
    control.click(pos.x, pos.y)


# 降低压力值 回复生命值 获得齿轮硬币
@task.page(name="降低压力值", target_texts=["^获得齿轮硬币$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^获得齿轮硬币$")
    control.click(pos.x, pos.y)


# 不感兴趣 离开这里
@task.page(name="不感兴趣", target_texts=["^不感兴趣$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^不感兴趣$")
    control.click(pos.x, pos.y)


# 假面研究者
@task.page(name="假面研究者", target_texts=["^拒绝他的好意$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^拒绝他的好意$")
    control.click(pos.x, pos.y)


@task.page(name="假面研究者_物资", target_texts=["^拿点侵蚀物资$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^拿点侵蚀物资$")
    control.click(pos.x, pos.y)


@task.page(name="假面研究者_降压", target_texts=["^做好降压准备$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^做好降压准备$")
    control.click(pos.x, pos.y)


@task.page(name="假面研究者_催化", target_texts=["^帮我催化催化"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^帮我催化催化")
    control.click(pos.x, pos.y)


@task.page(name="零号业绩领取", target_texts=["^确认$", "业绩"], priority=10)
def action(positions: Dict[str, Position]):
    pos = positions.get("^确认$")
    control.click(pos.x, pos.y)
    info.currentStage = 2
    if not config.wholeCourse:
        time.sleep(1)
        control.esc()


@task.page(name="邦布商人_鸣徽交易", target_texts=["^鸣徽交易", "^同类持有"])
def action():
    control.click(1210, 35)


@task.page(name="邦布商人_鸣徽催化", target_texts=["^鸣徽催化", "^可催化"])
def action():
    control.click(1210, 35)


@task.page(name="进入特殊区域", target_texts=["特殊区域"])
def action(screen: np.ndarray):
    special_areas = ["0044"]
    special_areas = list(map(lambda x: template(x), special_areas))
    ocr_results = task.ocr(screen)
    need_exit = False
    for ocr_result in ocr_results:
        for special_area in special_areas:
            if special_area.search(ocr_result.text):
                need_exit = True
                break
        if need_exit:
            break
    if need_exit:
        logger.info("进入特殊区域,且该特殊区域无法寻路，退出地图")
        for i in range(10):
            control.press("space")
            time.sleep(0.2)
        time.sleep(3)
        control.esc()
    else:
        logger.debug("进入特殊区域")
    control.press("space")


# 旧都往事系列
@task.page(name="旧都往事系列收集品", target_texts=["^收录至工作台$"])
def action():
    control.click(80, 35)


# 怀斯塔学会的援助
@task.page(name="怀斯塔学会的援助", target_texts=["^接受学会的好意$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^接受学会的好意$")
    control.click(pos.x, pos.y)


# 老练的调查员
@task.page(name="老练的调查员", target_texts=["老练的调查员", "不用了"])
def action(positions: Dict[str, Position]):
    pos = positions.get("不用了")
    control.click(pos.x, pos.y)


# 治安局预备队
@task.page(name="治安局预备队", target_texts=["治安局预备队", "^只要绝对安全的物资$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^只要绝对安全的物资$")
    control.click(pos.x, pos.y)


# 邦布的秘宝
@task.page(name="邦布的秘宝", target_texts=["邦布的秘宝", "^人为财死"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^人为财死")
    control.click(pos.x, pos.y)


# 异化检疫门
@task.page(name="异化检疫门", target_texts=["异化检疫门", "^强行闯入"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^强行闯入")
    control.click(pos.x, pos.y)
