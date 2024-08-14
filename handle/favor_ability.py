# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: favor_ability.py
@time: 2024/7/18 下午6:11
@author SuperLazyDog
"""
from typing import Dict
from schema import Position
from utils import control
from utils.task import task


# 好感度系列
@task.page(name="好感度_艾莲1", target_texts=["那休息一会儿$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("那休息一会儿$")
    control.click(pos.x, pos.y)


@task.page(name="好感度_艾莲2", target_texts=["休息长一点也是为了更好地工作$", "醒醒"])
def action(positions: Dict[str, Position]):
    pos = positions.get("醒醒")
    control.click(pos.x, pos.y)


@task.page(name="好感度_猫又1", target_texts=["捕猎游戏", "^出发寻找猫又$"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^出发寻找猫又$")
    control.click(pos.x, pos.y)


@task.page(name="好感度_猫又2", target_texts=["捕猎游戏", "等待猫"])
def action(positions: Dict[str, Position]):
    pos = positions.get("等待猫")
    control.click(pos.x, pos.y)


@task.page(name="好感度_格莉丝1", target_texts=["^心灵充电$", "^下不为例"])
def action(positions: Dict[str, Position]):
    pos = positions.get("^下不为例")
    control.click(pos.x, pos.y)


# 8、资源回收小组，特殊判断
@task.page(name="资源回收小组", target_texts=["^让猫又选物资箱$"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("^让猫又选物资箱$")
    control.click(pos.x, pos.y)
