# -*- coding: utf-8 -*-
"""
@file:      update_group
@time:      2024/9/2 13:11
@author:    sMythicalBird
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from qfluentwidgets import SettingCardGroup, FluentIcon
from ..components.designer_card import DesignerCard
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from .readme_group import BaseGroup
from ..api.check_update import check_update


class UpdateGroup(BaseGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_widget = QWidget(self)
        self.main_layout = QVBoxLayout()
        self.tip = QLabel("Tips:开发者最近在忙秋招，后续更新速度会放缓")
        self.warning_label = QLabel("更新需要同步github仓库，请确保网络畅通")
        self.check_btn = QPushButton("检查更新")
        self.check_label = QLabel("")

        self.init_ui()
        self.init_layout()

    def init_ui(self):
        self.check_btn.setFixedSize(100, 30)

        self.check_btn.clicked.connect(self.check_update)

    def init_layout(self):
        self.main_layout.addWidget(self.tip)
        self.main_layout.addWidget(self.warning_label)
        self.main_layout.addWidget(self.check_btn)
        self.main_layout.addWidget(self.check_label)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 10, 0, 0)
        self.vBoxLayout.addLayout(self.main_layout)

    def check_update(self):
        self.check_label.setText("检查中...")
        num, res = check_update()
        self.check_label.setText(res)
        if num == 1:
            print("有更新")
