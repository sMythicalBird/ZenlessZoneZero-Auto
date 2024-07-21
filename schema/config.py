# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: config.py
@time: 2024/7/12 下午9:05
@author SuperLazyDog
"""
from pydantic import BaseModel, Field
from enum import Enum

ZoneMap = {
    1: {
        "name": "旧都列车",
        "level": {1: "外围", 2: "前线", 3: "内部", 4: "腹地", 5: "核心"},
    },
    2: {
        "name": "施工废墟",
        "level": {1: "前线", 2: "内部", 3: "腹地", 4: "核心"},
    },
}


class TargetMap(BaseModel):
    zone: int = Field(1, ge=1, le=2)
    level: int = Field(1, ge=1, le=5)

    @property
    def Zone(self):
        return ZoneMap[self.zone]["name"]

    @property
    def Level(self):
        return ZoneMap[self.zone]["level"][self.level]


class Config(BaseModel):
    targetMap: TargetMap = Field(TargetMap())
    wholeCourse: bool = Field(False, description="是否打完全程")
    maxFightTime: int = Field(150, description="最大战斗时间（单位秒）")
    maxMapTime: int = Field(15 * 60, description="在地图内最大时间（单位秒）")
    useGpu: bool = Field(True, description="是否使用GPU")
