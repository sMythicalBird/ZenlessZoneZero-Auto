# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: info.py
@time: 2024/7/6 上午9:17
@author SuperLazyDog
"""
from datetime import datetime
from typing import List, Tuple
from pydantic import BaseModel, Field
from .map import MapComponent


class StatusInfo(BaseModel):
    currentPageName: str = Field("", title="当前页面名称")
    step: int = Field(0, title="当前地图已走步数")
    mapWay: List[Tuple[MapComponent, str]] = Field([], title="地图路径")
    lastMoveTime: datetime = Field(datetime.now(), title="上次移动时间")

    def reset_way(self):
        self.step = 0
        self.mapWay = []


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
