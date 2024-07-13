# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: current.py
@time: 2024/7/11 下午6:59
@author SuperLazyDog
"""
import onnxruntime as rt
from schema import ImgPosition
from ..utils import screenshot
import cv2
import numpy as np
from ..init import RootPath, logger

model_path = RootPath / "download" / "current.onnx"

# 判断能否使用GPU
if "CUDAExecutionProvider" in rt.get_available_providers():
    provider = ["CUDAExecutionProvider"]
elif "DmlExecutionProvider" in rt.get_available_providers():
    provider = ["DmlExecutionProvider"]
else:
    provider = ["CPUExecutionProvider"]
logger.info(f"使用 {','.join(provider)} 运行当前位置识别模型")
model = rt.InferenceSession(model_path, providers=provider)
input_name = model.get_inputs()[0].name
label_name = model.get_outputs()[0].name

# 获取模型的输入形状
input_shape = model.get_inputs()[0].shape
input_height = input_shape[2]
input_width = input_shape[3]


def find_current(
        screen: np.ndarray = None,
        conf_threshold: float = 0.5, iou_threshold: float = 0.5
) -> ImgPosition | None:
    """
    Find the current location.
    """
    if screen is None:
        screen = screenshot()
    img_height, img_width = screen.shape[:2]
    screen = cv2.resize(screen, (input_width, input_height))
    screen = screen.transpose(2, 0, 1)
    screen = screen[np.newaxis, ...].astype(np.float32)
    screen /= 255.0
    pred = model.run([label_name], {input_name: screen})
    outputs = np.transpose(np.squeeze(pred[0]))
    # 获取最高置信度
    max_score = np.amax(outputs[:, 4:])
    # 获取最高置信度的索引
    max_index = np.argmax(outputs[:, 4:])
    # 如果最高置信度大于等于阈值
    if max_score >= conf_threshold:
        # 获取最高置信度的类别ID
        class_id = max_index
        # 获取最高置信度的边界框坐标
        x, y, w, h = outputs[max_index, :4]
        # 将边界框坐标转换为原始图像的坐标
        x1 = int((x - w / 2) * img_width / input_width)
        y1 = int((y - h / 2) * img_height / input_height)
        x2 = int((x + w / 2) * img_width / input_width)
        y2 = int((y + h / 2) * img_height / input_height)
        return ImgPosition(x1=x1, y1=y1, x2=x2, y2=y2, confidence=max_score)
    return None
