# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: map.py
@time: 2024/7/9 上午1:41
@author SuperLazyDog
"""
from typing import List

from pydantic import BaseModel, Field


class MapComponent(BaseModel):
    name: str = Field(title="组件名称")
    x: int = Field(title="组件坐标")
    y: int = Field(title="组件坐标")
    index: int = Field(title="组件索引")
    confidence: float = Field(0, title="组件置信度")
    obstacle: bool = Field(True, title="是否为障碍物")
    hit: int = Field(1, title="需要的撞击次数")


class MapInfo(BaseModel):
    name: str = Field("地图信息", title="地图名称")
    size: tuple[int, int] = Field((5, 5), title="地图格子大小")
    center_x: int = Field(640, title="地图中心坐标")
    center_y: int = Field(320, title="地图中心坐标")
    w: int = Field(124, title="每个格子的大小")
    h: int = Field(108, title="每个格子的大小")
    components: List[List[MapComponent]] = Field([], title="组件信息")

    def __init__(self, **data):
        if "size" not in data:
            raise ValueError("size is required")
        if "components" not in data:
            data["components"] = [
                [MapComponent(name="默认", x=0, y=0, index=-1)] * data["size"][0]
                for _ in range(data["size"][1])
            ]  # 初始化组件二维数组
        super().__init__(**data)

    def __getitem__(self, item):
        return self.components[item]
