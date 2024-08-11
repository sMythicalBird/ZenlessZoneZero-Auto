import sys
from enum import Enum

from PySide6.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, Theme, FolderValidator, ConfigSerializer)

from .setting import CONFIG_FILE
from ..validator.CustomOptionsValidator import CustomOptionsValidator


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Config of application """

    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())
    ProjectRootPath = ConfigItem("AutoBattle", "ProjectRootPath", "")
    zone_Validator = ["旧都列车", "施工废墟"]
    zone = OptionsConfigItem(
        "TargetMap", "Zone", "", OptionsValidator(zone_Validator))
    level_Validator = ["外围", "前线", "内部", "腹地", "核心"]
    level = OptionsConfigItem(
        "TargetMap", "Level", "", CustomOptionsValidator(level_Validator))
    modeSelect_Validator = ['全通关', '零号业绩', '零号银行', '业绩与银行']
    modeSelect = OptionsConfigItem(
        "AutoBattle", "ModeSelect", "", OptionsValidator(modeSelect_Validator))
    maxFightTime = ConfigItem("AutoBattle", "MaxFightTime", '300')
    maxMapTime = ConfigItem("AutoBattle", "MaxMapTime", '1500')
    hasBoom = ConfigItem("AutoBattle", "HasBoom", True, BoolValidator())
    useGpu = ConfigItem("AutoBattle", "UseGpu", False, BoolValidator())
    game_path = ConfigItem("Program", "GamePath", '')
    auto_set_game_path = ConfigItem("Program", "AutoSetGamePath", False, BoolValidator())


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(str(CONFIG_FILE.absolute()), cfg)
