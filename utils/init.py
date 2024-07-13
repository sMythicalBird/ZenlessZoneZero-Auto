# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: init.py
@time: 2024/6/28 下午5:40
@author SuperLazyDog
"""
import re
import sys
import time
from ctypes import windll
from pathlib import Path

import win32api
import win32con
import win32gui
from loguru import logger

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
    logger.error("未找到游戏窗口")
else:
    # 将游戏窗口移动到屏幕左上角
    rect = win32gui.GetWindowRect(Hwnd)  # 获取窗口区域
    win32gui.MoveWindow(
        Hwnd, 0, 0, rect[2] - rect[0], rect[3] - rect[1], True
    )  # 设置窗口位置为0,0
    time.sleep(1)  # 等待窗口移动完成
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
    WidthRatio = w / 1280 * ScaleFactor
    HeightRatio = h / 720 * ScaleFactor
    RealWidth = int(w * ScaleFactor)
    RealHeight = int(h * ScaleFactor)
    menu_height = win32api.GetSystemMetrics(win32con.SM_CYSIZE)
    OffsetX = (rect[2] - w) / 2
    OffsetY = (rect[3] - menu_height - h - 1) / 2 + menu_height + 1
    logger.info(
        f"游戏窗口宽度为{w}，高度为{h},缩放因子为{ScaleFactor},实际宽度为{RealWidth},实际高度为{RealHeight}"
    )
    logger.info(f"宽度缩放比例为{WidthRatio},高度缩放比例为{HeightRatio}")
    logger.info(f"菜单栏高度为{menu_height},左上角偏移量为({OffsetX},{OffsetY})")
