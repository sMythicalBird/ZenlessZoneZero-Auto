# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: control.py
@time: 2024/7/8 下午1:36
@author SuperLazyDog
"""
import time
from functools import wraps

from pydirectinput import (
    press,
    click,
    moveTo,
    mouseDown,
    mouseUp,
    keyDown,
    keyUp,
    scroll,
)

from .init import OffsetX, OffsetY, WidthRatio, HeightRatio


def reset_mouse(x=0, y=0):
    """
    重置鼠标位置装饰器
    :return:  装饰器
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            moveTo(OffsetX + x, OffsetY + y)

        return wrapper

    return decorator


class Control:
    offset_x = OffsetX
    offset_y = OffsetY

    def _pre(self, x, y):
        # x,y 进行缩放
        # x = x * WidthRatio
        # y = y * HeightRatio
        x = x
        y = y
        # x,y 进行偏移窗口边框偏移 x轴偏移量为 offset_x y轴偏移量为 offset_y
        # offset_y 包含了窗口标题栏的高度
        x += self.offset_x
        y += self.offset_y
        return x, y

    @reset_mouse()
    def click(
        self, x, y, clicks: int = 2, interval: float = 0.1, duration: float = 0.1
    ):
        x, y = self._pre(x, y)
        click(x, y, clicks=clicks, interval=interval, duration=duration)

    def move_to(self, x, y):
        x, y = self._pre(x, y)
        moveTo(x, y)

    @staticmethod
    def esc():
        press("esc", duration=0.1)

    @staticmethod
    def attack():
        mouseDown()
        time.sleep(0.1)
        mouseUp()

    # 向前跑ts
    @staticmethod
    def head(t):
        keyDown("w")
        keyDown("shift")
        time.sleep(t)
        keyUp("w")
        keyUp("shift")

    @staticmethod
    def scroll(clicks: int):
        scroll(clicks)


control = Control()
