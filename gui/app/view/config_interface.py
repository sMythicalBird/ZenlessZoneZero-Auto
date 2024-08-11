import os

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QStackedWidget, QSpacerItem

from qfluentwidgets import FluentIcon as FIF, ComboBoxSettingCard, SwitchSettingCard, qconfig
from qfluentwidgets import SettingCardGroup, PushSettingCard, ScrollArea, InfoBar, PrimaryPushSettingCard, Pivot
from ..card.CustomComboBoxSettingCard import CustomComboBoxSettingCard, CustomComboBoxSettingCard1
from ..card.pushsettingcard1 import PushSettingCardEval
from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..utils.InfoBarUtils import InfoBarUtils
from ..utils.configUtils import generateConfigFile
from ..watcher.config_watcher import ConfigWatcher
from ..watcher.key_watcher import KeyAndValWatcher


class ConfigInterface(ScrollArea):
    def __init__(self, parent=None):
        """
        初始化视图对象。

        :param parent: 父窗口对象，默认为None。
        """
        super().__init__(parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self._info_bar_timer = QTimer(self)
        self._info_bar_timer.setSingleShot(True)
        self._info_bar_timer.timeout.connect(self.reset_has_shown_info)
        self._has_shown_info = False
        self.configSettingLabel = QLabel(self.tr("配置"), self)
        self.configSettingLabel.move(36, 50)
        self.infoBarPosition = self.configSettingLabel.parent()
        self.__initWidget()
        self.__initCard()
        self.__initLayout()
        self.__connectSignalToSlot()
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config_path = os.path.join(self.project_root, 'AppData', 'config.json')
        if os.path.exists(self.config_path):
            self.config_watcher = ConfigWatcher(self.config_path)
            self.config_watcher.configChanged.connect(self.on_config_changed)

    def __onProjectRootPathCardClicked(self):
        game_path = QFileDialog.getExistingDirectory(self, "选择项目根路径")
        if not game_path or cfg.ProjectRootPath == game_path:
            return
        project_root_path_process = game_path.replace('/', '\\')
        qconfig.set(cfg.ProjectRootPath, project_root_path_process)
        self.ProjectRootPathCard.setContent(game_path)

    def on_config_changed(self):
        if not cfg.ProjectRootPath.value:
            if not self._has_shown_info:
                self._has_shown_info = True
                InfoBarUtils.choose_root_path(self)
                self.__onProjectRootPathCardClicked()
                self._info_bar_timer.start(3000)
        else:
            generateConfigFile()

    def reset_has_shown_info(self):
        self._has_shown_info = False

    def __initWidget(self):
        """
        初始化界面组件。

        这个方法设置了界面的主要组件和布局，包括滚动区域的设置、对象名称的定义以及样式表的应用。
        它确保界面可以根据内容自适应调整大小，并且禁用了水平滚动条。
        """

        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setViewportMargins(0, 140, 0, 5)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setObjectName('configInterface')
        self.scrollWidget.setObjectName('scrollWidget')
        self.configSettingLabel.setObjectName('configSettingLabel')
        StyleSheet.CONFIG_INTERFACE.apply(self)

    def __initCard(self):
        self.AutoBattleGroup = SettingCardGroup(self.tr("自动战斗"), self.scrollWidget)
        self.ProjectRootPathCard = PushSettingCard(
            self.tr('选择'),
            FIF.GAME,
            self.tr("项目根路径"),
            cfg.ProjectRootPath.value
        )
        self.zoneCard = CustomComboBoxSettingCard(
            prompt=self.tr("请选择区域"),
            configItem=cfg.zone,
            icon=FIF.GAME,
            title=self.tr("区域"),
            content=self.tr(""),
            texts=cfg.zone_Validator,
            parent=self.AutoBattleGroup
        )
        self.levelCard = CustomComboBoxSettingCard1(
            prompt=self.tr("请选择等级"),
            configItem=cfg.level,
            icon=FIF.GAME,
            title=self.tr("等级"),
            texts=cfg.level_Validator,
            parent=self.AutoBattleGroup
        )
        self.modeSelectCard = CustomComboBoxSettingCard(
            prompt=self.tr("请选择模式"),
            configItem=cfg.modeSelect,
            icon=FIF.GAME,
            title=self.tr("模式"),
            content=self.tr(""),
            texts=cfg.modeSelect_Validator,
            parent=self.AutoBattleGroup
        )
        self.maxFightTimeCard = PushSettingCardEval(
            text=self.tr('修改'),
            icon=FIF.PEOPLE,
            title=self.tr("最大战斗时间（秒）"),
            config_item=cfg.maxFightTime,
            parent=self.configSettingLabel.parent()
        )
        self.maxMapTimeCard = PushSettingCardEval(
            text=self.tr('修改'),
            icon=FIF.PEOPLE,
            title=self.tr("地图内最大时间（秒）"),
            config_item=cfg.maxMapTime,
            parent=self.configSettingLabel.parent()
        )
        self.hasBoomCard = SwitchSettingCard(
            icon=FIF.TRANSPARENT,
            title=self.tr('解锁炸弹'),
            content=self.tr(''),
            configItem=cfg.hasBoom,
        )
        self.useGpuCard = SwitchSettingCard(
            icon=FIF.TRANSPARENT,
            title=self.tr('GPU加速'),
            content=self.tr('使用GPU会加速模型训练,关闭会强制使用CPU进行OCR识别'),
            configItem=cfg.useGpu,
        )
        self.ProgramGroup = SettingCardGroup(self.tr('程序设置'), self.scrollWidget)
        self.autogamePathCard = SwitchSettingCard(
            icon=FIF.GAME,
            title=self.tr('启用自动配置游戏路径'),
            content="通过快捷方式、官方启动器、运行中的游戏进程等方式尝试自动配置游戏路径（未测试国际服）",
            configItem=cfg.auto_set_game_path
        )
        self.gamePathCard = PushSettingCard(
            text=self.tr('选择'),
            icon=FIF.GAME,
            title=self.tr("游戏路径"),
            content=cfg.game_path.value
        )
        self.AboutGroup = SettingCardGroup(self.tr('关于'), self.scrollWidget)
        self.githubCard = PrimaryPushSettingCard(
            self.tr('项目主页'),
            FIF.GITHUB,
            self.tr('项目主页'),
            "https://github.com/sMythicalBird/ZenlessZoneZero-Auto"
        )
        self.qqGroupCard = PrimaryPushSettingCard(
            self.tr('加入群聊'),
            FIF.EXPRESSIVE_INPUT_ENTRY,
            self.tr('QQ群'),
            "985508983"
        )

    def __initLayout(self):
        self.configSettingLabel.move(36, 30)
        self.pivot.move(40, 80)
        self.vBoxLayout.addWidget(self.stackedWidget, 0, Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.AutoBattleGroup.addSettingCard(self.ProjectRootPathCard)
        self.AutoBattleGroup.addSettingCard(self.zoneCard)
        self.AutoBattleGroup.addSettingCard(self.levelCard)
        self.AutoBattleGroup.addSettingCard(self.modeSelectCard)
        self.AutoBattleGroup.addSettingCard(self.maxFightTimeCard)
        self.AutoBattleGroup.addSettingCard(self.maxMapTimeCard)
        self.AutoBattleGroup.addSettingCard(self.hasBoomCard)
        self.AutoBattleGroup.addSettingCard(self.useGpuCard)
        self.AboutGroup.addSettingCard(self.githubCard)
        self.AboutGroup.addSettingCard(self.qqGroupCard)

        self.ProgramGroup.addSettingCard(self.autogamePathCard)
        self.ProgramGroup.addSettingCard(self.gamePathCard)
        self.addSubInterface(self.AutoBattleGroup, 'AutoBattleInterface', self.tr('自动战斗'))

        self.pivot.addItem(
            routeKey='verticalBar',
            text="|",
            onClick=lambda: self.pivot.setCurrentItem(self.stackedWidget.currentWidget().objectName()),
        )
        self.addSubInterface(self.ProgramGroup, 'ProgramInterface', self.tr('程序'))
        self.addSubInterface(self.AboutGroup, 'AboutInterface', self.tr('关于'))
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.pivot.setCurrentItem(self.stackedWidget.currentWidget().objectName())
        self.stackedWidget.setFixedHeight(self.stackedWidget.currentWidget().sizeHint().height())

    def addSubInterface(self, widget: QLabel, objectName: str, text: str):
        """
        向堆叠式布局中添加子界面，并配置相关属性。

        :param widget: 要添加的QLabel控件
        :param objectName: 设置控件的名称，用于标识和查找控件
        :param text: 显示在控件上的文本
        """

        def remove_spacing(layout):
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if isinstance(item, QSpacerItem):
                    layout.removeItem(item)
                    break

        remove_spacing(widget.vBoxLayout)
        widget.titleLabel.setHidden(True)
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        self.verticalScrollBar().setValue(0)
        self.stackedWidget.setFixedHeight(self.stackedWidget.currentWidget().sizeHint().height())

    def __connectSignalToSlot(self):
        self.ProjectRootPathCard.clicked.connect(self.__onProjectRootPathCardClicked)
        self.githubCard.clicked.connect(self.__openUrl("https://github.com/sMythicalBird/ZenlessZoneZero-Auto"))
        self.qqGroupCard.clicked.connect(self.__openUrl(
            "https://qm.qq.com/cgi-bin/qm/qr?k=Oftg7EcBQx-Ur7WXZBoO_7qiEvUABOM3&jump_from=webapi&authKey=hADNxYfUOzVpVxycHVVblOOFM1dmDHmsG3kOFIb3Z8xwXfvVwSCXIge6wVHG5gcg"))

    def __openUrl(self, url):
        return lambda: QDesktopServices.openUrl(QUrl(url))
