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
from utils.task import task, find_template
from PIL import Image
from re import template
from utils.map.components import set_weight
import utils
from utils.map.components import my_set_weight, my_unset_weight


def get_pos(text: str):
    text = template(text)
    img = screenshot()  # 截图
    ocr_Results = task.ocr(img)  # OCR识别
    positions = []
    for ocr_result in ocr_Results:
        if text.search(ocr_result.text):
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
    exclude_texts=["零号银行", "呼叫增援", "进入特殊区域"],
)
def action():
    # 如果上一个页面是地图层数，说明刚进区域，此时等待一秒加载图像，主要是防止特殊区域的问题
    if task.lastPageName == "地图层数":
        time.sleep(1)
        return
    # 模板匹配找到通用选择事件
    screen = screenshot()  # 截图
    if any(
        find_template(screen, option_image_match, threshold=0.95)
        for option_image_match in OptionImageMatch
    ):
        return
    # 1.1版本后对话新加数字选项，可以直接输入数字继续对话，通用点击进行调整
    # exclude_texts = ["特殊区域"]
    # exclude_texts = list(map(lambda x: template(x), exclude_texts))
    # results = task.ocr(screen)
    # if any(
    #     exclude_text.search(result.text)
    #     for exclude_text in exclude_texts
    #     for result in results
    # ):
    #     return
    # # 点击坐标，点击位置根据点击次数变化
    # control.click(1050, 320 + (info.clickCount % 9) * 40)
    # info.clickCount = (info.clickCount + 1) % 9

    # 1.1版本变动事件处理逻辑，取消鼠标点击，容易产生误判，好感事件选择第一个，特殊情况额外加判断
    control.press("1")  # 非特殊判断事件和通用选择事件，则大概率是好感选择
    control.press("space")  # 对话确认


# 遇到确定就点击
@task.page(name="确定操作", target_texts=["^确定$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^确定$")
    control.click(pos.x, pos.y)


@task.page(name="确认操作", target_texts=["^确认$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^确认$")
    control.click(pos.x, pos.y)


@task.page(name="丢弃操作", target_texts=["^丢弃$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^丢弃$")
    control.click(pos.x, pos.y)


# 清除侵蚀效果
@task.page(name="清除侵蚀效果", target_texts=["^清除$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^清除$")
    control.click(pos.x, pos.y)


@task.page(name="目标位置", target_texts=["关键进展", "^确认继续$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^确认继续$")
    control.click(pos.x, pos.y)
    # 进入战斗
    if utils.config.modeSelect == 1:
        info.currentStage = 5  # 向下拖拽
    elif utils.config.modeSelect == 2:
        info.currentStage = 1  # 左下拖
    elif utils.config.modeSelect == 3:
        info.currentStage = 2  # 右下拖
    elif utils.config.modeSelect == 4:
        info.currentStage = 2  # 向下拖拽


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
@task.page(name="呼叫增援_接应", target_texts=["呼叫增援", "^接应支援代理人$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^接应支援代理人$")
    control.click(pos.x, pos.y)
    info.teammate -= 1
    # 若已经召唤两个队友，则不再召唤队友
    if info.teammate == 0:
        set_weight("呼叫增援", 3)


@task.page(name="呼叫增援_入队", target_texts=["呼叫增援", "^2号位$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^2号位$")
    control.click(pos.x, pos.y)


@task.page(name="呼叫增援_对话", priority=4, target_texts=["^呼叫增援"])
def action():
    control.press("space", duration=0.1)


@task.page(name="催化", target_texts=["同类持有", "^催化$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^催化$")
    control.click(pos.x, pos.y)


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


@task.page(name="投机客_离开", target_texts=["投机客", "^离开$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^离开$")
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
@task.page(name="降低压力值", target_texts=["^降低压力值"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^降低压力值")
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


@task.page(name="邦布商人_鸣徽交易", target_texts=["^鸣徽交易", "^同类持有"])
def action():
    control.click(1210, 35)


@task.page(name="邦布商人_鸣徽催化", target_texts=["^鸣徽催化", "^可催化"])
def action():
    control.click(1210, 35)


@task.page(name="进入特殊区域", target_texts=["进入特殊区域"])
def action(screen: np.ndarray):
    special_areas = ["0044"]
    special_areas = list(map(lambda x: template(x), special_areas))
    ocr_results = task.ocr(screen)
    need_exit = False
    for ocr_result in ocr_results:
        if ocr_result.text.strip() == "离开":
            control.click(ocr_result.position.x, ocr_result.position.y)
            return  # 离开特殊区域
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


# 1.1版本移除判断
# # 怀斯塔学会的援助
# @task.page(name="怀斯塔学会的援助", target_texts=["^接受学会的好意$"])
# def action(positions: Dict[str, Position]):
#     pos = positions.get("^接受学会的好意$")
#     control.click(pos.x, pos.y)


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
@task.page(name="异化检疫门", target_texts=["异化", "^强行", "接受"])
def action(positions: Dict[str, Position]):
    pos = positions.get("接受")
    control.click(pos.x, pos.y)
    time.sleep(0.2)
    pos = positions.get("^强行")
    control.click(pos.x, pos.y)


# 抵押欠款
@task.page(name="抵押欠款", target_texts=["^抵押欠款$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^抵押欠款$")
    control.click(pos.x, pos.y)


# 助战邦布已满 请选择要交换的邦布
@task.page(name="助战邦布已满", target_texts=["^交换$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^交换$")
    control.click(pos.x, pos.y)


# 零号银行
@task.page(name="零号银行_存款", target_texts=["^存款$", "^零号银行$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^存款$")
    control.click(pos.x, pos.y)


@task.page(name="零号银行_存血", target_texts=["消耗10%生命值", "^零号银行$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("消耗10%生命值")
    control.click(pos.x, pos.y)


@task.page(
    name="零号银行_离开",
    priority=10,
    target_texts=["还可存款0次", "^零号银行$", "^离开$"],
)
def action(positions: Dict[str, Position]):
    pos = positions.get("^离开$")
    control.click(pos.x, pos.y)
    if utils.config.modeSelect == 4:
        my_set_weight()
        info.currentStage = 6
        time.sleep(0.5)
        for i in range(3):
            control.press("space")
        time.sleep(0.5)
        for i in range(3):
            control.press("d")
        control.press("s")
        for i in range(4):
            control.press("d")
    else:  # 模式3
        info.exitFlag = True  # 存完钱准备离开


@task.page(
    name="零号银行_离开",
    priority=10,
    target_texts=["还可存款0次", "^零号银行$", "^离开$"],
)
def action(positions: Dict[str, Position]):
    pos = positions.get("^离开$")
    control.click(pos.x, pos.y)
    my_set_weight()


@task.page(
    name="零号银行_不要了",
    priority=10,
    target_texts=["^不要了$"],
)
def action(positions: Dict[str, Position]):
    pos = positions.get("^不要了$")
    control.click(pos.x, pos.y)
    my_set_weight()


# 零号业绩
@task.page(name="零号业绩领取", target_texts=["^确认$", "业绩"], priority=10)
def action(positions: Dict[str, Position]):
    pos = positions.get("^确认$")
    control.click(pos.x, pos.y)
    info.exitFlag = True  # 拿完业绩准备离开
    if utils.config.modeSelect == 4:
        my_unset_weight()


@task.page("付费通道", target_texts=["^付费", "^打开", "^暂时离开$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^打开")
    control.click(pos.x, pos.y)
    pos = positions.get("^暂时离开$")
    control.click(pos.x, pos.y)


@task.page("全自动医疗仓", target_texts=["^全自动", "^启动", "^暂时离开$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^启动")
    control.click(pos.x, pos.y)
    pos = positions.get("^暂时离开$")
    control.click(pos.x, pos.y)


# 此区域曾为娱乐区
@task.page(name="娱乐区幸运拉杆", target_texts=["^拉一下$", "^离开$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^离开$")
    control.click(pos.x, pos.y)


# # 古怪装置
# @task.page(name="古怪装置", target_texts=["^离开$"])
# def action(positions: Dict[str, Position]):
#     pos = positions.get("^离开$")
#     control.click(pos.x, pos.y)


# 事件有偿休息站
@task.page(name="事件有偿休息站", target_texts=["不付费直接使用", "事件有偿休息站"])
def action(positions: Dict[str, Position]):
    pos = positions.get("不付费直接使用")
    control.click(pos.x, pos.y)


# 事件安全车箱特殊处理
@task.page(name="事件安全车箱特殊处理", target_texts=["搜刮此处齿轮硬币"])
def action(positions: Dict[str, Position]):
    pos = positions.get("搜刮此处齿轮硬币")
    control.click(pos.x, pos.y)
