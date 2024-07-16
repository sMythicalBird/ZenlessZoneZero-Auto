# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: utils.py
@time: 2024/7/9 上午12:52
@author SuperLazyDog
"""

import numpy as np
from onnxruntime import InferenceSession
import cv2

from schema import MapComponent, MapInfo
from utils import screenshot, RootPath
from ..detect import Model, find_current

DownloadPath = RootPath / "download"  # 下载路径


# components_model = InferenceSession(DownloadPath / "components.onnx")
components_model = InferenceSession(DownloadPath / "components_level.onnx")
components_input_name = components_model.get_inputs()[0].name
components_output_name = components_model.get_outputs()[0].name

television_model = InferenceSession(DownloadPath / "television.onnx")
television_input_name = television_model.get_inputs()[0].name
television_output_name = television_model.get_outputs()[0].name
television = Model(television_model, iou_threshold=0.1)


def preprocess_crop(crop):
    """Preprocess a single crop for model inference."""
    crop = cv2.resize(crop, (64, 64))
    crop = np.transpose(crop, (2, 0, 1))
    crop = np.expand_dims(crop, 0).astype(np.float32) / 255.0
    return crop


def infer_crop(crop):
    """Run model inference on a single preprocessed crop."""
    result = components_model.run(
        [components_output_name], {components_input_name: crop}
    )
    conf = np.max(result[0], axis=1)[0]
    index = np.argmax(result[0], axis=1)[0]
    return conf, index


def component_class(screen: np.ndarray, x: int, y: int, w: int, h: int) -> MapComponent:
    x1, y1 = max(x - w // 2, 0), max(y - h, 0)
    x2, y2 = min(x + w // 2, screen.shape[1]), y
    crop = screen[y1:y2, x1:x2]
    crop = preprocess_crop(crop)
    # 模型推理 输出每个组件的概率
    conf, index = infer_crop(crop)
    # 获取组件标签
    return MapComponent(
        x=x,  # 组件坐标
        y=y,  # 组件坐标
        confidence=conf,  # 组件置信度
        weight=index,  # 组件权重
    )


def get_map_info(screen: np.ndarray = None) -> MapInfo | None:
    """
    获取当前地图信息
    """
    if screen is None:
        screen = screenshot()
    screen_w = screen.shape[1]
    current = find_current(screen)  # 查找当前位置
    if current is None:  # 如果未找到当前位置，则返回None
        return None
    w, h = current.w, current.h  # 获取当前位置的宽高
    float_w, float_h = w * 1 / 2, h * 1 / 2  # 计算浮动宽高
    process_screen = television.preprocess(screen)  # 预处理屏幕图像
    # 模型推理
    pred = television_model.run(
        [television_output_name], {television_input_name: process_screen}
    )
    # 后处理
    outputs = television.postprocess(screen, pred)
    # 筛选出 y 值大于 h 的输出
    outputs = [
        output
        for output in outputs
        if output["y"] >= h // 2
        and w // 2 < output["x"] < screen_w - w // 2  # 去掉不完整的图片
    ]  # 按 x 坐标排序
    print(w)
    print(h)
    for each in outputs:
        print(each)
    input("loc")
    x_groups = []
    x_outputs = sorted(outputs, key=lambda item: item["x"])
    # 遍历输出 对x坐标进行分组
    while x_outputs:
        output = x_outputs.pop(0)
        x = output["x"]
        map_component = component_class(screen, x, output["y"], w, h)
        group = x_groups[-1] if x_groups else None
        if group is None or group["max_x"] < x:
            x_groups.append(
                {
                    "x": len(x_groups),
                    "min_x": x,
                    "max_x": x + float_w,
                    "map_components": [[output["y"], map_component]],
                }
            )
        else:
            group["map_components"].append([output["y"], map_component])
    for each in outputs:
        print(each)
    input("x_group")
    # 按 y 坐标排序
    y_groups = []
    y_outputs = sorted(outputs, key=lambda item: item["y"])
    # 遍历输出 对y坐标进行分组
    while y_outputs:
        output = y_outputs.pop(0)
        y = output["y"]
        group = y_groups[-1] if y_groups else None
        if group is None or group["max_y"] < y:
            y_groups.append(
                {
                    "y": len(y_groups),
                    "min_y": y,
                    "max_y": y + float_h,
                }
            )
    for each in y_outputs:
        print(each)
    input("y_groups")
    # 构建地图信息
    size = (len(x_groups), len(y_groups))
    map_info = MapInfo(size=size, w=w, h=h)
    # 遍历地图组件
    for y_group in y_groups:
        for x_group in x_groups:
            for mapComponent_y, map_component in x_group["map_components"]:
                if y_group["min_y"] <= mapComponent_y < y_group["max_y"]:
                    map_component.y = y_group["y"]
                    map_component.x = x_group["x"]
                    map_info.components[y_group["y"]][x_group["x"]] = map_component
    return map_info
