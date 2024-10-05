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
    setTheme,
    Theme,
)
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPainterPath, QImage, QFont

from .components import LinkCardView, TaskCardView
from PIL import Image

import numpy as np

from .init_cfg import home_img_path
from start_task import start_task


class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(372)  # 初始高度，后续会调整
        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = TitleLabel(f"绝区零自动化v2.4.1", self)
        self.galleryLabel.setStyleSheet("color: #FFFFFF;")
        font = QFont("MiSans", 24, QFont.Weight.Bold)
        self.galleryLabel.setFont(font)

        # 获取背景图片
        self.img = Image.open(str(home_img_path / "bg.png"))

        self.banner = None
        self.path = None

        # 添加链接卡片
        self.link_card_view1 = LinkCardView(self)
        self.link_card_view1.setContentsMargins(10, 10, 10, 10)
        self.link_card_view2 = LinkCardView(self)
        self.link_card_view2.setContentsMargins(10, 10, 10, 10)

        # 添加垂直布局
        link_card_layout = QHBoxLayout()
        link_card_layout.addWidget(self.link_card_view1)
        link_card_layout.addWidget(self.link_card_view2)
        link_card_layout.setSpacing(10)
        link_card_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
        )

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addLayout(link_card_layout)

        self.vBoxLayout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )

        self.link_card_view1.add_card(
            FluentIcon.GITHUB,
            self.tr("GitHub repo"),
            self.tr("喜欢就给个星星吧"),
            "https://github.com/sMythicalBird/ZenlessZoneZero-Auto",
        )
        self.link_card_view2.add_card(
            FluentIcon.GLOBE,
            self.tr("项目主页"),
            self.tr("自动化框架介绍"),
            "https://fairy.autoscript.site/zh/",
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

    def load_samples(self):
        # 添加横幅小组件
        banner = BannerWidget(self)
        self.vBoxLayout.addWidget(banner)

        # 添加功能组件
        task_card_view = TaskCardView(self.tr("任务 >"), self.view)
        task_card_view.add_task_card(
            icon=str(home_img_path / "zero.jpg"),
            title="零号空洞",
            action=lambda: start_task("zero"),
        )
        task_card_view.add_task_card(
            icon=str(home_img_path / "money.jpg"),
            title="拿命验收",
            action=lambda: start_task("money"),
        )
        task_card_view.add_task_card(
            icon=str(home_img_path / "fight.jpg"),
            title="战斗任务",
            action=lambda: start_task("fight"),
        )
        self.vBoxLayout.addWidget(task_card_view)
