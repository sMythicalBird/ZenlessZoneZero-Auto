# -*- coding: utf-8 -*-
"""
@file:      __init__.py
@time:      2024/7/10
@author:    sMythicalBird
"""

# event: 添加各种事件的处理
# fight: 添加战斗的处理
# others: 未进入地图时的一些操作
# secretpath: 添加秘径遇到的各种事件的处理
# specialarea: 添加特殊区域(盲盒区域和未知区域遇到的特殊地图)

from .incident import *
from .fight import *
from .others import *
from .secretpath import *
from .specialarea import *

__all__ = []
