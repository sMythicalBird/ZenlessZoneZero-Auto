# -*- coding: utf-8 -*-
"""
@file:      update_group
@time:      2024/9/2 13:11
@author:    sMythicalBird
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import SettingCardGroup, FluentIcon
from ..components.designer_card import DesignerCard
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from .readme_group import BaseGroup


class UpdateGroup(BaseGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
