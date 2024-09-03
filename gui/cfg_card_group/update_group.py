# -*- coding: utf-8 -*-
"""
@file:      update_group
@time:      2024/9/2 13:11
@author:    sMythicalBird
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QApplication,
)

from .readme_group import BaseGroup
from ..api.check_update import check_update, download


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
            download()
            self.show_restart_dialog()

    def show_restart_dialog(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("更新已下载，是否立即重启程序？")
        msg_box.setWindowTitle("更新完成")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        msg_box.buttonClicked.connect(self.handle_restart)
        msg_box.exec()

    def handle_restart(self, button):
        if button.text() == "OK":
            self.restart_program()

    def restart_program(self):
        QApplication.quit()
