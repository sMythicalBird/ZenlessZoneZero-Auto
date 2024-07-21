# -*- coding: utf-8 -*-
""" 
@file:      dlc1.py
@time:      2024/7/21 上午12:13
@author:    sMythicalBird
"""
from threading import Thread
from pynput.keyboard import Key, Listener
from dlc.money import *


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


key_thread = Thread(target=key_event)
key_thread.start()


if __name__ == "__main__":
    task.pause()
    task.run()
