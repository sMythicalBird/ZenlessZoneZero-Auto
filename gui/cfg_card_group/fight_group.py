# -*- coding: utf-8 -*-
""" 
@file:      fight_group.py
@time:      2024/8/13 上午2:09
@author:    sMythicalBird
"""
from qfluentwidgets import SettingCardGroup, FluentIcon
from ..components import ComboBoxSettingCard1


class FightGroup(SettingCardGroup):
    def __init__(self, parent=None):
        super().__init__("战斗", parent)
        self.card1 = None
        self.card2 = None
        self.card3 = None
        self.card4 = None
        self.init_card()
        self.init_layout()

    def init_card(self):
        self.card1 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
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
        self.card5 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.card6 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.card7 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.card8 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.card9 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.card10 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.card11 = ComboBoxSettingCard1(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("区域"),
            texts=["旧都列车", "施工废墟", "巨骸大厦"],
        )
        self.card12 = ComboBoxSettingCard1(
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
        self.addSettingCard(self.card5)
        self.addSettingCard(self.card6)
        self.addSettingCard(self.card7)
        self.addSettingCard(self.card8)
        self.addSettingCard(self.card9)
        self.addSettingCard(self.card10)
        self.addSettingCard(self.card11)
        self.addSettingCard(self.card12)
