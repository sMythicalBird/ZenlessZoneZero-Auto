# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: option.py
@time: 2024/7/18 上午10:59
@author SuperLazyDog
"""
from typing import Dict

from schema import Position
from utils import control
from utils.task import task


@task.page(name="选项_红色风险", priority=2, target_image="option_red_risk.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_red_risk")
    control.click(pos.x, pos.y)


@task.page(name="选项_紫色风险", priority=2, target_image="option_purple_risk.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_purple_risk")
    control.click(pos.x, pos.y)


@task.page(name="选项_白色未知", priority=3, target_image="option_white_known.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_white_known")
    control.click(pos.x, pos.y)


@task.page(name="选项_蓝色打开", priority=3, target_image="option_blue_open.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_blue_open")
    control.click(pos.x, pos.y)


@task.page(name="选项_金色收益", priority=3, target_image="option_golden_benefit.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_golden_benefit")
    control.click(pos.x, pos.y)


@task.page(name="选项_蓝色收益", priority=3, target_image="option_blue_benefit.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_blue_benefit")
    control.click(pos.x, pos.y)


@task.page(name="选项_绿色收益", priority=3, target_image="option_green_benefit.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_green_benefit")
    control.click(pos.x, pos.y)


@task.page(name="选项_橙色插件", priority=3, target_image="option_orange_plugin.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_orange_plugin")
    control.click(pos.x, pos.y)


@task.page(name="选项_白色退出", priority=4, target_image="option_white_exit.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_white_exit")
    control.click(pos.x, pos.y)


@task.page(name="选项_绿色治疗", priority=4, target_image="option_green_treatment.png")
def action(positions: Dict[str, Position]):
    pos = positions.get("option_green_treatment")
    control.click(pos.x, pos.y)
