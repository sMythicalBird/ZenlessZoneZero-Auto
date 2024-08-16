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
import yaml
from schema import MapComponent, MapInfo
from utils import screenshot, RootPath, config
from ..detect import Model, find_current
from ..init import Provider

DownloadPath = RootPath / "download"  # 下载路径


# components_model = InferenceSession(DownloadPath / "components.onnx")
components_model = InferenceSession(
    str(DownloadPath / "components_keyword.onnx"), providers=Provider
)
components_input_name = components_model.get_inputs()[0].name
components_output_name = components_model.get_outputs()[0].name

television_model = InferenceSession(
    str(DownloadPath / "television.onnx"), providers=Provider
)
television_input_name = television_model.get_inputs()[0].name
television_output_name = television_model.get_outputs()[0].name
television = Model(television_model, iou_threshold=0.1)

# 记录模型输出的index对应的标签名和标签权重
with open(DownloadPath / "components_label.yaml", "r", encoding="utf-8") as f:
    components_label = yaml.safe_load(f)

# 通关模式，接一次队友
if config.modeSelect == 1:
    for i in components_label:
        if components_label[i]["name"] == "呼叫增援":
            components_label[i]["weight"] = 10
# 零号业绩模式，改变权重
if config.modeSelect == 2:
    for i in components_label:
        if components_label[i]["name"] == "零号业绩":
            components_label[i]["weight"] = 10
# 零号银行，改变权重
if config.modeSelect == 3:
    for i in components_label:
        if components_label[i]["name"] == "零号银行":
            components_label[i]["weight"] = 10
# 零号银行和零号业绩一起刷，改变权重
if config.modeSelect == 4:
    for i in components_label:
        if components_label[i]["name"] == "零号银行":
            components_label[i]["weight"] = 10


# 零号银行和零号业绩一起刷
def my_set_weight():
    # 拿完银行改变权重
    for i in components_label:
        if components_label[i]["name"] == "零号银行":
            components_label[i]["weight"] = 0
        if components_label[i]["name"] == "零号业绩":
            components_label[i]["weight"] = 10


def my_unset_weight():
    # 拿完业绩改变权重
    for i in components_label:
        if components_label[i]["name"] == "零号银行":
            components_label[i]["weight"] = 10
        if components_label[i]["name"] == "零号业绩":
            components_label[i]["weight"] = 0


def set_weight(name: str, weight: int):
    """
    改变权重
    """
    global components_label
    for item in components_label:
        if components_label[item]["name"] == name:
            components_label[item]["weight"] = weight


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


def component_class(
    screen: np.ndarray, x: int, y: int, w: int, h: int, label: int
) -> MapComponent:
    if label:
        x1, y1 = round(max(x - w / 2, 0)), round(max(y - h, 0))
        x2, y2 = round(min(x + w / 2, screen.shape[1])), round(y)
        crop = screen[y1:y2, x1:x2]
        crop = preprocess_crop(crop)
        # 模型推理 输出每个组件的概率
        conf, index = infer_crop(crop)
        if conf < 0.95:
            return MapComponent(
                name="当前未识别",  # 组件名称
                x=1,  # 组件坐标
                y=1,  # 组件坐标
                confidence=0,  # 组件置信度
                weight=1,  # 组件权重
            )
        # 获取组件标签
        return MapComponent(
            name=components_label[str(index)]["name"],
            x=x,  # 组件坐标
            y=y,  # 组件坐标
            confidence=conf,  # 组件置信度
            weight=components_label[str(index)]["weight"],  # 组件权重
            tp_id=components_label[str(index)]["tp_id"],  # 强制传送类型
        )
    return MapComponent(
        name="double",  # 组件名称
        x=1,  # 组件坐标
        y=1,  # 组件坐标
        confidence=0,  # 组件置信度
        weight=1,  # 组件权重
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
    # print(outputs)
    # input()
    outputs = [
        output
        for output in outputs
        if output["y"] >= h // 2
        and w // 2 < output["x"] < screen_w - w // 2  # 去掉不完整的图片
        and output["conf"] > 0.8  # 置信度大于0.8
    ]  # 按 x 坐标排序
    # 2*2 格子拆分
    m_w = w * 1.5  # 切割2*2
    outputs_real = []
    for each in outputs:
        if each["w"] < m_w:
            outputs_real.append(each)
        else:
            # 如果宽度大于2倍宽度，拆分为4个小格子
            # 计算中心点和小格子相对偏移量
            center_x = each["x"]
            center_y = each["y"] - h / 2
            offset_x = each["w"] / 4
            offset_y = h / 2
            outputs_real.append(
                {
                    "x": center_x - offset_x,
                    "y": center_y - offset_y,
                    "label": False,  # 是否需要进行图片分类
                }
            )
            outputs_real.append(
                {
                    "x": center_x + offset_x,
                    "y": center_y - offset_y,
                    "label": False,
                }
            )
            outputs_real.append(
                {
                    "x": center_x - offset_x,
                    "y": center_y + offset_y,
                    "label": False,
                }
            )
            outputs_real.append(
                {
                    "x": center_x + offset_x,
                    "y": center_y + offset_y,
                    "label": False,
                }
            )
    x_groups = []
    # 按 x 坐标排序
    x_outputs = sorted(outputs_real, key=lambda item: item["x"])
    # 遍历输出 对x坐标进行分组
    while x_outputs:
        output = x_outputs.pop(0)
        x = output["x"]
        map_component = component_class(screen, x, output["y"], w, h, output["label"])
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
    # 按 y 坐标排序
    y_groups = []
    y_outputs = sorted(outputs_real, key=lambda item: item["y"])
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
    # 构建地图信息
    size = (len(x_groups), len(y_groups))
    map_info = MapInfo(size=size, w=w, h=h)
    # 遍历地图组件，建立二维矩阵
    for y_group in y_groups:
        for x_group in x_groups:
            for mapComponent_y, map_component in x_group["map_components"]:
                if y_group["min_y"] <= mapComponent_y < y_group["max_y"]:
                    map_component.y = y_group["y"]
                    map_component.x = x_group["x"]
                    map_info.components[y_group["y"]][x_group["x"]] = map_component
    # for each in map_info.components:
    #     print(each)
    # input()
    return map_info
