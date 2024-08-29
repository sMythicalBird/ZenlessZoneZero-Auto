# -*- coding: utf-8 -*-
"""
@file: config_interface.py
@time: 2024/8/11
@auther: sMythicalBird
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
    QSpacerItem,
    QPushButton,
)
from PySide6.QtCore import Qt
from qfluentwidgets import Pivot, ScrollArea, SettingCardGroup, FluentIcon

from .cfg_card_group import ZeroHoleGroup, FightGroup


class ConfigInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("ConfigInterface")  # 设置对象名称
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.change_btn = QPushButton(self.tr("保存配置"), self)
        self.settingLabel = QLabel(self.tr("配置"), self)
        self.settingLabel.setStyleSheet(
            "font: 33px 'Microsoft YaHei Light';"
            "background-color: transparent;"
            "color: black;"
        )
        # 初始化卡组
        self.zero_hole_group = ZeroHoleGroup(self.scrollWidget)
        self.fight_group = FightGroup(self.scrollWidget)
        # 初始化界面
        self.init_ui()
        self.init_layout()

    def init_ui(self):
        # 在这里添加 UI 组件的初始化代码
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setViewportMargins(0, 50, 0, 5)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        self.setStyleSheet("background-color: transparent;")

    def init_layout(self):
        self.settingLabel.move(36, 30)
        # 设置导航栏
        self.pivot.move(40, 80)
        # 设置卡组视图
        self.vBoxLayout.addWidget(self.stackedWidget, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(40, 80, 36, 0)  # 设置卡组内容位置
        # 添加卡组
        self.add_sub_group(self.zero_hole_group, "ZeroGroup", self.tr("零号空洞"))
        self.add_sub_group(self.fight_group, "FightGroup", self.tr("战斗配置"))
        # 设置卡组切换
        self.stackedWidget.currentChanged.connect(self.on_current_index_changed)
        self.pivot.setCurrentItem(self.stackedWidget.currentWidget().objectName())
        self.stackedWidget.setFixedHeight(
            self.stackedWidget.currentWidget().sizeHint().height()
        )
        # 设置参数更新键
        self.change_btn.setObjectName("change_btn")
        self.change_btn.move(200, 40)
        self.change_btn.setStyleSheet(
            "background-color: #d3d3d3;"
            "border-radius: 5px;"
            "font: 18px 'Microsoft YaHei';"
            "border: 1px solid black;"
            "padding: 3px;"
        )
        self.change_btn.clicked.connect(self.on_change_btn_clicked)

    def add_sub_group(self, widget: SettingCardGroup, object_name, text):
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

    def on_change_btn_clicked(self):
        self.zero_hole_group.update()
        self.fight_group.update()
