# -*- coding: utf-8 -*-
"""
@file:      load
@time:      2024/8/21 00:36
@author:    sMythicalBird
"""
import os
from typing import List

import numpy as np
from PIL import Image
from yaml import safe_load, safe_dump
from loguru import logger
from pathlib import Path

InfoPath = Path(__file__).parent.parent / "yaml"
FightPath = (
    Path(__file__).parent.parent.parent / "resources/fight_logic/char_logic_group"
)
FightDefaultPath = Path(__file__).parent.parent.parent / "resources/fight_logic/default"


# 读取配置文件
def load_config(data_path: str, config: type):
    """
    加载系统配置
    """
    config_path = InfoPath / data_path
    logger.info(f"加载配置文件 {data_path}")
    # 判断配置文件是否存在
    if not config_path.exists():
        logger.error(f"{data_path} 未在 {config_path} 发现")
        with open(config_path, "w", encoding="utf-8") as f:
            safe_dump(config().model_dump(), f, allow_unicode=True)
        logger.info(f"已生成默认配置文件 config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config_temp: dict = safe_load(f)

    config_temp: config = config(**config_temp)
    logger.info(f"配置文件 {data_path} 加载成功")
    return config_temp


# 保存配置文件
def save_config(save_path: str, config):
    """
    保存系统配置
    """
    config_path = InfoPath / save_path
    logger.info(f"保存配置文件 {save_path}")
    with open(config_path, "w", encoding="utf-8") as f:
        safe_dump(config.model_dump(), f, allow_unicode=True)
    logger.info(f"配置文件 {save_path} 保存成功")


# 加载个角色对应的战斗目录
def get_fight_logic():
    # 获取所有子目录的名称
    subdirectories = [d.name for d in FightPath.iterdir() if d.is_dir()]
    fight_logic_dict = {}
    for each in subdirectories:
        subdir = FightPath / each
        fight_logic_dict[each] = {
            "path": subdir,
            "logic_dir": [d.name for d in subdir.iterdir() if d.is_dir()],
        }
        fight_logic_dict[each]["logic_dir"].append("默认逻辑")

    return fight_logic_dict


def load_tactics():
    """
    加载战斗逻辑
    """
    fightTacticsDictTemp = {}
    tactics_dir = RootPath / "fight/tactics"
    if not tactics_dir.exists() or len(list(tactics_dir.glob("*.yaml"))) == 0:
        logger.info(
            f"未检测到 {tactics_dir} 目录，请在 {tactics_dir} 目录下添加战斗策略文件"
        )
        tactics_dir = RootPath / "fight/tactics_defaults"
        logger.info(f"将使用 {tactics_dir} 默认目录加载战斗策略文件")

    for yaml_file in tactics_dir.glob("*.yaml"):
        logger.info(f"加载战斗策略文件 {yaml_file}")
        with open(yaml_file, "r", encoding="utf-8") as f:
            fightTactics: List[dict] = safe_load(f)
        if not fightTactics:
            logger.error(f"战斗策略为空，请检查战斗策略文件 {yaml_file}")
            continue
        fightTactics: List[Tactic] = [Tactic(**item) for item in fightTactics]
        fightTacticsDictTemp[yaml_file.stem] = fightTactics
    return fightTacticsDictTemp


def load_characters():
    """
    加载角色头像进行模板匹配
    """
    characterIconsTemp = {}
    character_dir = RootPath / "fight/characters"
    logger.info(f"加载人物头像 {character_dir}")
    if not character_dir.exists():
        os.makedirs(character_dir)
    # 读取配置文件角色头像
    for chara in config.characters:
        png_file = character_dir / f"{chara}.png"
        if not png_file.exists():  # 不存在使用默认配置
            logger.info(f"暂不支持{chara}战斗模块")
            continue
        image = np.array(Image.open(png_file))
        characterIconsTemp[chara] = image
    return characterIconsTemp


print("Executing utils module")
# config = load_config()
# fightTacticsDict = load_tactics()
# characterIcons = load_characters()
