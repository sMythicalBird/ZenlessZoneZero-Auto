import time
import pydirectinput


def keyboard_press(key: str, duration: float, interval: float):
    pydirectinput.keyDown(key)
    time.sleep(duration)
    pydirectinput.keyUp(key)
    time.sleep(interval)


def mouse_press(key: str, duration: float, interval: float):
    pydirectinput.mouseDown(button=key)
    time.sleep(duration)
    pydirectinput.mouseUp(button=key)
    time.sleep(interval)


def fight_login():
    for i in range(5):
        keyboard_press('shift', 0.025, 0.05)
        mouse_press('left', 0.025, 0.1)
        keyboard_press('space', 0.025, 0.05)
        mouse_press('left', 0.025, 0.025)
        keyboard_press('shift', 0.025, 0.025)
        mouse_press('left', 0.025, 0.1)
    keyboard_press('2', 0.025, 0.025)