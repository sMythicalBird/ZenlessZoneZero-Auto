# -*- coding: utf-8 -*-
"""
@file:      fight_logic.py
@time:      2024/7/22 下午11:32
@author:    zeromike
"""

import time
from utils import control, logger
from pydirectinput import press

def default_fight_logic():
    for _ in range(5):
        control.attack()
        time.sleep(0.2)
        control.attack()
        time.sleep(0.2)
        control.attack()
        time.sleep(0.2)
        control.attack()
        time.sleep(0.2)
        control.attack()
        time.sleep(0.2)
        control.attack()
        time.sleep(0.2)
        press("e", duration=0.1)
        time.sleep(0.3)
        press("space", duration=0.1)
        time.sleep(0.2)
        press("shift", duration=0.1)
    press("q", duration=0.1)
    time.sleep(0.2)

def ellen_0_fight_logic():
    logger.debug("-------- 进入艾莲0战斗逻辑 --------")
    for _ in range(5):
        control.dash_charge_attack(0.5)
        time.sleep(0.2)
        control.attack()
        time.sleep(0.2)
        control.attack()
        time.sleep(0.2)
        control.frequent_attack(5)

    for _ in range(2):
        press("e", duration=0.1)
        time.sleep(0.5)
        control.frequent_attack(5)

    press("q", duration=0.1)
    time.sleep(0.2)
def ellen_2_fight_logic():
    logger.debug("-------- 进入艾莲2战斗逻辑 --------")
    for _ in range(5):
        control.dash_attack(0.3)
        time.sleep(0.2)
        control.attack()
        time.sleep(0.2)
        control.attack()
        time.sleep(0.2)
        control.frequent_attack(5)

    for _ in range(2):
        press("e", duration=0.1)
        time.sleep(0.5)
        control.frequent_attack(5)

    press("q", duration=0.1)
    time.sleep(0.2)

fight_logics = {
    "default": default_fight_logic,
    "ellen": ellen_0_fight_logic,
    "ellen_2": ellen_2_fight_logic
}