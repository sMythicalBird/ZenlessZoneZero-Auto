# -*- coding: utf-8 -*-
"""
@file: config_interface.py
@time: 2024/8/11
@auther: sMythicalBird
"""
from qfluentwidgets import ScrollArea, FluentIcon as FIF


class ConfigInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("ConfigInterface")
        self.init_ui()

    def init_ui(self):
        # 在这里添加 UI 组件的初始化代码
        pass