# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 上午9:28
# @Author  : zidianzhimeng
# @FileName: conditional.py
from utils.task import task
from utils.config import config
from utils import logger
from schema import info


# 条件任务 - 最大战斗次数
# 当战斗次数达到最大战斗次数时，停止战斗
# 装饰器 conditional 用于定义条件任务
# 参数 name 为任务名称
# 参数 condition 为条件函数，返回 True 时执行任务
# 示例中使用了 lambda 表达式定义条件函数
# 任务函数无需参数，无需返回值
@task.conditional(
    name="最大战斗次数",
    condition=lambda: config.maxFightCount and info.fightCount >= config.maxFightCount and info.currentPageName == '结算界面',
)
def max_fight_times():
    """
    达到最大战斗次数
    """
    logger.info(f"当前已达到最大战斗次数{config.maxFightCount}，停止战斗")
    task.stop()