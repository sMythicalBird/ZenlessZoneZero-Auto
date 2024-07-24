# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: config.py
@time: 2024/7/12 下午9:09
@author SuperLazyDog
"""
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
fightTactics = config.pop("fightTactics")
fightTactics = [Tactic(**item) for item in fightTactics]
config: Config = Config(**config)
config.fightTactics = fightTactics
if not config.fightTactics:
    logger.error(f"战斗策略为空，请检查配置文件")
    exit(1)
logger.info(f"配置文件加载成功")
