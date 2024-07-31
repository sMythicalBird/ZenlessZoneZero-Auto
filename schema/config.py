# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: config.py
@time: 2024/7/12 下午9:05
@author SuperLazyDog
"""
from typing import List

from pydantic import BaseModel, Field, model_validator

ZoneMap = {
    1: {
        "name": "旧都列车",
        "level": {1: "外围", 2: "前线", 3: "内部", 4: "腹地", 5: "核心"},
    },
    2: {
        "name": "施工废墟",
        "level": {1: "前线", 2: "内部", 3: "腹地", 4: "核心"},
    },
    3: {
        "name": "巨厦",
        "level": {1: "内部", 2: "腹地", 3: "核心"},
    },
}


class Tactic(BaseModel):
    key: str | None = Field(
        None,
        description="按下的按键，如果为None，则只延迟，鼠标操作时为left、right、middle",
    )
    type_: str | None = Field(None, description="技能类型", alias="type")
    duration: float | None = Field(None, description="按键持续时间（单位秒）", ge=0)
    delay: float | None = Field(None, description="按键间隔时间（单位秒）", ge=0)
    repeat: int = Field(1, description="重复操作次数", ge=1)

    def __init__(self, **data):
        # 如果设置了 key，但没有设置 duration 和 delay，则默认设置为 0.1
        if "key" in data and "duration" not in data:
            data["duration"] = 0.1
        if "key" in data and "delay" not in data:
            data["delay"] = 0.1
        # 如果设置了ket，但是没有设置type，则默认设置为press
        if "key" in data and "type" not in data and "type_" not in data:
            data["type"] = "press"
        super().__init__(**data)

    # 检查 type_ 是否合法
    @model_validator(mode="after")
    def check_type(self):
        if self.type_ not in ["press", "down", "up"] and self.key is not None:
            raise ValueError(
                f"Invalid type: {self.type_}, must be one of ['press', 'down', 'up']"
            )


class TargetMap(BaseModel):
    zone: int = Field(1, ge=1, le=3)
    level: int = Field(1, ge=1, le=5)

    @property
    def Zone(self):
        return ZoneMap[self.zone]["name"]

    @property
    def Level(self):
        return ZoneMap[self.zone]["level"][self.level]


class Config(BaseModel):
    targetMap: TargetMap = Field(TargetMap())
    modeSelect: int = Field(2, description="模式选择")
    maxFightTime: int = Field(200, description="最大战斗时间（单位秒）")
    maxMapTime: int = Field(25 * 60, description="在地图内最大时间（单位秒）")
    hasBoom: bool = Field(False, description="是否有炸弹")
    useGpu: bool = Field(True, description="是否使用GPU")
    selBuff: List[str] = Field(["冻结", "暴击", "决斗", "闪避"], description="选择buff")
    characters: List[str] = Field(["艾莲", "莱卡恩", "苍角", "朱鸢", "安比", "妮可", "格莉丝"], description="角色池，用于载入角色战斗模块，空则载入默认战斗模块")
