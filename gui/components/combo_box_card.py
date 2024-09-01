# -*- coding: utf-8 -*-
"""
@file: combo_box_card.py
@time: 2024/8/12
@auther: sMythicalBird
"""
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Qt
from qfluentwidgets import SettingCard, FluentIconBase, ComboBox
from typing import Union
from schema.cfg.info import zero_cfg
from ..base.MultiSelectComboBox import MultiSelectComboBox

data = {
    "旧都列车": {1: "外围", 2: "前线", 3: "内部", 4: "腹地", 5: "核心"},
    "施工废墟": {1: "前线", 2: "内部", 3: "腹地", 4: "核心"},
    "巨厦": {1: "内部", 2: "腹地", 3: "核心"},
}


class ZeroLevelSelectCard(SettingCard):
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
        # 添加布局
        self.comboBox1 = ComboBox(self)
        self.comboBox2 = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox1, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.comboBox2, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

        # 添加选项
        self.comboBox1.addItems(data.keys())
        self.comboBox1.currentIndexChanged.connect(self.update_value_combo_box)
        self.comboBox1.setCurrentText(zero_cfg.targetMap.Zone)
        self.update_value_combo_box(zero_cfg.targetMap.zone - 1)
        self.comboBox2.setCurrentText(zero_cfg.targetMap.Level)

    def update_value_combo_box(self, index):
        key = self.comboBox1.itemText(index)
        values = data[key].values()
        self.comboBox2.clear()
        self.comboBox2.addItems(values)


class ModeSelectCard(SettingCard):
    def __init__(
        self,
        name: str,
        icon: Union[str, QIcon, FluentIconBase],
        title,
        index: int,
        texts: list[str],
        content=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent)
        self.name = name
        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.comboBox.addItems(texts)
        self.comboBox.setCurrentText(texts[index])


class NumTextCard(SettingCard):
    def __init__(
        self,
        name: str,
        icon: Union[str, QIcon, FluentIconBase],
        title,
        init_value: int,
        content=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent)
        self.name = name
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setValidator(QIntValidator())  # 只能输入整数
        self.hBoxLayout.addWidget(self.lineEdit, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.lineEdit.setText(str(init_value))

    # 获取当前值
    def get_value(self):
        return int(self.lineEdit.text())


class MultiSelectCard(SettingCard):
    def __init__(
        self,
        name: str,
        icon: Union[str, QIcon, FluentIconBase],
        title,
        selected_items: list[str],
        options: list[str],
        max_sel_num: int = 10000,
        size: (int, int) = None,
        content=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent)
        self.name = name
        self.multiSelectComboBox = MultiSelectComboBox(
            selected_items, options, max_sel_num, self
        )
        self.multiSelectComboBox.set_width(size[0])
        self.multiSelectComboBox.set_height(size[1])
        self.hBoxLayout.addWidget(
            self.multiSelectComboBox, 0, Qt.AlignmentFlag.AlignRight
        )
        self.hBoxLayout.addSpacing(16)

    def get_value(self):
        return self.multiSelectComboBox.selected_items  # 获取当前选中的选项
