# -*- coding: utf-8 -*-
""" 
@file:      link_card.py
@time:      2024/8/12 上午1:57
@author:    sMythicalBird
"""
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QFrame,
    QHBoxLayout,
)
from PySide6.QtGui import QDesktopServices, QPainter, QPainterPath, QColor
from qfluentwidgets import IconWidget, FluentIcon, TextWrap, SingleDirectionScrollArea


class LinkCard(QFrame):

    def __init__(self, icon, title, content, url, parent=None):
        super().__init__(parent=parent)
        self.url = QUrl(url)
        self.setFixedSize(120, 120)
        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 24, False)[0], self)
        self.contentLabel.setStyleSheet("font-size: 12px; font-weight: 400;")
        self.urlWidget = IconWidget(FluentIcon.LINK, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.init_ui()

    def init_ui(self):
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.iconWidget.setFixedSize(40, 40)
        self.urlWidget.setFixedSize(16, 16)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        self.urlWidget.move(100, 100)

        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        QDesktopServices.openUrl(self.url)


class LinkCardView(SingleDirectionScrollArea):
    """Link card view"""

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Orientation.Horizontal)
        self.view = QWidget(self)
        # self.setFixedSize(200, 250)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.hBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.hBoxLayout.setSpacing(5)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.view.setObjectName("view")
        # 设置view的样式表
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")  # 设置背景透明
        self.view.setStyleSheet("border: none;")  # 去掉边框

    def add_card(self, icon, title, content, url):
        """add link card"""
        card = LinkCard(icon, title, content, url, self.view)
        self.hBoxLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignLeft)
        # 调整view尺寸与card保持一致
        self.setFixedSize(card.width() + 12, card.height() + 12)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        painter.setRenderHints(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 10, 10)
        painter.setClipPath(path)
        painter.fillPath(path, QColor(255, 255, 255, 128))
