# -*- coding: utf-8 -*-
""" 
@file:      home_interface.py
@time:      2024/8/11 下午4:41
@author:    sMythicalBird
"""
from qfluentwidgets import ScrollArea, FluentIcon as FIF


class HomeInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("HomeInterface")
        self.init_ui()

    def init_ui(self):
        # 在这里添加 UI 组件的初始化代码
        pass
