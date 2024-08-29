# -*- coding: utf-8 -*-
"""
@file:      designer_card
@time:      2024/8/29 18:45
@author:    sMythicalBird
"""

from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QWidget,
    QLabel,
)
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Qt
from qfluentwidgets import SettingCard, FluentIconBase, ComboBox
from typing import Union
from schema.cfg.fight_info import EventInfo


class CombiningWidget1(QWidget):
    def __init__(self, name: str, default_value="", width=50):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.label = QLabel(name)
        self.edit = QLineEdit()
        self.edit.setFixedWidth(width)
        self.edit.setPlaceholderText(default_value)
        self.edit.setStyleSheet("QLineEdit { border: 1px solid lightgray; }")
        self.hBoxLayout.addWidget(self.label)
        self.hBoxLayout.addWidget(self.edit)


class CombiningWidget2(QWidget):
    def __init__(self, name: str, items=None, width=50):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.label = QLabel(name)
        self.comboBox = QComboBox()
        self.comboBox.setFixedWidth(width)
        self.comboBox.addItems(items)
        self.hBoxLayout.addWidget(self.label)
        self.hBoxLayout.addWidget(self.comboBox)


class DesignerCard(SettingCard):
    def __init__(
        self,
        name: str,
        icon: Union[str, QIcon, FluentIconBase],
        title,
        content=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent)
        self.name = name
        self.info_designer1 = CombiningWidget1("key", "any_key", 80)
        self.info_designer2 = CombiningWidget2("type", ["press", "down", "up"], 80)
        self.info_designer3 = CombiningWidget1("duration(s)", "0.2")
        self.info_designer4 = CombiningWidget1("delay(s)", "0.2")
        self.info_designer5 = CombiningWidget2("repeat", [str(i) for i in range(1, 5)])

        # 将标签和复选框添加到布局中
        self.hBoxLayout.addWidget(self.info_designer1)
        self.hBoxLayout.addWidget(self.info_designer2)
        self.hBoxLayout.addWidget(self.info_designer3)
        self.hBoxLayout.addWidget(self.info_designer4)
        self.hBoxLayout.addWidget(self.info_designer5)
        self.hBoxLayout.addSpacing(16)
