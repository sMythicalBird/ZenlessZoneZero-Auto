# -*- coding: utf-8 -*-
""" 
@file:      zero_hole_group.py
@time:      2024/8/13 上午1:57
@author:    sMythicalBird
"""
from qfluentwidgets import SettingCardGroup, FluentIcon
from ..components.combo_box_card import ChoiceSettingCard, ComboBoxSettingCard1


class ZeroHoleGroup(SettingCardGroup):
    def __init__(self, parent=None):
        super().__init__("零号空洞", parent)
        self.card1 = None
        self.card2 = None
        self.card3 = None
        self.card4 = None
        self.init_card()
        self.init_layout()

    def init_card(self):
        self.card1 = ChoiceSettingCard(
            "zero_level_selection",
            FluentIcon.ALIGNMENT,
            self.tr("副本选择"),
        )
        self.card2 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.card3 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.card4 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )

    def init_layout(self):
        self.addSettingCard(self.card1)
        self.addSettingCard(self.card2)
        self.addSettingCard(self.card3)
        self.addSettingCard(self.card4)
