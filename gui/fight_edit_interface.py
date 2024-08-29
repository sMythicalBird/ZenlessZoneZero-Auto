# -*- coding: utf-8 -*-
"""
@file:      fight_test
@time:      2024/8/29 18:16
@author:    sMythicalBird
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame, QSizePolicy, QLabel

from PySide6.QtCore import Qt
from qfluentwidgets import (
    ComboBox,
    VBoxLayout,
    PushButton,
    TitleLabel,
    BodyLabel,
    SpinBox,
    ExpandGroupSettingCard,
    FluentIcon,
    LineEdit,
    DoubleSpinBox,
    ScrollArea,
)
from .cfg_card_group.designer_group import DesignerGroup


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

        self.enter_btn.setFixedWidth(100)
        self.add_btn.setFixedWidth(100)
        self.delete_btn.setFixedWidth(100)

    def init_layout(self):
        self.settingLabel.move(20, 20)

        # 添加按钮
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.enter_btn)
        h_layout.addWidget(self.add_btn)
        h_layout.addWidget(self.delete_btn)
        h_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 设置布局靠左对齐
        self.vBoxLayout.addLayout(h_layout)

        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 添加配置卡组信息
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)  # 设置卡组内容位置
        # self.designer_group.titleLabel.hide()  # 隐藏卡组标题
        self.vBoxLayout.addWidget(self.designer_group)

        # 添加点击事件
        self.add_btn.clicked.connect(self.on_add_button_click)
        self.delete_btn.clicked.connect(self.on_delete_button_click)

    def on_add_button_click(self):
        self.designer_group.add_card()

    def on_delete_button_click(self):
        self.designer_group.remove_card()
