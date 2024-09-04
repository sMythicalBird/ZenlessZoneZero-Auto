# -*- coding: utf-8 -*-
"""
@file:      fight_test
@time:      2024/8/29 18:16
@author:    sMythicalBird
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from PySide6.QtCore import Qt
from qfluentwidgets import (
    ComboBox,
    VBoxLayout,
    PushButton,
    ScrollArea,
)
from .cfg_card_group.designer_group import DesignerGroup
from schema.cfg.load import save_diy
from schema.cfg.info import char_list


class FightEditInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("FightEditInterface")
        self.scrollWidget = QWidget()
        self.vBoxLayout = VBoxLayout(self.scrollWidget)
        self.settingLabel = QLabel(self.tr("战斗设计"), self)
        self.settingLabel.setStyleSheet(
            "font: 33px 'Microsoft YaHei Light';"
            "background-color: transparent;"
            "color: black;"
        )
        self.designer_group = DesignerGroup(self.scrollWidget)
        self.select_label = QLabel("选择角色:", self)
        self.select_combobox = ComboBox(self)
        self.enter_btn = PushButton(self.tr("保存逻辑"), self)
        self.add_btn = PushButton(self.tr("增加配置"), self)
        self.delete_btn = PushButton(self.tr("减少配置"), self)
        self.init_ui()
        self.init_layout()

    def init_ui(self):
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setViewportMargins(0, 50, 0, 5)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        self.setStyleSheet("background-color: transparent;")

        self.select_label.setFixedWidth(100)
        self.select_combobox.setFixedWidth(80)
        self.select_combobox.addItems(char_list)

        self.enter_btn.setFixedWidth(100)
        self.add_btn.setFixedWidth(100)
        self.delete_btn.setFixedWidth(100)

    def init_layout(self):
        self.settingLabel.move(20, 20)
        # 添加控件
        h_layout_left = QHBoxLayout()
        h_layout_left.addWidget(self.select_label)
        h_layout_left.addWidget(self.select_combobox)
        h_layout_right = QHBoxLayout()
        h_layout_right.addWidget(self.enter_btn)
        h_layout_right.addWidget(self.add_btn)
        h_layout_right.addWidget(self.delete_btn)
        h_layout = QHBoxLayout()
        h_layout.addLayout(h_layout_left)
        h_layout.addLayout(h_layout_right)
        h_layout_left.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 靠左对齐
        h_layout_right.setAlignment(Qt.AlignmentFlag.AlignRight)  # 靠右对齐
        self.vBoxLayout.addLayout(h_layout)

        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 添加配置卡组信息
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)  # 设置卡组内容位置
        self.vBoxLayout.addWidget(self.designer_group)

        # 添加点击事件
        self.add_btn.clicked.connect(self.on_add_button_click)
        self.delete_btn.clicked.connect(self.on_delete_button_click)
        self.enter_btn.clicked.connect(self.on_enter_button_click)

    def on_add_button_click(self):
        self.designer_group.add_card()

    def on_delete_button_click(self):
        self.designer_group.remove_card()

    def on_enter_button_click(self):
        char_name = self.select_combobox.currentText()
        tactic_logic = self.designer_group.get_logic()
        save_diy(char_name, tactic_logic)
