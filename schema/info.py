# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: info.py
@time: 2024/7/6 上午9:17
@author SuperLazyDog
"""
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from enum import Enum


class Dirct(Enum):
    up = "w"
    down = "s"
    left = "a"
    right = "d"

    def __str__(self):
        return self.value

    # 取反
    def reverse(self):
        if self == Dirct.up:
            return Dirct.down
        if self == Dirct.down:
            return Dirct.up
        if self == Dirct.left:
            return Dirct.right
        if self == Dirct.right:
            return Dirct.left


class StatusInfo(BaseModel):
    currentPageName: str = Field("", title="当前页面名称")
    lastMoveTime: datetime = Field(datetime.now(), title="上次移动时间")
    lastDirct: Dirct = Field("", title="上次移动方向")
    fightCount: int = Field(10, description="战斗次数记录")
    entryMapTime: datetime = Field(datetime.now(), title="进入地图时间")


info = StatusInfo()


class Second_MapInfo(BaseModel):
    currentPageName: str = Field("", title="当前页面名称")
    step: int = Field(0, title="当前地图已走步数")
    mapWay: List[str] = Field([], title="地图路径")

    def reset_way(self):
        self.step = 0
        self.mapWay = []

    def get_way(self):
        self.mapWay = ["w", "d", "w", "d", "w", "d", "d", "w"]


sec_info = Second_MapInfo()
