# -*- coding: utf-8 -*-
""" 
@file:      option.py
@time:      2024/8/30 上午2:17
@author:    sMythicalBird
"""
from typing import Dict
from schema import Position
from utils import control
from utils.task import ImageMatch
from utils.task import task_zero as task
from pathlib import Path

opt_img_path = Path(__file__).parent.parent.parent / "resources/img/pic_1080x720/zero"


# 增加邦布商人等事件的红叉选择
@task.page(
    name="红叉离开事件",
    priority=5,
    target_image=ImageMatch(image=opt_img_path / "red_exit.png", confidence=0.9),
)
def action(positions: Dict[str, Position]):
    pos = positions.get("red_exit")
    control.click(pos.x, pos.y)


@task.page(
    name="选项_红色风险", priority=2, target_image=opt_img_path / "option_red_risk.png"
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_red_risk")
    control.click(pos.x, pos.y)


@task.page(
    name="选项_紫色风险",
    priority=2,
    target_image=opt_img_path / "option_purple_risk.png",
    exclude_texts=["进入商店"],
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_purple_risk")
    control.click(pos.x, pos.y)


@task.page(
    name="选项_白色未知",
    priority=3,
    target_image=opt_img_path / "option_white_known.png",
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_white_known")
    control.click(pos.x, pos.y)


@task.page(
    name="选项_蓝色打开", priority=3, target_image=opt_img_path / "option_blue_open.png"
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_blue_open")
    control.click(pos.x, pos.y)


# 由于现在不会购买东西，所有金币收益很低
@task.page(
    name="选项_金色收益",
    priority=2,
    target_image=opt_img_path / "option_golden_benefit.png",
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_golden_benefit")
    control.click(pos.x, pos.y)


@task.page(
    name="选项_蓝色收益",
    priority=3,
    target_image=ImageMatch(
        image=opt_img_path / "option_blue_benefit.png", confidence=0.9
    ),
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_blue_benefit")
    control.click(pos.x, pos.y)


@task.page(
    name="选项_绿色收益",
    priority=3,
    target_image=opt_img_path / "option_green_benefit.png",
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_green_benefit")
    control.click(pos.x, pos.y)


@task.page(
    name="选项_橙色插件",
    priority=3,
    target_image=opt_img_path / "option_orange_plugin.png",
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_orange_plugin")
    control.click(pos.x, pos.y)


@task.page(
    name="选项_白色退出",
    priority=4,
    target_image=opt_img_path / "option_white_exit.png",
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_white_exit")
    control.click(pos.x, pos.y)


@task.page(
    name="选项_绿色治疗",
    priority=4,
    target_image=opt_img_path / "option_green_treatment.png",
)
def action(positions: Dict[str, Position]):
    pos = positions.get("option_green_treatment")
    control.click(pos.x, pos.y)
