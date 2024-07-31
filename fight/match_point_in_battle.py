import cv2

import time
import os
import math

from pydirectinput import moveRel
from utils.utils import screenshot

def calc_angle(x, y, w, h):
    """
    计算圆点坐标与屏幕中心的夹角
    :param x: 圆点横坐标
    :param y: 圆点纵坐标
    :param w: 屏幕宽度
    :param h: 屏幕高度
    :return: 圆点与屏幕中心的夹角
    """
    x0 = w / 2 + 0.5
    y0 = h / 2 + 0.5
    delta_x = x - x0
    delta_y = y0 - y
    angle = math.degrees(math.atan2(delta_y, delta_x))
    
    return angle


def match_point(image_to_match):
    """
    匹配圆点位置，计算夹角，并转动鼠标，使得圆点与屏幕中心的夹角接近90度
    :param image_to_match: 圆点模板图片，灰度模式
    """
    delta_ang = 90
    flag = False
    global try_times
    global get_times # 记录尝试次数和成功次数，用于调试，或后续处理bug

    h_crop = 85
    w_crop = 225 # 屏幕裁剪区域高度和宽度，减小计算量，提高匹配准确率

    for i in range(3): # 调整视角为最高处俯视，方便计算圆点坐标夹角
        moveRel(xOffset=0, yOffset=300, relative=True, duration=0.2)
        time.sleep(0.1) # 等待视角调整

    while not flag:
        try_times += 1
        screen = screenshot()
        h, w, _ = screen.shape

        sub_screen = screen.copy()[h_crop:h-h_crop, w_crop:w-w_crop]
        h1, w1, _ = sub_screen.shape

        sub_screen_gray = cv2.cvtColor(sub_screen, cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(sub_screen_gray, image_to_match, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.8:
            get_times += 1
            x, y = max_loc
            x += image_to_match.shape[1] / 2
            y += image_to_match.shape[0] / 2
            angle = calc_angle(x, y, w1, h1)
            delta_ang = abs(angle - 90)

            sign = int(math.copysign(1, x - w1 / 2))
            mov_x = 400 if delta_ang > 60 else 200 if delta_ang > 30 else 100 if delta_ang > 10 else 10
            mov_x *= sign

            moveRel(xOffset=mov_x, yOffset=0, relative=True, duration=0.2)
            time.sleep(0.3) # 等待视角调整

            if delta_ang <= 2:
                cv2.line(sub_screen, (int(w1/2), int(h1/2)), (int(x), int(y)), (0, 0, 255), 2)
                # plot_images([screen, sub_screen])
                time.sleep(0.5)
                flag = True



# 调试用例
file = "point_23.png"
directory = r"screenshots\\circle_point\\good_point\\"
try_times = 0
get_times = 0
img = cv2.imread(os.path.join(directory, file), cv2.IMREAD_GRAYSCALE) # 读取圆点模板图片，灰度模式
match_point(img)