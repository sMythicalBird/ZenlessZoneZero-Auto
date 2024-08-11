# coding: utf-8
import os
import subprocess

from PySide6.QtCore import QUrl, QSize, Qt, QTimer
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QApplication

from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SplashScreen, NavigationBarPushButton, setThemeColor, \
    toggleTheme, InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon as FIF

from .config_interface import ConfigInterface
from ..card.messagebox_custom import MessageBoxSupport
from ..common.config import cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common import resource
from ..utils.InfoBarUtils import InfoBarUtils
from ..utils.gamePathUtils import detect_game_path, auto_path_detection


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # TODO: create sub interface
        # self.homeInterface = HomeInterface(self)
        self.configInterface = ConfigInterface(self)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()

        self._info_bar_timer = QTimer(self)  # 创建一个定时器对象
        self._info_bar_timer.setSingleShot(True)  # 确保住定时器只触发一次
        self._info_bar_timer.timeout.connect(self.reset_has_shown_info)  # 连接定时器超时信号到重置标志位的方法
        self._has_shown_info = False  # 添加一个标志变量来跟踪提示信息是否已经显示过

    def reset_has_shown_info(self):
        self._has_shown_info = False  # 在定时器超时后将标志位重置为 False

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def initNavigation(self):
        # self.navigationInterface.setAcrylicEnabled(True)

        # TODO: add navigation items
        # self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            'startGameButton',
            NavigationBarPushButton(FIF.PLAY, '启动游戏', isSelectable=False),
            self.startGame,
            NavigationItemPosition.BOTTOM)
        self.navigationInterface.addWidget(
            'themeButton',
            NavigationBarPushButton(FIF.BRUSH, '主题', isSelectable=False),
            lambda: toggleTheme(lazy=True),
            NavigationItemPosition.BOTTOM)
        self.navigationInterface.addWidget(
            'avatar',
            NavigationBarPushButton(FIF.HEART, '赞赏', isSelectable=False),
            lambda: MessageBoxSupport(
                '支持作者🥰',
                '此程序为免费开源项目，如果你付了钱请立刻退款\n如果喜欢本项目，可以微信赞赏送作者一杯咖啡☕\n您的支持就是作者开发和维护项目的动力🚀',
                'app/resource/images/256.jpg',
                self
            ).exec(),
            NavigationItemPosition.BOTTOM
        )
        # 配置
        self.addSubInterface(
            self.configInterface, FIF.SAVE, self.tr('配置'), FIF.SAVE, NavigationItemPosition.BOTTOM)

        self.splashScreen.finish()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/app/images/zero.png'))
        self.setWindowTitle('绝区零助手')
        # 设置窗口主题颜色为粉红色，并延迟应用以提高性能
        setThemeColor('#f18cb9', lazy=True)
        # 隐藏并禁用最大化按钮，禁止双击标题栏，禁用窗口大小调整
        # 禁用最大化
        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)
        # 设置窗口初始大小为960x640
        self.resize(960, 640)
        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def startGame(self):
        if auto_path_detection():
            # 检测游戏路径
            detect_game_path()
        try:
            """启动游戏"""
            if not os.path.exists(cfg.game_path.value):
                InfoBarUtils.start_fail(self)
                return False
            if not self._has_shown_info:
                self._has_shown_info = True
                self.show_info_bar()
                subprocess.Popen(self.game_path)
                InfoBarUtils.start_success(self)
                self._info_bar_timer.start(3000)
            return True
        except Exception as e:
            InfoBarUtils.start_error(self)
        return False
