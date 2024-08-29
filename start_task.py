# -*- coding: utf-8 -*-
""" 
@file:      start_task.py
@time:      2024/8/30 上午3:22
@author:    sMythicalBird
"""

import threading
import subprocess
import sys
import inspect


def task1():
    print("Task 1 is running...")


def start_task(action):
    subprocess.Popen(
        [sys.executable, "-c", action], creationflags=subprocess.CREATE_NEW_CONSOLE
    )
