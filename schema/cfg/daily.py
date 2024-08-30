# -*- coding: utf-8 -*-
"""
@file:      daily
@time:      2024/8/30 16:23
@author:    sMythicalBird
"""
from typing import List
from pydantic import BaseModel, Field, model_validator


class CodeList(BaseModel):
    code_cnt: int = Field(0, description="兑换码数量")
    code_value: List[str] = Field([], description="兑换码列表")

    def get_code(self):
        code = self.code_value.pop(0)
        self.code_cnt -= 1
        return code


code_list = CodeList()
