# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: utils.py
@time: 2024/7/11 下午8:57
@author SuperLazyDog
"""
from onnxruntime import InferenceSession
import cv2
import numpy as np

from schema import ImgPosition


def _update_labels(labels, ratio, padw, padh):
    """Update labels."""
    labels["instances"].convert_bbox(format="xyxy")
    labels["instances"].denormalize(*labels["img"].shape[:2][::-1])
    labels["instances"].scale(*ratio)
    labels["instances"].add_padding(padw, padh)
    return labels


class LetterBox:
    """
    Resize image and padding for detection, instance segmentation, pose.
    """

    def __init__(
        self,
        new_shape=(640, 640),
        auto=False,
        scaleFill=False,
        scaleup=True,
        center=True,
        stride=32,
    ):
        """初始化LetterBox对象，指定特定参数。

        参数:
            new_shape(tuple): 指定输出图像的新尺寸，默认为(640, 640)。
            auto(bool): 是否自动调整图像尺寸，默认为False。
            scaleFill(bool): 是否根据新尺寸缩放填充图像，默认为False。
            scaleup(bool): 是否允许图像尺寸放大，默认为True。
            center(bool): 是否将图像居中，默认为True。
            stride(int): 步长，默认为32。
        """
        self.new_shape = new_shape
        self.auto = auto
        self.scaleFill = scaleFill
        self.scaleup = scaleup
        self.stride = stride
        self.center = center  # 是否将图像放在中间或左上角

    def __call__(self, labels=None, image=None):
        """对输入的labels和image添加边框，并返回更新后的labels和image。

        Args:
            labels (dict, optional): 输入的标签信息，包括img和其他相关信息，默认为None.
            image (ndarray, optional): 输入的图像，默认为None.

        Returns:
            dict or ndarray: 更新后的labels或image.

        """
        if labels is None:
            labels = {}

        img = labels.get("img") if image is None else image
        shape = img.shape[:2]  # 当前形状 [高度, 宽度]
        new_shape = labels.pop("rect_shape", self.new_shape)
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # 缩放比例 (新 / 旧)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not self.scaleup:  # 仅缩小，不放大 (以获得更好的验证mAP)
            r = min(r, 1.0)

        # 计算填充
        ratio = r, r  # 宽度，高度比例
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = (
            new_shape[1] - new_unpad[0],
            new_shape[0] - new_unpad[1],
        )  # 填充的宽度，高度
        if self.auto:  # 最小矩形
            dw, dh = np.mod(dw, self.stride), np.mod(
                dh, self.stride
            )  # 填充的宽度，高度
        elif self.scaleFill:  # 拉伸
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # 宽度，高度比例

        if self.center:
            dw /= 2  # 将填充分为两侧
            dh /= 2

        if shape[::-1] != new_unpad:  # 调整大小
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)) if self.center else 0, int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)) if self.center else 0, int(round(dw + 0.1))
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114)
        )  # 添加边框
        if labels.get("ratio_pad"):
            labels["ratio_pad"] = (labels["ratio_pad"], (left, top))  # 用于评估

        if len(labels):
            labels = _update_labels(labels, ratio, dw, dh)
            labels["img"] = img
            labels["resized_shape"] = new_shape
            return labels
        else:
            return img


class Model:

    def __init__(
        self,
        model: InferenceSession,
        conf_threshold: float = 0.5,
        iou_threshold: float = 0.5,
    ):
        self.model = model
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.input_name = model.get_inputs()[0].name
        self.label_name = model.get_outputs()[0].name
        input_shape = model.get_inputs()[0].shape
        self.input_height = input_shape[2]
        self.input_width = input_shape[3]
        self.letterbox = LetterBox((self.input_height, self.input_width))
        self.pad_w = 0
        self.pad_h = 0
        self.scale_ratio = 0

    def preprocess(self, img: np.ndarray):
        """
        在进行推理之前，对输入图像进行预处理。
        返回:
            image_data: 预处理后的图像数据，准备好进行推理。
        """

        # 将图像调整为匹配输入形状(640,640,3)
        img_height, img_width = img.shape[:2]  # 获取输入图片形状
        img = self.letterbox(image=img)
        scale_ratio_w = img_width / self.input_width
        scale_ratio_h = img_height / self.input_height
        self.scale_ratio = max(scale_ratio_w, scale_ratio_h)  # 实际缩放比例
        # 当前偏移量
        self.pad_w = 0  # 重置一次
        self.pad_h = 0
        if scale_ratio_w < scale_ratio_h:
            self.pad_w = (
                self.input_width - self.input_width * img_width / img_height
            ) / 2
        elif scale_ratio_w > scale_ratio_h:
            self.pad_h = (
                self.input_height - self.input_height * img_height / img_width
            ) / 2
        # 将图像数据除以255.0进行归一化
        image_data = np.array(img) / 255.0

        # 转置图像，使通道维度成为第一个维度(3,640,640)
        image_data = np.transpose(image_data, (2, 0, 1))  # 通道优先

        # 扩展图像数据的维度以匹配期望的输入形状(1,3,640,640)
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)

        # 返回预处理后的图像数据
        return image_data

    def postprocess(self, input_image: np.ndarray, output: np.ndarray) -> list[dict]:
        img_height, img_width = input_image.shape[:2]
        # 转置并压缩输出以匹配期望的形状：(8400, 84)
        outputs = np.transpose(np.squeeze(output[0]))
        # 获取输出数组的行数
        rows = outputs.shape[0]
        # 存储检测到的边界框、分数和类别ID的列表
        boxes = []
        scores = []
        class_ids = []
        # # 计算边界框坐标的比例因子
        # x_factor = img_width / self.input_width
        # y_factor = img_height / self.input_height

        # 遍历输出数组的每一行
        for i in range(rows):
            # 从当前行提取类别的得分
            classes_scores = outputs[i][4:]
            # 找到类别得分中的最大值
            max_score = np.amax(classes_scores)

            # 如果最大得分大于或等于置信度阈值
            if max_score >= self.conf_threshold:
                # 获取得分最高的类别ID
                class_id = np.argmax(classes_scores)
                # 从当前行提取边界框坐标
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                # 计算边界框的缩放坐标
                left = round((x - w / 2 - self.pad_w) * self.scale_ratio)
                top = round((y - h / 2 - self.pad_h) * self.scale_ratio)
                width = round(w * self.scale_ratio)
                height = round(h * self.scale_ratio)
                # 将类别ID、得分和边界框坐标添加到相应的列表中
                class_ids.append(class_id)
                scores.append(max_score)
                boxes.append([left, top, width, height])

        # 应用非极大抑制以过滤重叠的边界框
        indices = cv2.dnn.NMSBoxes(
            boxes, scores, self.conf_threshold, self.iou_threshold
        )

        results = []
        # 遍历非极大抑制后选择的索引
        for i in indices:
            # 获取与索引对应的边界框、得分和类别ID
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]
            x1, y1, w, h = box
            x, y = round(x1 + w // 2), round(y1 + h // 2)
            # 将检测结果添加到结果列表中
            results.append(
                {
                    "class": class_id,
                    "conf": score,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h,
                    "label": True,  # 是否需要进行图片分类
                }
            )
        # 返回修改后的输入图像
        return results

    def max_box(self, input_image: np.ndarray, results: np.ndarray):
        img_height, img_width = input_image.shape[:2]
        outputs = np.transpose(np.squeeze(results[0]))
        max_score = np.amax(outputs[:, 4:])
        # 获取最高置信度的索引
        max_index = np.argmax(outputs[:, 4:])
        # 如果最高置信度大于等于阈值
        if max_score >= self.conf_threshold:
            # 获取最高置信度的类别ID
            # 获取最高置信度的边界框坐标
            x, y, w, h = outputs[max_index, :4]
            # 将边界框坐标转换为原始图像的坐标
            x1 = round((x - w / 2) * img_width / self.input_width)
            y1 = round((y - h / 2) * img_height / self.input_height)
            x2 = round((x + w / 2) * img_width / self.input_width)
            y2 = round((y + h / 2) * img_height / self.input_height)
            return ImgPosition(x1=x1, y1=y1, x2=x2, y2=y2, confidence=max_score)
        return None
