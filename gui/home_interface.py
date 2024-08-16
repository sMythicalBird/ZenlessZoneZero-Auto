# -*- coding: utf-8 -*-
""" 
@file:      home_interface.py
@time:      2024/8/11 下午4:41
@author:    sMythicalBird
"""
from qfluentwidgets import (
    ScrollArea,
    FluentIcon,
    TitleLabel,
    LargeTitleLabel,
    qconfig,
    setTheme,
    Theme,
)
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPainterPath, QImage, QFont

from .components import LinkCardView, TaskCardView
from PIL import Image

import numpy as np

from .init_cfg import home_img_path


class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(570)  # 初始高度，后续会调整
        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = TitleLabel(f"绝区零自动化", self)
        font = QFont("MiSans", 30, QFont.Bold)
        self.galleryLabel.setFont(font)
        setTheme(Theme.AUTO)

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # 阴影模糊半径
        shadow.setColor(Qt.GlobalColor.black)  # 阴影颜色
        shadow.setOffset(1.2, 1.2)  # 阴影偏移量

        # 将阴影效果应用于小部件
        self.galleryLabel.setGraphicsEffect(shadow)
        self.galleryLabel.setObjectName("galleryLabel")

        # 获取背景图片
        self.img = Image.open(str(home_img_path / "bg.jpg"))

        self.banner = None
        self.path = None

        # 添加链接卡片
        self.link_card_view = LinkCardView(self)
        self.link_card_view.setContentsMargins(0, 0, 0, 36)
        # 添加垂直布局
        link_card_layout = QHBoxLayout()
        link_card_layout.addWidget(self.link_card_view)
        link_card_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
        )

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addLayout(link_card_layout)
        self.vBoxLayout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )

        self.link_card_view.add_card(
            FluentIcon.GITHUB,
            self.tr("GitHub repo"),
            self.tr("喜欢就给个星星吧\n拜托求求你啦|･ω･)"),
            "https://github.com/sMythicalBird/ZenlessZoneZero-Auto",
        )

    # 画笔绘制背景
    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing
        )
        if not self.banner or not self.path:
            crop_area = (0, 0, self.img.width, self.img.height)
            cropped_img = self.img.crop(crop_area)
            self.img_data = np.array(cropped_img.convert("RGBA"))
            height, width, channels = self.img_data.shape
            bytes_per_line = channels * width
            self.banner = QImage(
                self.img_data.data,
                width,
                height,
                bytes_per_line,
                QImage.Format.Format_RGBA8888,
            )

            path = QPainterPath()
            path.addRoundedRect(0, 0, width + 50, height + 50, 30, 30)
            self.path = path.simplified()

        painter.setClipPath(self.path)
        painter.drawImage(self.rect(), self.banner)

    # 每次调整窗口大小时重新计算高度
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 重新计算高度
        new_height = self.size().width() * self.img.height // self.img.width
        self.setFixedHeight(new_height)


class HomeInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        # 添加窗口和布局
        self.view = QWidget(self)
        # 给view设置布局
        self.vBoxLayout = QVBoxLayout(self.view)
        # 初始化窗口界面
        self.init_ui()
        # 初始化窗口组件
        self.load_samples()

    def init_ui(self):
        self.setObjectName("HomeInterface")
        self.view.setObjectName("view")
        # 将view设为中心部件
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        # 设置布局格式 添加banner
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(25)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # 设置view的样式表去掉边框
        self.view.setStyleSheet("border: none;")

    def test_fun1(self, task_name: str):
        print(task_name)

    def test_fun2(self, task_name: str):
        print(task_name)

    def load_samples(self):
        # 添加横幅小组件
        banner = BannerWidget(self)
        self.vBoxLayout.addWidget(banner)

        # 添加功能组件
        task_card_view = TaskCardView(self.tr("任务 >"), self.view)
        task_card_view.add_task_card(
            icon=str(home_img_path / "安比.jpg"),
            title="测试-sig",
            action=lambda: self.test_fun1("测试-sig"),
        )
        task_card_view.add_task_card(
            icon=str(home_img_path / "安比.jpg"),
            title="测试-mul",
            action={
                "test1": lambda: self.test_fun1("测试-mul-1"),
                "test2": lambda: self.test_fun2("测试-mul-2"),
            },
        )
        self.vBoxLayout.addWidget(task_card_view)
