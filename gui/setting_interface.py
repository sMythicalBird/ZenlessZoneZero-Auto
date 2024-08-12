# -*- coding: utf-8 -*-
""" 
@file:      setting_interface.py
@time:      2024/8/11 下午4:53
@author:    sMythicalBird
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from qfluentwidgets import Pivot, ScrollArea


class SettingInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("SettingInterface")
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)

        self.settingLabel = QLabel(self.tr("配置"), self)
        self.settingLabel.setStyleSheet(
            "font: 33px 'Microsoft YaHei Light';"
            "background-color: transparent;"
            "color: black;"
        )
        # 初始化界面
        self.init_ui()

    def init_ui(self):
        # 在这里添加 UI 组件的初始化代码
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setViewportMargins(0, 140, 0, 5)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setObjectName("settingInterface")
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        self.setStyleSheet("background-color: transparent;")
