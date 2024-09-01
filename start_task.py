# -*- coding: utf-8 -*-
""" 
@file:      start_task.py
@time:      2024/8/30 上午3:22
@author:    sMythicalBird
"""
from threading import Thread
from pynput.keyboard import Key, Listener

from utils.task import task_zero, task_money, task_code


def key_event(task):
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


# 任务——零号空洞
def zero_task():
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_zero,))
    key_thread.start()

    # 导入任务
    import event_handling.zero
    import event_handling.fight.fight_zero

    # 任务开始
    task_zero.run()


# 任务-拿命验收
def zero_money():
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_money,))
    key_thread.start()

    # 导入任务
    import event_handling.money

    # 任务开始
    task_money.run()


# 任务——兑换码
def redemption_code():
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_code,))
    key_thread.start()

    # 导入任务
    import event_handling.code

    # 任务开始
    task_code.run()


def start_task(action):
    if action == "zero":
        print("start zero task")
        zero_task()
    elif action == "money":
        print("start money task")
        zero_money()
