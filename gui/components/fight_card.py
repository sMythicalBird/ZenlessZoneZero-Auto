# -*- coding: utf-8 -*-
"""
@file:      fight_card
@time:      2024/8/29 15:32
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
from schema.cfg.info import fight_logic_all, char_list


class FightSelBox(QWidget):
    def __init__(
        self,
        label: str,
        name: str,
        logic: str,
        items: list,
    ):
        super().__init__()
        # 创建标签和复选框
        self.label = QLabel(label)
        self.comboBox1 = QComboBox()
        self.comboBox1.setFixedWidth(150)  # 设置宽度为150
        self.comboBox2 = QComboBox()
        self.comboBox2.setFixedWidth(150)  # 设置宽度为150
        self.comboBox1.addItems(items)  # 添加选项

        # 创建水平布局
        self.hBoxLayout = QHBoxLayout()

        # 将标签和复选框添加到布局中
        self.hBoxLayout.addWidget(self.label)
        self.hBoxLayout.addWidget(self.comboBox1)
        self.hBoxLayout.addWidget(self.comboBox2)

        # 设置窗口的主布局
        self.setLayout(self.hBoxLayout)

        # 连接复选框的状态改变信号到槽函数并设置当前角色，更新当前角色技能选择框，并选择配置技能
        self.comboBox1.currentIndexChanged.connect(self.update_value_combo_box)
        self.comboBox1.setCurrentText(name)  # 设置当前角色
        self.update_value_combo_box()
        self.comboBox2.setCurrentText(logic)  # 设置当前技能

    def update_value_combo_box(self):
        name = self.comboBox1.currentText()
        values = fight_logic_all[name]["logic_dir"]
        self.comboBox2.clear()
        self.comboBox2.addItems(values)


class FightCfgCard(SettingCard):
    def __init__(
        self,
        name: str,
        icon: Union[str, QIcon, FluentIconBase],
        title,
        config: EventInfo,
        content=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent)
        self.name = name
        self.setFixedHeight(120)
        self.config = config
        self.fight_sel_box1 = FightSelBox(
            "1号位:", self.config.first.char, self.config.first.logic, char_list
        )
        self.fight_sel_box2 = FightSelBox(
            "2号位:", self.config.second.char, self.config.second.logic, char_list
        )
        self.fight_sel_box3 = FightSelBox(
            "3号位:", self.config.third.char, self.config.third.logic, char_list
        )
        self.init_layout()

    def init_layout(self):
        cfg_layout = QVBoxLayout()
        cfg_layout.addWidget(self.fight_sel_box1)
        cfg_layout.addWidget(self.fight_sel_box2)
        cfg_layout.addWidget(self.fight_sel_box3)
        self.hBoxLayout.addLayout(cfg_layout)

    # 获取当前值
    def get_value(self):
        self.config.first.char = self.fight_sel_box1.comboBox1.currentText()
        self.config.first.logic = self.fight_sel_box1.comboBox2.currentText()
        self.config.second.char = self.fight_sel_box2.comboBox1.currentText()
        self.config.second.logic = self.fight_sel_box2.comboBox2.currentText()
        self.config.third.char = self.fight_sel_box3.comboBox1.currentText()
        self.config.third.logic = self.fight_sel_box3.comboBox2.currentText()
