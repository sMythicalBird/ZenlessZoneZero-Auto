# -*- coding: utf-8 -*-
""" 
@file:      setting_interface.py
@time:      2024/8/11 下午4:53
@author:    sMythicalBird
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from qfluentwidgets import Pivot, ScrollArea, SettingCardGroup, FluentIcon
from .components import ComboBoxSettingCard1


class SettingInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("SettingInterface")
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)

        self.settingLabel = QLabel(self.tr("配置"), self)
        self.settingLabel.setStyleSheet(
            "font: 33px 'Microsoft YaHei Light';"
            "background-color: transparent;"
            "color: black;"
        )
        # 初始化卡组
        self.ZeroGroup = SettingCardGroup(self.tr("零号空洞"), self.scrollWidget)
        self.OneGroup = SettingCardGroup(self.tr("战斗"), self.scrollWidget)
        # 初始化界面
        self.init_ui()
        self.init_card()
        self.init_layout()

    def init_ui(self):
        # 在这里添加 UI 组件的初始化代码
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setViewportMargins(0, 50, 0, 5)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setObjectName("settingInterface")
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        self.setStyleSheet("background-color: transparent;")

    def init_card(self):
        # 在这里添加卡片的初始化代码
        self.instanceTypeCard = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            None,
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.instanceTypeCard2 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("战斗"),
            None,
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )

    def init_layout(self):
        self.ZeroGroup.addSettingCard(self.instanceTypeCard)
        self.OneGroup.addSettingCard(self.instanceTypeCard2)

        self.settingLabel.move(36, 30)
        self.pivot.move(40, 80)

        self.vBoxLayout.addWidget(self.stackedWidget, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(40, 80, 36, 0)

        self.add_sub_page(self.ZeroGroup, "ZeroGroup", self.tr("零号空洞"))
        self.add_sub_page(self.OneGroup, "OneGroup", self.tr("战斗"))

        self.stackedWidget.currentChanged.connect(self.on_current_index_changed)
        self.pivot.setCurrentItem(self.stackedWidget.currentWidget().objectName())
        self.stackedWidget.setFixedHeight(
            self.stackedWidget.currentWidget().sizeHint().height()
        )

    def add_sub_page(self, widget: SettingCardGroup, object_name, text):
        def remove_spacing(layout):
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if isinstance(item, QSpacerItem):
                    layout.removeItem(item)
                    break

        remove_spacing(widget.layout())
        widget.titleLabel.hide()

        widget.setObjectName(object_name)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=object_name,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    # 页面切换
    def on_current_index_changed(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())

        self.verticalScrollBar().setValue(0)
        self.stackedWidget.setFixedHeight(
            self.stackedWidget.currentWidget().sizeHint().height()
        )
