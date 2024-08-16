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
    moveRel,
)
import pydirectinput

from .init import OffsetX, OffsetY

# 禁用安全模式
pydirectinput.FAILSAFE = False


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
        self,
        x: int,
        y: int,
        clicks: int = 2,
        interval: float = 0.05,
        duration: float = 0.05,
    ):
        x, y = self._pre(x, y)
        click(x, y, clicks=clicks, interval=interval, duration=duration)

    def move_to(self, x, y):
        x, y = self._pre(x, y)
        moveTo(x, y)

    @staticmethod
    def move_at(x1, y1, x2, y2):
        moveTo(x1, y1)
        time.sleep(0.1)
        mouseDown()
        time.sleep(0.1)
        moveTo(x2, y2)
        time.sleep(0.1)
        mouseUp()
        time.sleep(0.3)

    @staticmethod
    def esc():
        press("esc", duration=0.1)

    # 向前跑ts
    @staticmethod
    def head(t):
        keyDown("w")
        time.sleep(t)
        keyUp("w")

    @staticmethod
    def scroll(clicks: int):
        scroll(clicks)

    @staticmethod
    def move_rel(x, y):
        moveRel(x, y, relative=True)

    @staticmethod
    def press(key, duration=0.05):
        press(key, duration=duration)


control = Control()
