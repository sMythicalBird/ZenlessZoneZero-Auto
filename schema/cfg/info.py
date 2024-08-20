# -*- coding: utf-8 -*-
"""
@file:      info
@time:      2024/8/21 01:00
@author:    sMythicalBird
"""

from .zero_info import Config
from .load import load_config


zero_cfg = load_config("zero.yaml", Config)
