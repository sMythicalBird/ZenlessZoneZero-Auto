# -*- coding: utf-8 -*-
"""
@file:      designer_group
@time:      2024/8/29 18:47
@author:    sMythicalBird
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import SettingCardGroup, FluentIcon
from ..components.designer_card import DesignerCard
from PySide6.QtCore import Qt


class DesignerGroup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setSpacing(0)

        self.vBoxLayout.addSpacing(12)

        self.card_num = 0
        self.card_list = []
        self.init_card()

    def init_card(self):
        self.add_card()  # 添加一个配置卡片

    def add_card(self):
        self.card_num += 1
        card = DesignerCard(
            f"cfg_{self.card_num}",
            FluentIcon.ALIGNMENT,
            self.tr(f"配置_{self.card_num}"),
            parent=self,
        )
        self.card_list.append(card)
        card.setParent(self)
        self.vBoxLayout.addWidget(card)
        self.adjustSize()

    def remove_card(self):
        if self.card_num > 0:
            self.card_num -= 1
            self.remove_setting_card(self.card_list[-1])
            self.adjustSize()
            self.update()  # 刷新界面
            self.repaint()  # 确保界面重绘

    def remove_setting_card(self, cur_card: DesignerCard):
        self.card_list.remove(cur_card)
        self.vBoxLayout.removeWidget(cur_card)
        cur_card.setParent(None)
        cur_card.deleteLater()  # 删除防止内存泄漏

    def adjustSize(self):
        h = self.card_num * 50 + 46
        self.resize(self.width(), h)

    # 返回配置信息
    def get_logic(self):
        tactic_logic = []
        for card in self.card_list:
            tactic_logic.append(
                {
                    "key": card.info_designer1.edit.text(),
                    "type": card.info_designer2.comboBox.currentText(),
                    "duration": float(card.info_designer3.edit.text()),
                    "delay": float(card.info_designer4.edit.text()),
                    "repeat": int(card.info_designer5.comboBox.currentText()),
                }
            )
        return tactic_logic
