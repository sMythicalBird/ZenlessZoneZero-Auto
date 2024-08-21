# -*- coding: utf-8 -*-
""" 
@file:      zero_hole_group.py
@time:      2024/8/13 上午1:57
@author:    sMythicalBird
"""
from operator import index

from qfluentwidgets import SettingCardGroup, FluentIcon
from schema.cfg.info import zero_cfg
from ..components.combo_box_card import (
    ZeroLevelSelectCard,
    ModeSelectCard,
    NumTextCard,
)


class ZeroHoleGroup(SettingCardGroup):
    def __init__(self, parent=None):
        super().__init__("零号空洞", parent)
        self.card1 = None
        self.card2 = None
        self.card3 = None
        self.card4 = None
        self.card5 = None
        self.card6 = None
        self.card7 = None
        self.init_card()
        self.init_layout()

    def init_card(self):
        # 副本难度选择
        self.card1 = ZeroLevelSelectCard(
            "zero_level_selection",
            FluentIcon.ALIGNMENT,
            self.tr("副本选择"),
        )
        # 刷取模式选择
        self.card2 = ModeSelectCard(
            "instance_type",
            FluentIcon.ALIGNMENT,
            self.tr("模式选择"),
            index=zero_cfg.modeSelect - 1,
            texts=["全通关(无业绩)", "业绩速刷", "银行速刷", "全通关(含业绩)"],
        )
        # 携带队友个数
        self.card3 = ModeSelectCard(
            "team_number",
            FluentIcon.ALIGNMENT,
            self.tr("呼叫支援次数"),
            index=zero_cfg.teamMates,
            texts=["0", "1", "2"],
        )
        # 是否解锁炸弹
        self.card4 = ModeSelectCard(
            "bomb_unlock",
            FluentIcon.ALIGNMENT,
            self.tr("是否解锁炸弹"),
            index=zero_cfg.hasBoom,
            texts=["是", "否"],
        )
        # 单次进去地图最大时间
        self.card5 = NumTextCard(
            "max_map_time",
            FluentIcon.ALIGNMENT,
            self.tr("单次进入地图最大时间"),
            zero_cfg.maxMapTime,
        )
        # 单场战斗最大用时
        self.card6 = NumTextCard(
            "max_fight_time",
            FluentIcon.ALIGNMENT,
            self.tr("单场战斗最大用时"),
            zero_cfg.maxFightTime,
        )
        # 运行次数
        self.card7 = NumTextCard(
            "max_fight_count",
            FluentIcon.ALIGNMENT,
            self.tr("运行次数"),
            zero_cfg.maxFightCount,
        )

    def init_layout(self):
        self.addSettingCard(self.card1)
        self.addSettingCard(self.card2)
        self.addSettingCard(self.card3)
        self.addSettingCard(self.card4)
        self.addSettingCard(self.card5)
        self.addSettingCard(self.card6)
        self.addSettingCard(self.card7)

    # 更新当前参数值
    def update(self):
        zero_cfg.targetMap.zone = self.card1.comboBox1.currentText()
        zero_cfg.targetMap.level = self.card1.comboBox2.currentText()
        zero_cfg.modeSelect = self.card2.comboBox.currentIndex() + 1
        zero_cfg.teamNumber = self.card3.comboBox.currentIndex()
        zero_cfg.hasBomb = self.card4.comboBox.currentIndex()
        zero_cfg.maxMapTime = self.card5.get_value()
        zero_cfg.maxFightTime = self.card6.get_value()
        zero_cfg.maxFightCount = self.card7.get_value()
