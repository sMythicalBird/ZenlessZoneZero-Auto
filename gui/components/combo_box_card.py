# -*- coding: utf-8 -*-
"""
@file: combo_box_card.py
@time: 2024/8/12
@auther: sMythicalBird
"""
from PySide6.QtWidgets import QComboBox, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from qfluentwidgets import SettingCard, FluentIconBase, ComboBox
from typing import Union


#
class ComboBoxSettingCard1(SettingCard):
    """Setting card with a combo box"""

    def __init__(
        self,
        name: str,
        icon: Union[str, QIcon, FluentIconBase],
        title,
        content=None,
        texts=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent)
        self.name = name
        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)
