# -*- coding: utf-8 -*-
""" 
@file:      setting_interface.py
@time:      2024/8/11 下午4:53
@author:    sMythicalBird
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from qfluentwidgets import Pivot, ScrollArea, SettingCardGroup, FluentIcon
from .components import ComboBoxSettingCard1


class SettingInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("SettingInterface")

    def init_ui(self):
        # 在这里添加 UI 组件的初始化代码
        pass
