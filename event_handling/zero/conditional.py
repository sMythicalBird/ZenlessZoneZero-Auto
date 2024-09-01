# -*- coding: utf-8 -*-
""" 
@file:      conditional.py
@time:      2024/8/30 上午2:20
@author:    sMythicalBird
"""
from utils.task import task_zero as task
from utils import logger
from schema.cfg.info import zero_cfg
from schema.cfg.zero_info import state_zero


@task.conditional(
    name="最大战斗次数",
    condition=lambda: zero_cfg.maxFightCount
    and state_zero.fightCount >= zero_cfg.maxFightCount
    and state_zero.currentPageName == "结算界面",
)
def max_fight_times():
    """
    达到最大战斗次数
    """
    logger.info(f"当前已达到最大战斗次数{zero_cfg.maxFightCount}，停止战斗")
    task.stop()
