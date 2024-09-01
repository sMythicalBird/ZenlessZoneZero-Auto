# -*- coding: utf-8 -*-
""" 
@file:      conditional.py
@time:      2024/8/30 上午2:23
@author:    sMythicalBird
"""
from pydantic import BaseModel, Field


# dlc中相关的标志
class DlcStage(BaseModel):
    moneyFightFlag: bool = Field(False, description="是否进入战斗")


stage = DlcStage()
