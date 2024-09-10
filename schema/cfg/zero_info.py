# -*- coding: utf-8 -*-
"""
@file:      zero_info
@time:      2024/8/20 23:49
@author:    sMythicalBird
"""
from typing import List
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
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

    def reward_count(self):
        if self.zone == 1 and self.level < 3:
            return 1
        elif self.zone == 2 and self.level == 1:
            return 1
        else:
            return 2


class ZeroConfig(BaseModel):
    targetMap: TargetMap = Field(TargetMap())
    modeSelect: int = Field(1, description="模式选择")
    maxFightTime: int = Field(200, description="最大战斗时间（单位秒）")
    maxMapTime: int = Field(25 * 60, description="在地图内最大时间（单位秒）")
    hasBoom: bool = Field(False, description="是否有炸弹")
    useGpu: bool = Field(False, description="是否使用GPU")
    selBuff: List[str] = Field(["冻结", "暴击", "决斗", "闪避"], description="选择buff")
    maxFightCount: int = Field(10000, description="最大战斗次数")
    teamMates: int = Field(2, description="队友数量")
    carry: dict = Field({"char":'默认',"point":3000}, description="主C（放终结技的角色）")

class Dirct(Enum):
    up = "w"
    down = "s"
    left = "a"
    right = "d"

    def __str__(self):
        return self.value


class StatusInfo(BaseModel):
    currentPageName: str = Field("", title="当前页面名称")
    lastMoveTime: datetime = Field(datetime.now(), title="上次移动时间")
    fightCount: int = Field(0, description="战斗次数记录")
    entryMapTime: datetime = Field(datetime.now(), title="进入地图时间")
    currentStage: int = Field(
        0, title="当前阶段"
    )  # 0、无偏移     1、左下        2、右下         5、下          6、左
    hasBoom: bool = Field(True, title="是否有炸弹")
    exitFlag: bool = Field(False, title="是否退出")
    clickCount: int = Field(0, title="点击次数")
    teamMate: int = Field(2, title="队友数量")
    rewardCount: int = Field(0, title="奖励次数")
    stage2Count: int = Field(0, title="向业绩移动的情况")
    stage1flag: int = Field(0, title="是否在第一阶段")


state_zero = StatusInfo()
