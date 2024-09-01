# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: ocr.py
@time: 2024/6/25 下午4:19
@author SuperLazyDog
"""
import time

import numpy as np

from schema import OcrResult, Position, OcrWordResult
from .constant import ModelsPath
from .download import maybe_download
from ..init import logger
from schema.cfg.info import zero_cfg

models = {
    "ch_PP-OCRv4_rec_server_infer": "https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_server_infer.tar",
    "ch_PP-OCRv4_rec_infer": "https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_infer.tar",
    "ch_PP-OCRv4_det_server_infer": "https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_server_infer.tar",
    "ch_PP-OCRv4_det_infer": "https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_infer.tar",
    # "ch_ppocr_mobile_v2.0_cls": "https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar",
}


class Ocr:
    last_time = time.time()

    def __init__(
        self,
        rec_model_dir: str = None,
        det_model_dir: str = None,
        interval: float = 0,
        server_model: bool = False,
        return_word_box: bool = False,
    ):
        """
        初始化OCR
        :param rec_model_dir:  文本识别模型目录
        :param det_model_dir:  文本检测模型目录
        :param interval:  OCR调用间隔时间
        :param server_model:  是否使用Server模型 Server模型更大
        :param return_word_box:  是否返回单字框
        :return:
        """
        logger.debug("初始化OCR")
        # 由于PaddleOCR的import速度较慢，所以在这里导入
        from paddleocr import PaddleOCR
        from paddle.device import is_compiled_with_cuda

        if rec_model_dir is None:  # 如果没有传入模型目录，则下载模型
            rec_model_dir = (
                maybe_download(
                    ModelsPath / "ch_PP-OCRv4_rec_server_infer",
                    models["ch_PP-OCRv4_rec_server_infer"],
                )
                if server_model  # 如果使用服务器模型
                else maybe_download(
                    ModelsPath / "ch_PP-OCRv4_rec_infer",
                    models["ch_PP-OCRv4_rec_infer"],
                )
            )
        if det_model_dir is None:
            det_model_dir = (
                maybe_download(
                    ModelsPath / "ch_PP-OCRv4_det_server_infer",
                    models["ch_PP-OCRv4_det_server_infer"],
                )
                if server_model  # 如果使用服务器模型
                else maybe_download(
                    ModelsPath / "ch_PP-OCRv4_det_infer",
                    models["ch_PP-OCRv4_det_infer"],
                )
            )
        self.interval = interval
        # 判断GPU是否可用
        use_gpu = is_compiled_with_cuda()
        # 判断是否使用cpu
        device = "GPU" if use_gpu and zero_cfg.useGpu else "CPU"
        logger.debug(f"使用{device}进行OCR识别")
        self.paddleOCR = PaddleOCR(
            use_angle_cls=False,
            lang="ch",
            use_gpu=use_gpu,
            show_log=False,
            rec_model_dir=rec_model_dir,
            det_model_dir=det_model_dir,
            return_word_box=return_word_box,
        )
        self.return_word_box = return_word_box
        logger.debug("初始化OCR完成")

    def check_interval(self):
        """
        检查OCR调用间隔
        :return:
        """
        if time.time() - self.last_time < self.interval:
            time.sleep(self.interval - (time.time() - self.last_time))
        self.last_time = time.time()

    def ocr(self, img: np.ndarray) -> list[OcrResult]:
        """
        文字识别
        """
        if self.interval:
            self.check_interval()
        results = self.paddleOCR.ocr(img, cls=False)[0]
        if not results:
            return []
        res = []
        for result in results:
            text = result[1][0]
            position = result[0]
            position = Position(
                x1=position[0][0],
                y1=position[0][1],
                x2=position[2][0],
                y2=position[2][1],
            )
            confidence = result[1][1]
            res.append(OcrResult(text=text, position=position, confidence=confidence))
        return res

    def word_ocr(self, img: np.ndarray) -> list[OcrWordResult]:
        """
        文字识别
        :param img:  图片
        :return:
        """
        assert self.return_word_box, "请在初始化时设置return_word_box=True"
        if self.interval:
            self.check_interval()
        results = self.paddleOCR.ocr(img, cls=False)[0]
        if not results:
            return []
        res = []
        for result in results:
            text = result[1][0]
            x = [i[0] for i in result[0]]
            y = [i[1] for i in result[0]]
            position = Position(
                x1=min(x),
                y1=min(y),
                x2=max(x),
                y2=max(y),
            )
            word_positions = cal_ocr_word_box(text, position, result[1][2])
            confidence = result[1][1]
            res.append(
                OcrWordResult(
                    text=text,
                    position=position,
                    confidence=confidence,
                    word_positions=word_positions,
                )
            )
        return res

    def __call__(self, img: np.ndarray):
        return self.ocr(img)

    def ocr_state(
        self, img: np.ndarray, states: str | list[str] = "cn"
    ) -> list[OcrResult]:
        """
        文字识别
        :param img:  图片
        :param states:  识别的文字类型  cn en&num splitter
        :return:
        """
        assert self.return_word_box, "请在初始化时设置return_word_box=True"
        if self.interval:
            self.check_interval()
        if isinstance(states, str):
            states = states.split()
        results = self.paddleOCR.ocr(img, cls=False)[0]
        if not results:
            return []
        res = []
        for result in results:
            all_text = result[1][0]
            x = [i[0] for i in result[0]]  # 识别框的x坐标
            y = [i[1] for i in result[0]]  # 识别框的y坐标
            confidence = result[1][1]  # 识别的置信度
            bbox_x_start = min(x)  # 识别框的左上角x坐标
            bbox_x_end = max(x)  # 识别框的右下角x坐标
            bbox_y_start = min(y)  # 识别框的左上角y坐标
            bbox_y_end = max(y)  # 识别框的右下角y坐标
            # 识别的文字信息 包括 列数、文字、列的位置、文字类型
            col_num, word_list, word_col_list, state_list = result[1][2]
            cell_width = (bbox_x_end - bbox_x_start) / col_num  # 每列的宽度
            for word, word_col, state in zip(
                word_list, word_col_list, state_list
            ):  # 遍历识别的文字信息
                if state not in states:  # 如果识别的文字类型不在指定的类型中，则跳过
                    continue
                if len(word_col) > 1:
                    char_seq_length = (word_col[-1] - word_col[0] + 1) * cell_width
                    char_width = char_seq_length / (
                        len(word_col) - 1
                    )  # 如果文字列有多个，则计算文字宽度
                else:
                    # 如果文字列只有一个，则直接计算文字宽度
                    char_width = (bbox_x_end - bbox_x_start) / len(all_text)
                start_x = (word_col[0] + 0.5) * cell_width
                end_x = (word_col[-1] + 0.5) * cell_width
                cell_x_start = (
                    max(int(start_x - char_width / 2), 0) + bbox_x_start
                )  # 文字的左上角x坐标
                cell_x_end = (
                    min(int(end_x + char_width / 2), bbox_x_end - bbox_x_start)
                    + bbox_x_start
                )
                p = Position(
                    x1=cell_x_start,
                    y1=bbox_y_start,
                    x2=cell_x_end,
                    y2=bbox_y_end,
                )
                text = "".join(word)  # 文字
                res.append(OcrResult(text=text, position=p, confidence=confidence))
        return res


def cal_ocr_word_box(rec_str: str, box: Position, rec_word_info: tuple):
    col_num, word_list, word_col_list, state_list = rec_word_info
    bbox_x_start = box.x1
    bbox_x_end = box.x2
    bbox_y_start = box.y1
    bbox_y_end = box.y2
    cell_width = (bbox_x_end - bbox_x_start) / col_num
    word_box_list = []
    cn_width_list = []
    cn_col_list = []
    for word, word_col, state in zip(word_list, word_col_list, state_list):
        if state == "cn":
            if len(word_col) != 1:
                char_seq_length = (word_col[-1] - word_col[0] + 1) * cell_width
                char_width = char_seq_length / (len(word_col) - 1)
                cn_width_list.append(char_width)
            cn_col_list += word_col
        else:
            cell_x_start = bbox_x_start + int(word_col[0] * cell_width)
            cell_x_end = bbox_x_start + int((word_col[-1] + 1) * cell_width)
            p = Position(
                x1=cell_x_start,
                y1=bbox_y_start,
                x2=cell_x_end,
                y2=bbox_y_end,
            )
            word_box_list.append(p)
    if len(cn_col_list) != 0:
        if len(cn_width_list) != 0:
            avg_char_width = np.mean(cn_width_list)
        else:
            avg_char_width = (bbox_x_end - bbox_x_start) / len(rec_str)
        for center_idx in cn_col_list:
            center_x = (center_idx + 0.5) * cell_width
            cell_x_start = max(int(center_x - avg_char_width / 2), 0) + bbox_x_start
            cell_x_end = (
                min(int(center_x + avg_char_width / 2), bbox_x_end - bbox_x_start)
                + bbox_x_start
            )
            p = Position(
                x1=cell_x_start,
                y1=bbox_y_start,
                x2=cell_x_end,
                y2=bbox_y_end,
            )
            word_box_list.append(p)
    return sorted(word_box_list, key=lambda pos: pos.x1)


paddle_ocr = Ocr()
