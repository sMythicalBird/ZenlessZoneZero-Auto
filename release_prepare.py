# -*- coding: utf-8 -*-
"""
@file:      release_prepare
@time:      2024/9/3 14:10
@author:    sMythicalBird
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))  # 将当前目录添加到 sys.path 中

from schema.download import check_file_task
from gui.api.check_update import release_version

release_version()
check_file_task()
