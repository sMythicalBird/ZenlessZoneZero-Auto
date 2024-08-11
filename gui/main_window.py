# -*- coding: utf-8 -*-
""" 
@file:      main_window.py
@time:      2024/8/11 下午1:21
@author:    sMythicalBird
"""

from qfluentwidgets import MSFluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
from .home_interface import HomeInterface
from .setting_interface import SettingInterface


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle("主窗口")
        # 设置窗口尺寸
        self.resize(800, 600)
        # 其他初始化操作
        self.init_ui()
        self.initNavigation()

    def init_ui(self):
        # 在这里添加 UI 组件的初始化代码
        pass

    def initNavigation(self):
        # 添加侧边栏切换按钮
        self.addSubInterface(HomeInterface(), FIF.HOME, self.tr("主页"))

        # 添加设置按钮
        self.addSubInterface(
            SettingInterface(),
            FIF.SETTING,
            self.tr("设置"),
            position=NavigationItemPosition.BOTTOM,
        )
