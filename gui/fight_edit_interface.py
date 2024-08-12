# -*- coding: utf-8 -*-
"""
@file: fight_edit_interface.py
@time: 2024/8/12
@auther: sMythicalBird
"""
from qfluentwidgets import ScrollArea


class FightEditInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("FightEditInterface")
        self.init_ui()

    def init_ui(self):
        # 在这里添加 UI 组件的初始化代码
        pass
