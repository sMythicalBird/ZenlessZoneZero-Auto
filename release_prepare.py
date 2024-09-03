# -*- coding: utf-8 -*-
"""
@file:      release_prepare
@time:      2024/9/3 14:10
@author:    sMythicalBird
"""
from schema.download import check_file_task
from gui.api.check_update import release_version

release_version()
check_file_task()
