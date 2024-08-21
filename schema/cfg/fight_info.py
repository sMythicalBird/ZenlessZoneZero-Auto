# -*- coding: utf-8 -*-
"""
@file:      fight_info
@time:      2024/8/21 23:32
@author:    sMythicalBird
"""

from typing import List
from pydantic import BaseModel, Field, model_validator


class LogicInfo(BaseModel):
    char: str = Field("艾莲", description="角色")
    logic: str = Field("默认逻辑", description="逻辑")


class EventInfo(BaseModel):
    first: LogicInfo = Field(
        LogicInfo(char="艾莲", logic="默认逻辑"), description="首次"
    )
    second: LogicInfo = Field(
        LogicInfo(char="莱卡恩", logic="默认逻辑"), description="首次"
    )
    third: LogicInfo = Field(
        LogicInfo(char="苍角", logic="默认逻辑"), description="首次"
    )


class FightConfig(BaseModel):
    zero_fight: EventInfo = Field(EventInfo(), description="零号战斗配置")
    daily_fight: EventInfo = Field(EventInfo(), description="日常战斗配置")
