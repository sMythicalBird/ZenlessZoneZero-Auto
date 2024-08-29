# -*- coding: utf-8 -*-
""" 
@file:      conditional.py
@time:      2024/8/30 上午2:20
@author:    sMythicalBird
"""
from utils.task import task
from utils.config import config
from utils import logger
from schema import info


@task.conditional(
    name="最大战斗次数",
    condition=lambda: config.maxFightCount
    and info.fightCount >= config.maxFightCount
    and info.currentPageName == "结算界面",
)
def max_fight_times():
    """
    达到最大战斗次数
    """
    logger.info(f"当前已达到最大战斗次数{config.maxFightCount}，停止战斗")
    task.stop()
