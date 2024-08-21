# -*- coding: utf-8 -*-
""" 
@file:      zero_hole_group.py
@time:      2024/8/13 上午1:57
@author:    sMythicalBird
"""
from paddle.tensor.manipulation import zero_
from qfluentwidgets import SettingCardGroup, FluentIcon
from sympy import false

from schema.cfg.info import zero_cfg
from ..components.combo_box_card import (
    ZeroLevelSelectCard,
    ModeSelectCard,
    NumTextCard,
    MultiSelectCard,
)
from schema.cfg.load import save_config


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
        self.card8 = None
        self.card9 = None
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
        # 鸣徽类型选择
        self.card8 = MultiSelectCard(
            "buff_type",
            FluentIcon.ALIGNMENT,
            self.tr("鸣徽类型(至多5个)"),
            zero_cfg.selBuff,
            [
                "以太",
                "冻结",
                "暴击",
                "引燃",
                "感电",
                "能量",
                "强袭",
                "支援",
                "决斗",
                "护盾",
                "协助",
                "通用",
                "闪避",
                "研究",
                "邦布",
                "空洞",
                "诡术",
                "契合",
            ],
            5,
            (350, 40),
        )
        # 鸣徽类型选择
        self.card9 = MultiSelectCard(
            "char_type",
            FluentIcon.ALIGNMENT,
            self.tr("代理人选择(至多3个)"),
            zero_cfg.characters,
            [
                "青衣",
                "朱鸢",
                "艾莲",
                "莱卡恩",
                "猫又",
                "11号",
                "丽娜",
                "珂蕾妲",
                "格莉丝",
                "露西",
                "派派",
                "妮可",
                "比利",
                "本",
                "仓角",
                "安比",
                "可琳",
                "安东",
            ],
            3,
            (300, 40),
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

    # 更新当前参数值
    def update(self):
        zero_cfg.targetMap.zone = self.card1.comboBox1.currentIndex() + 1
        zero_cfg.targetMap.level = self.card1.comboBox2.currentIndex() + 1
        zero_cfg.modeSelect = self.card2.comboBox.currentIndex() + 1
        zero_cfg.teamMates = self.card3.comboBox.currentIndex()
        if self.card4.comboBox.currentIndex():
            zero_cfg.hasBoom = True
        else:
            zero_cfg.hasBoom = False
        zero_cfg.maxMapTime = self.card5.get_value()
        zero_cfg.maxFightTime = self.card6.get_value()
        zero_cfg.maxFightCount = self.card7.get_value()
        zero_cfg.selBuff = self.card8.get_value()
        zero_cfg.characters = self.card9.get_value()
        for each in zero_cfg:
            print(each)
        save_config("zero.yaml", zero_cfg)
        print("更新成功")
