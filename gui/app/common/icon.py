# coding: utf-8
from enum import Enum

from qfluentwidgets import FluentIconBase, getIconColor, Theme


class Icon(FluentIconBase, Enum):

    # TODO: Add your icons here

    SETTINGS = "Settings"
    SETTINGS_FILLED = "SettingsFilled"

    def path(self, theme=Theme.AUTO):
        return f":/app/images/icons/{self.value}_{getIconColor(theme)}.svg"
