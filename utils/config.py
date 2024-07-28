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

import cv2
import os
import shutil

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


tactics_dir = RootPath / "tactics"
fightTacticsDict = {}
if not tactics_dir.exists() or len(tactics_dir.glob("*.yaml"))==0:
    logger.info(f"未检测到 {tactics_dir} 目录，请在 {tactics_dir} 目录下添加战斗策略文件")
    tactics_dir = RootPath / "tactics_defaults"
    logger.info(f"将使用 {tactics_dir} 默认目录加载战斗策略文件")

for yaml_file in tactics_dir.glob("*.yaml"):
    logger.info(f"加载战斗策略文件 {yaml_file}")
    with open(yaml_file, "r", encoding="utf-8") as f:
        fightTactics: List[dict] = safe_load(f)
    if not fightTactics:
        logger.error(f"战斗策略为空，请检查战斗策略文件 {yaml_file}")
        continue
    fightTactics: List[Tactic] = [Tactic(**item) for item in fightTactics]
    fightTacticsDict[yaml_file.stem] = fightTactics


character_dir = RootPath / "download" / "characters"
tmp_file = character_dir / "tmp.png"
logger.info(f"加载人物头像 {character_dir}")
if not character_dir.exists():
    os.makedirs(character_dir)
characters = {}
for chara in config.characters:
    png_file = character_dir / f"{chara}.png"
    if not png_file.exists():
        logger.info(f"暂不支持{chara}战斗模块")
        continue
    shutil.copy(png_file, tmp_file)
    image = cv2.imread(str(tmp_file), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"加载头像文件失败: {png_file}")
    characters[chara] = image
os.remove(tmp_file)
