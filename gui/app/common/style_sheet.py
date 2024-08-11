# coding: utf-8
from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    # TODO: Add your qss here
    
    SETTING_INTERFACE = "setting_interface"
    CONFIG_INTERFACE = "config_interface"
    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/app/qss/{theme.value.lower()}/{self.value}.qss"
