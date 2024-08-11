import os
from typing import Union

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from qfluentwidgets import SettingCard, OptionsConfigItem, FluentIconBase, qconfig, ComboBox

from ..utils.configUtils import get_compute_tactic
from ..watcher.config_watcher import ConfigWatcher
from ..common.config import cfg
from ..watcher.key_watcher import KeyAndValWatcher


class CustomComboBoxSettingCard(SettingCard):

    def __init__(self, prompt, configItem: OptionsConfigItem, icon: Union[str, QIcon, FluentIconBase], title,
                 content=None, texts=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.configItem = configItem
        self.comboBox = ComboBox(self)
        self.comboBox.setFixedWidth(350)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.optionToText = {o: t for o, t in zip(configItem.options, texts)}
        for text, option in zip(texts, configItem.options):
            self.comboBox.addItem(text, userData=option)
        self.comboBox.setCurrentText(self.optionToText[qconfig.get(configItem)])
        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)
        configItem.valueChanged.connect(self.setValue)

    def _onCurrentIndexChanged(self, index: int):
        qconfig.set(self.configItem, self.comboBox.itemData(index))

    def setValue(self, value):
        if value not in self.optionToText:
            return
        self.comboBox.setCurrentText(self.optionToText[value])
        qconfig.set(self.configItem, value)


class CustomComboBoxSettingCard1(SettingCard):
    def __init__(self, prompt, configItem: OptionsConfigItem, icon: Union[str, QIcon, FluentIconBase], title,
                 content=None, texts=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.configItem = configItem
        self.comboBox = ComboBox(self)
        self.comboBox.setFixedWidth(350)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.texts = texts
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config_path = os.path.join(self.project_root, 'AppData', 'config.json')
        if os.path.exists(self.config_path):
            self.config_watcher = KeyAndValWatcher(self.config_path, 'TargetMap', 'Zone')
            self.config_watcher.configChanged.connect(self.on_config_changed)
        self.optionToText = {o: t for o, t in zip(self.configItem.options, self.texts)}
        for text, option in zip(self.texts, self.configItem.options):
            self.comboBox.addItem(text, userData=option)
        self.comboBox.setCurrentText(self.optionToText[qconfig.get(self.configItem)])
        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)
        self.configItem.valueChanged.connect(self.setValue)

    def on_config_changed(self):

        val = get_compute_tactic(self.config_path, 'TargetMap', 'Zone')
        if val == "旧都列车":
            self.texts = cfg.level_Validator = ["外围", "前线", "内部", "腹地", "核心"]
            self.current_text = self.comboBox.currentText()
            self.comboBox.clear()
            self.comboBox.addItems(self.texts)
        elif val == "施工废墟":
            self.texts = cfg.level_Validator = ["前线", "内部", "腹地", "核心"]
            self.current_text = self.comboBox.currentText()
            self.comboBox.clear()
            self.comboBox.addItems(self.texts)
        if self.current_text in self.texts:
            self.comboBox.setCurrentText(self.current_text)
        else:
            self.comboBox.setCurrentIndex(0)
            qconfig.set(self.configItem, self.texts[0])
            return
        qconfig.set(self.configItem, self.current_text)
    def _onCurrentIndexChanged(self, index: int):
        qconfig.set(self.configItem, self.texts[index])
    def setValue(self, value):
        if value not in self.optionToText:
            return
        self.comboBox.setCurrentText(self.optionToText[value])
        qconfig.set(self.configItem, value)
