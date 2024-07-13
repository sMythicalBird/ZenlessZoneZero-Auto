# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: screenshot.py
@time: 2024/7/5 下午4:17
@author SuperLazyDog
"""
from ctypes import windll
import numpy as np
from PIL import Image
import win32gui
import win32ui
from pynput.keyboard import Key, Listener
from loguru import logger
from threading import Thread
from pathlib import Path

RootPath = Path(__file__).parent.parent
screenshot_path = RootPath / "yolo/screenshot"


def screenshot(hwnd, real_w, real_h) -> np.ndarray | None:
    """
    截取当前窗口的屏幕图像。

    通过调用Windows图形设备接口（GDI）和Python的win32gui、win32ui模块，
    本函数截取指定窗口的图像，并将其存储为numpy数组。

    返回值:
        - np.ndarray: 截图的numpy数组，格式为RGB（不包含alpha通道）。
        - None: 如果截取屏幕失败，则返回None。
    """
    hwndDC = win32gui.GetWindowDC(hwnd)  # 获取窗口设备上下文（DC）
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 创建MFC DC从hwndDC
    saveDC = mfcDC.CreateCompatibleDC()  # 创建与mfcDC兼容的DC
    saveBitMap = win32ui.CreateBitmap()  # 创建一个位图对象
    saveBitMap.CreateCompatibleBitmap(
        mfcDC, int(real_w), int(real_h)
    )  # 创建与mfcDC兼容的位图
    saveDC.SelectObject(saveBitMap)  # 选择saveDC的位图对象，准备绘图

    # 尝试使用PrintWindow函数截取窗口图像
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    if result != 1:
        logger.error(f"PrintWindow函数截取失败: {result}")
        return None  # 如果截取失败，则返回None

    # 从位图中获取图像数据
    bmp_info = saveBitMap.GetInfo()  # 获取位图信息
    bmp_str = saveBitMap.GetBitmapBits(True)  # 获取位图数据
    im = np.frombuffer(bmp_str, dtype="uint8")  # 将位图数据转换为numpy数组
    im.shape = (bmp_info["bmHeight"], bmp_info["bmWidth"], 4)  # 设置数组形状
    im = im[:, :, [2, 1, 0, 3]][:, :, :3]  # 调整颜色通道顺序为RGB 并去掉alpha通道

    # 清理资源
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return im  # 返回截取到的图像waA


def get_scale_factor():
    try:
        windll.shcore.SetProcessDpiAwareness(1)  # 设置进程的 DPI 感知
        scale_factor = windll.shcore.GetScaleFactorForDevice(
            0
        )  # 获取主显示器的缩放因子
        return scale_factor / 100  # 返回百分比形式的缩放因子
    except Exception as e:
        print("Error:", e)
        return None


running = False


def screen(path: Path, count: int = None):
    global running
    if running:
        return
    running = True
    hwnd = win32gui.FindWindow("UnityWndClass", "绝区零")
    if hwnd == 0:
        print("未找到游戏窗口")
        return
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    w = right - left
    h = bot - top
    scale_factor = get_scale_factor()
    real_w = int(w * scale_factor)
    real_h = int(h * scale_factor)
    images_count = len(list(path.glob("*.png")))
    while running:
        logger.info("截图")
        img = screenshot(hwnd, real_w, real_h)
        img = Image.fromarray(img)
        img.save(rf"{path}\{images_count}.png")
        images_count += 1
        if count:
            count -= 1
            if count <= 0:
                running = False
                break
    logger.info("截图结束")


def on_press(key):
    global running
    match key:
        case Key.f8:
            logger.info("开始截图（单次）")
            Thread(target=screen, args=(screenshot_path, 1)).start()
        case Key.f9:
            logger.info("开始截图:20次")
            Thread(target=screen, args=(screenshot_path, 20)).start()
        case Key.f10:
            logger.info("开始截图")
            Thread(target=screen, args=(screenshot_path,)).start()
        case Key.f11:
            logger.info("暂停截图")
            running = False
        case Key.f12:
            logger.info("结束截图")
            running = False
            return False
    return None


if __name__ == "__main__":
    print(
        """
    按键说明:
    F8: 开始截图（单次）
    F9: 开始截图（20次）
    F10: 开始截图
    F11: 暂停截图
    F12: 结束截图
    """
    )

    with Listener(on_press=on_press) as listener:
        listener.join()
