# -*- coding: utf-8 -*-
"""
@file:      readme_group
@time:      2024/9/2 12:16
@author:    sMythicalBird
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import SettingCardGroup, FluentIcon
from ..components.designer_card import DesignerCard
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class BaseGroup(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setSpacing(0)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(12)
        # 设置标签字体大小
        font = QFont()
        font.setPointSize(20)
        self.titleLabel.setFont(font)


class ReadmeGroup(BaseGroup):
    def __init__(self, parent=None):
        super().__init__(self.tr("说明"), parent)
