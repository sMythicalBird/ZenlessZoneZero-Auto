# -*- coding: utf-8 -*-
"""
@file:      coditional
@time:      2024/8/19 18:05
@author:    sMythicalBird
"""
from pydantic import BaseModel, Field


# dlc中相关的标志
class DlcStage(BaseModel):
    moneyFightFlag: bool = Field(False, description="是否进入战斗")


stage = DlcStage()
