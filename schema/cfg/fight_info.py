# -*- coding: utf-8 -*-
"""
@file:      fight_info
@time:      2024/8/21 23:32
@author:    sMythicalBird
"""

from typing import List
from pydantic import BaseModel, Field, model_validator
from pathlib import Path


class LogicInfo(BaseModel):
    char: str = Field("艾莲", description="角色")
    logic: str = Field("默认逻辑", description="逻辑")


class EventInfo(BaseModel):
    first: LogicInfo = Field(
        LogicInfo(char="艾莲", logic="默认逻辑"), description="1号位"
    )
    second: LogicInfo = Field(
        LogicInfo(char="莱卡恩", logic="默认逻辑"), description="2号位"
    )
    third: LogicInfo = Field(
        LogicInfo(char="苍角", logic="默认逻辑"), description="3号位"
    )


class FightConfig(BaseModel):
    zero_fight: EventInfo = Field(EventInfo(), description="零号战斗配置")
    daily_fight: EventInfo = Field(EventInfo(), description="日常战斗配置")


# 战斗逻辑配置参数
class Tactic(BaseModel):
    key: str | None = Field(
        None,
        description="按下的按键，如果为None，则只延迟，鼠标操作时为left、right、middle",
    )
    type_: str | None = Field(None, description="技能类型", alias="type")
    duration: float | None = Field(None, description="按键持续时间（单位秒）", ge=0)
    delay: float | None = Field(None, description="按键间隔时间（单位秒）", ge=0)
    repeat: int = Field(1, description="重复操作次数", ge=1)
    endure: bool = Field(False, description="霸体")
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


class TacticList(BaseModel):
    tac_list: List[List[Tactic]] = Field([], description="战斗逻辑配置")
    cur_pos: int = Field(0, description="列表序号")

    # 获取当前的战斗逻辑
    def get_cur_logic(self):
        list_len = len(self.tac_list)
        self.cur_pos %= list_len
        self.cur_pos += 1
        return self.tac_list[self.cur_pos - 1]


class TacticsConfig(BaseModel):
    char_icons: dict = Field({}, description="角色头像")
    tactics: dict = Field({}, description="战斗逻辑配置")
