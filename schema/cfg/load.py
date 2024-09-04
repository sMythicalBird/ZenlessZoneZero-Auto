# -*- coding: utf-8 -*-
"""
@file:      load
@time:      2024/8/21 00:36
@author:    sMythicalBird
"""
import os
from typing import List

import numpy as np
import yaml
from PIL import Image
from yaml import safe_load, safe_dump
from loguru import logger
from pathlib import Path
from .fight_info import TacticsConfig, Tactic, TacticList

InfoPath = Path(__file__).parent.parent / "yaml"
FightPath = (
    Path(__file__).parent.parent.parent / "resources/fight_logic/char_logic_group"
)
FightDefaultPath = Path(__file__).parent.parent.parent / "resources/fight_logic/default"
DiyPath = Path(__file__).parent.parent.parent / "resources/fight_logic/diy"
default_path = (
    Path(__file__).parent.parent.parent / "resources/fight_logic/default"
)  # 默认战斗逻辑路径
char_img_path = Path(__file__).parent.parent.parent / "resources/img/pic_1080x720/char"


# 读取配置文件
def load_config(data_path: str, config: type):
    """
    加载系统配置
    """
    os.makedirs(InfoPath, exist_ok=True)
    config_path = InfoPath / data_path
    logger.info(f"加载配置文件 {data_path}")
    # 判断配置文件是否存在,不存在则生成默认配置文件
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


# 检查目录
def count_yaml_files_in_directory(path):
    """
    检查路径下是否存在需要的文件夹，不存在则创建，返回该路径下的文件数量
    """
    if not path.exists():
        os.makedirs(path)
        return 0
    yaml_file_count = len(list(path.glob("*.yaml")))
    return yaml_file_count


# 保存diy设计文件
def save_diy(char_name: str, tactic_logic):
    save_dir = DiyPath / char_name / "test"
    save_file_cnt = count_yaml_files_in_directory(save_dir) + 1
    save_path = save_dir / f"{save_file_cnt}.yaml"
    logger.info(f"保存配置逻辑 {save_path}")
    with open(save_path, "w", encoding="utf-8") as f:
        yaml.dump(tactic_logic, f, allow_unicode=True, default_flow_style=False)
    logger.info(f"配置逻辑 {save_path} 保存成功")


# 加载个角色对应的战斗目录
def get_fight_logic(char_list):
    # 获取所有子目录的名称
    fight_logic_dict = {}
    for each in char_list:
        char_logic_path = FightPath / each
        if not char_logic_path.exists():
            os.makedirs(char_logic_path)
        fight_logic_dict[each] = {
            "path": char_logic_path,
            "logic_dir": [d.name for d in char_logic_path.iterdir() if d.is_dir()],
        }
        fight_logic_dict[each]["logic_dir"].append("默认逻辑")

    return fight_logic_dict


def get_logic_path(fight_info, fight_logic_all):
    logic_path_dic = {}
    if fight_info.first.logic == "默认逻辑":
        logic_path_dic[fight_info.first.char] = default_path / "默认逻辑"
    else:
        logic_path_dic[fight_info.first.char] = (
            fight_logic_all[fight_info.first.char]["path"] / fight_info.first.logic
        )
    if fight_info.second.logic == "默认逻辑":
        logic_path_dic[fight_info.second.char] = default_path / "默认逻辑"
    else:
        logic_path_dic[fight_info.second.char] = (
            fight_logic_all[fight_info.second.char]["path"] / fight_info.second.logic
        )
    if fight_info.third.logic == "默认逻辑":
        logic_path_dic[fight_info.third.char] = default_path / "默认逻辑"
    else:
        logic_path_dic[fight_info.third.char] = (
            fight_logic_all[fight_info.third.char]["path"] / fight_info.third.logic
        )
    return logic_path_dic


def load_tactics(fight_info, fight_logic_all):
    """
    加载战斗逻辑和角色图像
    """
    logic_path_list = get_logic_path(fight_info, fight_logic_all)
    tactic_cfg = TacticsConfig()
    for char, path in logic_path_list.items():
        tactic_list = TacticList()
        for yaml_file in path.glob("*.yaml"):
            with open(yaml_file, "r", encoding="utf-8") as f:
                fight_tactics: List[dict] = safe_load(f)
            tactic_list.tac_list.append([Tactic(**item) for item in fight_tactics])
        tactic_cfg.tactics[char] = tactic_list
        tactic_cfg.char_icons[char] = np.array(
            Image.open(char_img_path / f"{char}.png")
        )
    # 获取红黄光和连携
    for yaml_file in default_path.glob("*.yaml"):
        tactic_list = TacticList()
        yaml_name = yaml_file.name.split(".")[0]
        with open(yaml_file, "r", encoding="utf-8") as f:
            fight_tactics: List[dict] = safe_load(f)
        tactic_list.tac_list.append([Tactic(**item) for item in fight_tactics])
        tactic_cfg.tactics[yaml_name] = tactic_list

    return tactic_cfg
