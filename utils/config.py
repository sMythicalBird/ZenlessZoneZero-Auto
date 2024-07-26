# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: config.py
@time: 2024/7/12 下午9:09
@author SuperLazyDog
"""
from typing import List

from yaml import safe_load, safe_dump
from schema.config import Config, Tactic
from .init import RootPath, logger


config_path = RootPath / "config.yaml"
logger.info(f"加载配置文件 {config_path}")
# 判断配置文件是否存在
if not config_path.exists():
    logger.error(f"config.yaml 未在 {config_path} 发现")
    with open(config_path, "w", encoding="utf-8") as f:
        safe_dump(Config().model_dump(), f)
    # logger.error(f"请参照 config.example.yaml 修改配置")
    # exit(1)
    logger.info(f"已生成默认配置文件 config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    config: dict = safe_load(f)

config: Config = Config(**config)
logger.info(f"配置文件加载成功")


tactics_path = RootPath / "tactics.yaml"
logger.info(f"加载战斗策略文件 {tactics_path}")
# 判断配置文件是否存在
if not tactics_path.exists():
    logger.error(f"tactics.yaml 未在 {tactics_path} 发现")
    with open(tactics_path, "w", encoding="utf-8") as f:
        safe_dump([], f)
    logger.error(f"请参照 tactics.example.yaml 修改配置")
    exit(1)
with open(tactics_path, "r", encoding="utf-8") as f:
    fightTactics: List[dict] = safe_load(f)

fightTactics: List[Tactic] = [Tactic(**item) for item in fightTactics]

if not fightTactics:
    logger.error(f"战斗策略为空，请检查战斗策略文件 {tactics_path}")
    exit(1)
