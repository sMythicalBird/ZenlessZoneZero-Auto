# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: utils.py
@time: 2024/6/25 上午7:48
@author SuperLazyDog
"""
import time
from copy import deepcopy
from ctypes import windll
from re import Pattern, template
from typing import Dict
from threading import Lock
import cv2
import numpy as np
import win32gui
import win32ui
from PIL import Image, ImageFont, ImageDraw
from loguru import logger

from schema import ImgPosition, Position
from .init import Hwnd, RealWidth, RealHeight

def find_all_template(
    img: np.ndarray,
    template_img: np.ndarray | str,
    region: tuple = None,
    threshold: float = 0.8,
    w_ratio: float = None,
    h_ratio: float = None,
    limit: int = 0,
) -> list[ImgPosition]:
    """
    使用 opencv matchTemplate 方法在指定区域内进行模板匹配并返回所有匹配结果
    :param img:  大图片
    :param template_img: 小图片
    :param region:  区域（x1, y1, x2, y2），默认为 None 表示全图搜索
    :param threshold:  阈值
    :param w_ratio:  宽度缩放比例
    :param h_ratio:  高度缩放比例
    :param limit:  限制返回结果数量
    :return:
    """
    if isinstance(template_img, str):
        template_img = cv2.imread(template_img)
    # # 判断是否为灰度图，如果不是转换为灰度图
    # if len(img.shape) == 3:
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # if len(template_img.shape) == 3:
    #     template_img = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
    # 如果提供了region参数，则裁剪出指定区域，否则使用整幅图像
    if region:
        x, y, x2, y2 = region
        cropped_img = img[y:y2, x:x2]
    else:
        cropped_img = img
        x, y = 0, 0

    if w_ratio is None:
        w_ratio = 1
    if h_ratio is None:
        h_ratio = 1

    # 如果提供了缩放比例参数，则对模板进行缩放
    if w_ratio != 1 or h_ratio != 1:
        template_img = cv2.resize(template_img, (0, 0), fx=w_ratio, fy=h_ratio)
    # 在裁剪后的区域内进行模板匹配
    res = cv2.matchTemplate(cropped_img, template_img, cv2.TM_CCOEFF_NORMED)
    positions = []
    template_img_width, template_img_height, _ = template_img.shape[::-1]

    while True:
        if limit and len(positions) >= limit:
            break
        confidence = np.max(res)
        if confidence < threshold:
            break
        max_loc = np.where(res == confidence)
        left, top = max_loc[1][0], max_loc[0][0]
        x1, y1, x2, y2 = (
            left + x,
            top + y,
            left + x + template_img_width,
            top + y + template_img_height,
        )
        positions.append(
            ImgPosition(
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                confidence=confidence,
            )
        )
        # 将匹配到的区域置为0，防止重复匹配
        x1 = max(0, x1 - template_img_width)
        y1 = max(0, y1 - template_img_height)
        x2 = min(img.shape[1], x2 + template_img_width)
        y2 = min(img.shape[0], y2 + template_img_height)
        res[y1:y2, x1:x2] = 0
    return positions


def find_template(
    img: np.ndarray,
    template_img: np.ndarray | str,
    region: tuple = None,
    threshold: float = 0.8,
    w_ratio: float = None,
    h_ratio: float = None,
) -> None | ImgPosition:
    """
    使用 opencv matchTemplate 方法在指定区域内进行模板匹配并返回匹配结果
    :param img:  大图片
    :param template_img: 小图片
    :param region: 区域（x1, y1, x2, y2），默认为 None 表示全图搜索
    :param threshold:  阈值
    :param w_ratio:  宽度缩放比例
    :param h_ratio:  高度缩放比例
    :return: ImgPosition 或 None
    """
    positions = find_all_template(
        img, template_img, region, threshold, w_ratio, h_ratio, limit=1
    )
    if not positions:
        return None
    return positions[0]


screenshot_lock = Lock()


def screenshot() -> np.ndarray | None:
    """
    截取当前窗口的屏幕图像。

    通过调用Windows图形设备接口（GDI）和Python的win32gui、win32ui模块，
    本函数截取指定窗口的图像，并将其存储为numpy数组。

    返回值:
        - np.ndarray: 截图的numpy数组，格式为RGB（不包含alpha通道）。
        - None: 如果截取屏幕失败，则返回None。
    """
    screenshot_lock.acquire()
    hwndDC = win32gui.GetWindowDC(Hwnd)  # 获取窗口设备上下文（DC）
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 创建MFC DC从hwndDC
    saveDC = mfcDC.CreateCompatibleDC()  # 创建与mfcDC兼容的DC
    saveBitMap = win32ui.CreateBitmap()  # 创建一个位图对象
    saveBitMap.CreateCompatibleBitmap(
        mfcDC, RealWidth, RealHeight
    )  # 创建与mfcDC兼容的位图
    saveDC.SelectObject(saveBitMap)  # 选择saveDC的位图对象，准备绘图

    # 尝试使用PrintWindow函数截取窗口图像
    result = windll.user32.PrintWindow(Hwnd, saveDC.GetSafeHdc(), 3)
    if result != 1:
        logger.error("截取屏幕失败")
        # 释放所有资源
        try:
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(Hwnd, hwndDC)
            del hwndDC, mfcDC, saveDC, saveBitMap
        except Exception as e:
            logger.error(f"清理截图资源失败: {e}")
        screenshot_lock.release()
        return screenshot()  # 如果截取失败，则重试

    # 从位图中获取图像数据
    bmp_info = saveBitMap.GetInfo()  # 获取位图信息
    bmp_str = saveBitMap.GetBitmapBits(True)  # 获取位图数据
    im = np.frombuffer(bmp_str, dtype="uint8")  # 将位图数据转换为numpy数组
    im.shape = (bmp_info["bmHeight"], bmp_info["bmWidth"], 4)  # 设置数组形状
    # 调整通道顺序 并 去除alpha通道
    im = im[:, :, [2, 1, 0, 3]][:, :, :3]

    # 清理资源
    try:
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(Hwnd, hwndDC)
    except Exception as e:
        logger.error(f"清理截图资源失败: {e}")
    screenshot_lock.release()
    return im  # 返回截取到的图像


def np2pil(img: np.ndarray) -> Image.Image:
    """
    将numpy数组转换为PIL图像对象。
    通过调用PIL库，本函数将numpy数组转换为PIL图像对象。
    参数:
        - img: np.ndarray: 输入的numpy数组。
    返回值:
        - Image.Image: 转换后的PIL图像对象。
    """
    return Image.fromarray(img)


def cv2_add_chinese_text(img, text, position, textColor=(0, 255, 0), textSize=30):
    """
    在图片上添加中文文本
    """
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype("simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def wait_text(
    ocr,
    text: str | Pattern = None,
    target_texts: list[str | Pattern] = None,
    timeout: int = 10,
    region: Position = None,
) -> Dict[str, Position]:
    """
    等待指定文本出现
    :param text:  目标文本
    :param target_texts: 目标文本列表
    :param ocr:  Ocr对象
    :param region:  搜索区域
    :param timeout:  超时时间
    :return: Dict[str, Position] 字典的键为目标文本，值为位置
    """
    if text is None and target_texts is None:
        raise ValueError("text 和 target_texts 不能同时为 None")
    if text:
        target_texts += [text]
    for text in target_texts:
        if isinstance(text, str):
            target_texts[target_texts.index(text)] = template(text)
    start_time = time.time()
    while time.time() - start_time < timeout:
        ocr_results = {}
        target_texts_copy = deepcopy(target_texts)
        screen = screenshot()
        if screen is None:
            continue
        results = ocr.ocr(screen)
        for result in results:
            for text in target_texts_copy:
                if text.search(result.text):
                    if region and result.position not in region:
                        continue
                    ocr_results[text.pattern] = result.position
                    target_texts_copy.remove(text)
                    break
            if not target_texts_copy:
                return ocr_results
    return {}


def retry(count: int = 3, interval: int = 1):
    """
    重试装饰器
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(count):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception(e)
                    time.sleep(interval)
            return None

        return wrapper

    return decorator

