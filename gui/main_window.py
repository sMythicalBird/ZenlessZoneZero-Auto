# -*- coding: utf-8 -*-
""" 
@file:      main_window.py
@time:      2024/8/11 下午1:21
@author:    sMythicalBird
"""

from qfluentwidgets import MSFluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon
from .home_interface import HomeInterface
from .setting_interface import SettingInterface
from .config_interface import ConfigInterface
from .api.check_update import check_update


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        # 初始化窗口ui
        self.init_ui()
        # 初始化窗口导航
        self.init_navigation()
        # 检查更新
        check_update()

    def init_ui(self):
        self.setWindowTitle("主窗口")
        self.resize(1080, 720)

    def init_navigation(self):
        # 添加主页导航页
        self.addSubInterface(HomeInterface(), FluentIcon.HOME, self.tr("主页"))

        # 添加配置导航页
        self.addSubInterface(
            ConfigInterface(),
            FluentIcon.SAVE,
            self.tr("配置"),
            position=NavigationItemPosition.BOTTOM,
        )

        # 添加设置导航页
        self.addSubInterface(
            SettingInterface(),
            FluentIcon.SETTING,
            self.tr("设置"),
            position=NavigationItemPosition.BOTTOM,
        )
