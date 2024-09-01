# -*- coding: utf-8 -*-
"""
@file: task_card.py
@time: 2024/8/12
@auther: sMythicalBird
"""
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt
from qfluentwidgets import (
    CardWidget,
    IconWidget,
    TeachingTip,
    RoundMenu,
    InfoBarIcon,
    TeachingTipTailPosition,
    FlowLayout,
)
import base64


class TaskCard(CardWidget):
    """Sample card"""

    def __init__(self, icon, title, action, parent=None):
        super().__init__(parent=parent)

        self.action = action
        # 设置卡片背景图
        self.iconWidget = IconWidget(icon, self)
        self.iconOpacityEffect = QGraphicsOpacityEffect(self)
        self.iconOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.iconWidget.setGraphicsEffect(self.iconOpacityEffect)

        # 设置标签文字样式
        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: 500;")
        self.titleOpacityEffect = QGraphicsOpacityEffect(self)
        self.titleOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.titleLabel.setGraphicsEffect(self.titleOpacityEffect)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 文字居中对齐

        # 设置卡片和图片视图宽高
        self.setFixedSize(130, 160)
        self.iconWidget.setFixedSize(110, 110)

        # 调整布局
        self.hBoxLayout = QVBoxLayout(self)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addWidget(
            self.iconWidget, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # 垂直中心对齐
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(
            self.titleLabel, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        self.vBoxLayout.addStretch(1)
        self.titleLabel.setObjectName("titleLabel")

    def show_bottom_teaching_tip(self):
        TeachingTip.create(
            target=self.iconWidget,
            icon=InfoBarIcon.SUCCESS,
            title="开始执行(＾∀＾●)",
            content="",
            isClosable=False,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self,
        )

    def create_menu(self, pos):
        menu = RoundMenu(parent=self)

        def create_triggered_function(task):
            def triggered_function():
                self.show_bottom_teaching_tip()
                try:
                    task()
                except Exception as e:
                    # log.warning(f"执行失败：{e}")
                    pass

            return triggered_function

        for index, (key, value) in enumerate(self.action.items()):
            action = QAction(key, self)
            action.triggered.connect(create_triggered_function(value))
            menu.addAction(action)
            if index != len(self.action) - 1:  # 检查是否是最后一个键值对
                menu.addSeparator()
        menu.exec(pos, ani=True)

    # 重载鼠标释放事件
    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        try:
            if callable(self.action):  # 传递进来的是一个函数，检测到鼠标释放则直接执行
                self.show_bottom_teaching_tip()
                self.action()
            elif isinstance(self.action, dict):  # 当传递进来的是一个函数列表
                self.create_menu(e.globalPos())  # 运行程序
        except Exception as e:
            pass

    # 重载鼠标进入事件
    def enterEvent(self, event):
        super().enterEvent(event)
        self.iconOpacityEffect.setOpacity(0.75)
        self.titleOpacityEffect.setOpacity(0.75)
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # 设置鼠标指针为手形

    # 重载鼠标离开事件
    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.iconOpacityEffect.setOpacity(1)
        self.titleOpacityEffect.setOpacity(1)
        self.setCursor(Qt.CursorShape.ArrowCursor)  # 恢复鼠标指针的默认形状


class TaskCardView(QWidget):
    """Sample card view"""

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.vBoxLayout.setContentsMargins(20, 0, 20, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.titleLabel.setObjectName("viewTitleLabel")

    def add_task_card(self, icon, title, action):
        """add sample card"""
        card = TaskCard(icon, title, action, self)
        self.flowLayout.addWidget(card)
