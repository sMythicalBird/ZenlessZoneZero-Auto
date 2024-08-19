# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: init.py
@time: 2024/6/28 下午5:40
@author SuperLazyDog
"""
import re
import sys
from ctypes import windll
from pathlib import Path
import os
import ctypes
import win32api
import win32con
import win32gui
from loguru import logger
import onnxruntime as rt


def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


if not is_admin():
    logger.error("请以管理员权限运行此程序")
    input("按任意键退出...")
    sys.exit(0)
logger.debug("初始化utils模块中")
RootPath = Path(__file__).parent.parent
log_path = RootPath / "logs"
# 判断是否存在logs文件夹，不存在则创建
if not log_path.exists():
    log_path.mkdir()
logger.add(
    log_path / "logger.log",
    rotation="5 MB",
    encoding="utf-8",
    level="INFO",
    retention="14 days",
)


def wait_exit():
    input("按任意键退出...")
    sys.exit(0)


# 判断 root_path 中是否包含中文或特殊字符
special_chars_pattern = r"[\u4e00-\u9fa5\!\@\#\$\%\^\&\*\(\)]"
if bool(re.search(special_chars_pattern, str(RootPath))):
    logger.error("请将项目路径移动到纯英文路径下")
    wait_exit()

WidthRatio = 0
HeightRatio = 0
RealWidth = 0
RealHeight = 0
ScaleFactor = 0
OffsetX = 0
OffsetY = 0
Hwnd = win32gui.FindWindow("UnityWndClass", "绝区零")
if Hwnd == 0:
    Hwnd = win32gui.FindWindow("UnityWndClass", "ZenlessZoneZero")
if Hwnd == 0:
    logger.error("未找到游戏窗口")
    wait_exit()
else:
    # 将游戏窗口移动到屏幕左上角
    rect = win32gui.GetWindowRect(Hwnd)  # 获取窗口区域
    win32gui.MoveWindow(
        Hwnd, 0, 0, rect[2] - rect[0], rect[3] - rect[1], True
    )  # 设置窗口位置为0,0
    logger.debug("将游戏窗口移动到屏幕左上角")
    while True:
        rect = win32gui.GetWindowRect(Hwnd)  # 获取窗口区域
        if rect[0] == 0 and rect[1] == 0:
            break
    left, top, right, bot = win32gui.GetClientRect(Hwnd)
    w = right - left
    h = bot - top
    ScaleFactor = None
    try:
        windll.shcore.SetProcessDpiAwareness(1)  # 设置进程的 DPI 感知
        # 获取主显示器的缩放因子
        ScaleFactor = windll.shcore.GetScaleFactorForDevice(0) / 100
    except Exception as e:
        logger.exception(e)
        wait_exit()
    RealWidth = round(w * ScaleFactor)
    RealHeight = round(h * ScaleFactor)
    menu_height = win32api.GetSystemMetrics(win32con.SM_CYSIZE)
    RealRight = round((rect[2] - rect[0]) * ScaleFactor)
    RealBot = round((rect[3] - rect[1]) * ScaleFactor)
    OffsetX = (RealRight - RealWidth) / 2
    OffsetY = (RealBot - menu_height - RealHeight - 1) / 2 + menu_height + 1
    logger.info(
        f"游戏窗口宽度为{w}，高度为{h},缩放因子为{ScaleFactor},实际宽度为{RealWidth},实际高度为{RealHeight}"
    )
    logger.info(f"菜单栏高度为{menu_height},左上角偏移量为({OffsetX},{OffsetY})")
    # if not(RealWidth == 1280 and RealHeight == 720):
    #     logger.warning("游戏窗口分辨率不是1280x720，请修改游戏显示模式为“1280x720 窗口”")
    #     wait_exit()

# 判断能否使用GPU
if "CUDAExecutionProvider" in rt.get_available_providers():
    Provider = ["CUDAExecutionProvider"]
elif "DmlExecutionProvider" in rt.get_available_providers():
    Provider = ["DmlExecutionProvider"]
else:
    Provider = ["CPUExecutionProvider"]
