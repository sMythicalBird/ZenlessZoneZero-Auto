# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: utils.py
@time: 2024/7/9 上午12:52
@author SuperLazyDog
"""

import json

import cv2
import numpy as np
from onnxruntime import InferenceSession

from schema import MapComponent, MapInfo
from utils import screenshot, RootPath
from ..init import logger


DownloadPath = RootPath / "download"  # 下载路径

# 加载地图组件标签
with open(DownloadPath / "components.json", "r", encoding="utf-8") as f:
    components_label: dict = json.load(f)
    logger.debug("加载地图组件标签成功！")

# 加载地图组件信息
with open(DownloadPath / "components_info.json", "r", encoding="utf-8") as f:
    components_info: dict = json.load(f)
    logger.debug("加载地图组件信息成功！")

model = InferenceSession(DownloadPath / "components.onnx")
input_name = model.get_inputs()[0].name
output_name = model.get_outputs()[0].name


def get_map_info(
    size: tuple[int, int] = (5, 5),
    w: int = 124,
    h: int = 108,
    center_x: int = 640,
    center_y: int = 320,
) -> MapInfo:
    x1, y1 = (
        center_x - w * size[0] // 2,
        center_y - h * size[1] // 2,
    )  # 地图左上角坐标
    x2, y2 = (
        center_x + w * size[0] // 2,
        center_y + h * size[1] // 2,
    )  # 地图右下角坐标
    screen = screenshot()  # RGB格式图片
    # 将地图部分截取出来
    screen = screen[y1:y2, x1:x2, :]
    # 创建地图信息对象
    map_info = MapInfo(size=size, w=w, h=h, center_x=center_x, center_y=center_y)
    for i in range(size[0]):
        for j in range(size[1]):
            x = w * i
            y = h * j
            # 截取地图组件
            img = screen[y : y + h, x : x + w, :]
            # 图片预处理
            img = cv2.resize(img, (64, 64))
            img = np.transpose(img, (2, 0, 1))
            img = np.expand_dims(img, 0)
            img = img.astype(np.float32)
            img /= 255.0
            # 模型推理 输出每个组件的概率
            result = model.run([output_name], {input_name: img})
            conf = np.max(result[0], axis=1)[0]
            # 获取概率最大的组件索引
            index = np.argmax(result[0], axis=1)[0]
            # 获取组件标签
            label = components_label[str(index)]
            if conf < 0.9:
                map_info.components[i][j] = MapComponent(
                    name=f"未知_{label}", x=i, y=j, index=-1, confidence=conf
                )
                continue
            # 获取组件信息，如果没有则使用默认值
            component_info: dict = components_info.get(label, {})
            # 获取组件置信度
            # 创建地图组件对象
            map_info.components[i][j] = MapComponent(
                name=label,  # 组件名称
                x=i,  # 组件坐标
                y=j,  # 组件坐标
                index=index,  # 组件类别索引
                confidence=conf,  # 组件置信度
                obstacle=component_info.get("obstacle", True),  # 是否为障碍物
                hit=component_info.get("hit", 1),  # 需要碰撞的次数
            )
    return map_info
