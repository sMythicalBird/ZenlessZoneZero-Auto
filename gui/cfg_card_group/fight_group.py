# -*- coding: utf-8 -*-
""" 
@file:      fight_group.py
@time:      2024/8/13 上午2:09
@author:    sMythicalBird
"""
from qfluentwidgets import SettingCardGroup, FluentIcon
from ..components.fight_card import FightCfgCard
from schema.cfg.load import save_config
from schema.cfg.info import fight_cfg, update_fight, update_fight_logic_all


class FightGroup(SettingCardGroup):
    def __init__(self, parent=None):
        super().__init__("战斗", parent)
        self.zero_fight_card = None
        self.daily_fight_card = None
        self.init_card()
        self.init_layout()

    def init_card(self):
        self.zero_fight_card = FightCfgCard(
            "zero_fight",
            FluentIcon.ALIGNMENT,
            self.tr("零号战斗配置"),
            fight_cfg.zero_fight,
            parent=self,
        )
        self.daily_fight_card = FightCfgCard(
            "daily_fight",
            FluentIcon.ALIGNMENT,
            self.tr("日常战斗配置"),
            fight_cfg.daily_fight,
            parent=self,
        )

    def init_layout(self):
        self.addSettingCard(self.zero_fight_card)
        self.addSettingCard(self.daily_fight_card)

    def update(self):
        self.zero_fight_card.get_value()
        self.daily_fight_card.get_value()
        update_fight()
        save_config("fight.yaml", fight_cfg)
