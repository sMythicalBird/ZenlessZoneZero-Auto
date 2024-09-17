# -*- coding: utf-8 -*-
""" 
@file:      start_task.py
@time:      2024/8/30 上午3:22
@author:    sMythicalBird
"""
from threading import Thread
from pynput.keyboard import Key, Listener

from utils.task import task_zero, task_money, task_code, task_fight, task_daily


# 测试更新情况


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
def money_task():
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_money,))
    key_thread.start()

    # 导入任务
    import event_handling.money

    # 任务开始
    task_money.run()


def fight_task():
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_fight,))
    key_thread.start()

    # 导入任务
    import event_handling.fight.fight_only

    # 任务开始
    task_fight.run()


# 任务——兑换码
def redemption_code():
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_code,))
    key_thread.start()

    # 导入任务
    import event_handling.code

    # 任务开始
    task_code.run()

# 自动化日常任务
def daily():
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_daily,))
    key_thread.start()

    # 导入任务
    import event_handling.daily

    # 任务开始
    task_daily.run()


def new_account():
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_daily,))
    key_thread.start()

    # 导入任务
    import event_handling.test

    # 任务开始
    task_daily.run()




def start_task(action):
    if action == "zero":
        print("start zero task")
        zero_task()
    elif action == "money":
        print("start money task")
        money_task()
    elif action == "fight":
        print("start fight task")
        fight_task()
    elif action == "daily":
        print("start daily task")
        daily()


if __name__ == '__main__':
    start_task('daily')
    # new_account()