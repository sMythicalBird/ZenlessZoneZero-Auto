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
from schema.cfg.info import zero_cfg

data = {
    "旧都列车": {1: "外围", 2: "前线", 3: "内部", 4: "腹地", 5: "核心"},
    "施工废墟": {1: "前线", 2: "内部", 3: "腹地", 4: "核心"},
    "巨骸大厦": {1: "内部", 2: "腹地", 3: "核心"},
}


class ChoiceSettingCard(SettingCard):
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
        # 添加布局
        self.comboBox1 = ComboBox(self)
        self.comboBox2 = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox1, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.comboBox2, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

        # 添加选项
        self.comboBox1.addItems(data.keys())
        self.comboBox1.currentIndexChanged.connect(self.update_value_combo_box)
        print(zero_cfg.targetMap.Zone)
        self.comboBox1.setCurrentText(zero_cfg.targetMap.Zone)
        self.update_value_combo_box(zero_cfg.targetMap.zone - 1)
        self.comboBox2.setCurrentText(zero_cfg.targetMap.Level)

    def update_value_combo_box(self, index):
        key = self.comboBox1.itemText(index)
        values = data[key].values()
        self.comboBox2.clear()
        self.comboBox2.addItems(values)


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
        for text, option in zip(texts, texts):
            self.comboBox.addItem(text)

        self.comboBox.setCurrentText(texts[0])
