import time
import pydirectinput
import cv2
from pathlib import Path
from utils import screenshot

root_path = Path(__file__).parent.parent
image_path = root_path / "download/yuan.png"
image_to_quan = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)


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
        keyboard_press("shift", 0.025, 0.05)
        mouse_press("left", 0.025, 0.1)
        keyboard_press("space", 0.025, 0.05)
        mouse_press("left", 0.025, 0.025)
        keyboard_press("shift", 0.025, 0.025)
        mouse_press("left", 0.025, 0.1)
    keyboard_press("2", 0.025, 0.025)


def turn():
    while True:
        flag = 0
        for i in range(10):
            # screen = np.array(ImageGrab.grab())
            screen = screenshot()
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(screen_gray, image_to_quan, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(
                result
            )  # max_val为识别图像左上角坐标
            if max_val > 0.85:
                flag = 1
                print("quan")
                x, _ = max_loc
                _, y = max_loc
                x += image_to_quan.shape[1] / 2
                y += image_to_quan.shape[0] / 2
                print(x, y)
                x = int(x)
                if y > 400:
                    pydirectinput.move(xOffset=1100, yOffset=0, relative=True)
                time.sleep(0.2)
                x = x - 648
                if abs(x) < 250:
                    if x > 0:
                        x = int(x ** (1 / 1.28))
                    else:
                        x = -int(abs(x) ** (1 / 1.28))
                pydirectinput.move(xOffset=x, yOffset=0, relative=True)
                if abs(x) <= 2:
                    keyboard_press("w", 2, 0)
                    break
            time.sleep(0.03)
        if flag == 0:
            break


time.sleep(3)
print("start")
turn()
print("end")
