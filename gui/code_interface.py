# -*- coding: utf-8 -*-
"""
@file:      code_interface
@time:      2024/8/30 14:22
@author:    sMythicalBird
"""

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
)

from PySide6.QtCore import Qt
from qfluentwidgets import (
    ScrollArea,
)
from start_task import redemption_code
from schema.cfg.daily import code_list


class CodeInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("CodeInterface")
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.settingLabel = QLabel(self.tr("兑换码兑换"), self)
        self.settingLabel.setStyleSheet(
            "font: 33px 'Microsoft YaHei Light';"
            "background-color: transparent;"
            "color: black;"
        )
        self.text_edit = QTextEdit(self)
        self.enter_btn = QPushButton("兑换", self)
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
        self.text_edit.setPlaceholderText("在这里输入兑换码")
        self.text_edit.setStyleSheet("QTextEdit { border: 1px solid lightgray; }")

        # 文本框样式
        self.text_edit.setFixedSize(400, 200)

    def init_layout(self):
        self.settingLabel.move(20, 20)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)  # 设置卡组内容位置
        self.vBoxLayout.addWidget(self.text_edit)

        # 添加确认按钮
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.enter_btn)
        h_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vBoxLayout.addLayout(h_layout)

        # 按钮设置
        self.enter_btn.clicked.connect(self.on_enter_btn_clicked)

    def on_enter_btn_clicked(self):
        text = self.text_edit.toPlainText()
        text_list = text.split()  # 按空格或换行符分割
        # 保存兑换码列表
        code_list.code_value = text_list
        code_list.code_cnt = len(text_list)
        redemption_code()
