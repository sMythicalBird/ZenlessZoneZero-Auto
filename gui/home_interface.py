# -*- coding: utf-8 -*-
""" 
@file:      home_interface.py
@time:      2024/8/11 下午4:41
@author:    sMythicalBird
"""
from qfluentwidgets import ScrollArea, FluentIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPainterPath, QImage

from .init_cfg import home_img_path
from PIL import Image

import numpy as np


class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(320)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel(f'绝区零自动化', self)
        self.galleryLabel.setStyleSheet("color: black; font-size: 50px; font-weight: 600; "
                                        "font-family: 'Microsoft YaHei';")

        # 创建阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # 阴影模糊半径
        shadow.setColor(Qt.black)  # 阴影颜色
        shadow.setOffset(1.2, 1.2)  # 阴影偏移量

        # 将阴影效果应用于小部件
        self.galleryLabel.setGraphicsEffect(shadow)
        self.galleryLabel.setObjectName('galleryLabel')

        # 获取背景图片
        self.img = Image.open(str(home_img_path / 'bg.png'))
        self.banner = None
        self.path = None

        # # 添加链接卡片
        # self.linkCardView = LinkCardView(self)
        # self.linkCardView.setContentsMargins(0, 0, 0, 36)
        # 添加垂直布局
        # linkCardLayout = QHBoxLayout()
        # linkCardLayout.addWidget(self.linkCardView)
        # linkCardLayout.setAlignment(Qt.AlignBottom)


        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        # self.vBoxLayout.addLayout(linkCardLayout)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # self.linkCardView.addCard(
        #     FluentIcon.GITHUB,
        #     self.tr('GitHub repo'),
        #     self.tr('喜欢就给个星星吧\n拜托求求你啦|･ω･)'),
        #     "https://github.com/sMythicalBird/ZenlessZoneZero-Auto",
        # )

    # 画笔绘制背景
    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)

        if not self.banner or not self.path:
            # 获取图片归一化高度进行裁剪
            image_height = self.img.width * self.height() // self.width()
            crop_area = (0, 0, self.img.width, image_height)
            cropped_img = self.img.crop(crop_area)
            img_data = np.array(cropped_img.convert("RGBA"))  # Ensure the image is in RGBA format
            height, width, channels = img_data.shape
            bytes_per_line = channels * width
            self.banner = QImage(img_data.data, width, height, bytes_per_line, QImage.Format.Format_RGBA8888)

            path = QPainterPath()
            path.addRoundedRect(0, 0, width + 50, height + 50, 10, 10)  # 10 is the radius for corners
            self.path = path.simplified()

        painter.setClipPath(self.path)
        painter.drawImage(self.rect(), self.banner)


class HomeInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        # 添加窗口和布局
        self.view = QWidget(self)
        # 给view设置布局
        self.vBoxLayout = QVBoxLayout(self.view)
        # 添加横幅小组件
        self.banner = BannerWidget(self)
        # 初始化窗口界面
        self.init_ui()

    def init_ui(self):
        self.setObjectName("HomeInterface")
        self.view.setObjectName('view')
        # 将view设为中心部件
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        # 设置布局格式 添加banner
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(25)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)


