# -*- coding: utf-8 -*-
""" 
@file:      start_task.py
@time:      2024/8/30 上午3:22
@author:    sMythicalBird
"""
from threading import Thread
from pynput.keyboard import Key, Listener

from utils.task import task


def key_event():
    def on_press(key):
        if key == Key.f12:
            task.stop()
            return False
        if key == Key.f11:
            task.pause()
        if key == Key.f10:
            task.restart()
        return None

    with Listener(on_press=on_press) as listener:
        listener.join()


def redemption_code():
    # 监听运行状态
    key_thread = Thread(target=key_event)
    key_thread.start()
    # 清空task的任务
    # task.clear_task()
    # 导入任务
    import event_handling.code

    # 任务开始
    task.run()


def task1():
    print("Task 1 is running...")


def start_task(action):
    if action == "task1":
        task1()
