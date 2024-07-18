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
    fightCount: int = Field(0, description="战斗次数记录")
    entryMapTime: datetime = Field(datetime.now(), title="进入地图时间")
    currentStage: int = Field(
        0, title="当前阶段"
    )  # 0、无偏移     1、左下        2、右下


info = StatusInfo()
