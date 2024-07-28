import cv2
import numpy as np

# 以下库调试用
import os


def canny_edge_detect_BGR(img: np.ndarray) -> np.ndarray:
    """
    针对BGR三通道的边缘检测
    :param img: 输入图像 RGB 格式
    """
    b, g, r = cv2.split(img)
    edge_b = cv2.Canny(b, 100, 200)
    edge_g = cv2.Canny(g, 100, 200)
    edge_r = cv2.Canny(r, 100, 200)
    edge_BGR = cv2.merge([edge_b, edge_g, edge_r])
    edge_BGR2GRAY = cv2.cvtColor(edge_BGR, cv2.COLOR_BGR2GRAY)
    return edge_BGR2GRAY


def find_contours(img_edge: np.ndarray) -> tuple:
    """
    轮廓提取
    :param img_edge: 输入轮廓检测结果
    """
    contours, _ = cv2.findContours(
        img_edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def rect_detect(img_edge: np.ndarray) -> bool:
    """
    矩形检测，长条图形易受到其他画面内容干扰，不适合作为主要判断标准
    :param img_edge: 输入轮廓检测结果
    """
    contours = find_contours(img_edge)
    for contour in contours:
        epslion = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epslion, True)

        if len(approx) == 4:  # 四边形
            x, y, w, h = cv2.boundingRect(contour)
            if w >= 450 and h <= 30:
                return True


def circle_detect(img_edge: np.ndarray) -> bool:
    """
    圆形检测
    :param img_edge: 输入轮廓检测结果
    """
    circles = cv2.HoughCircles(img_edge,
                               cv2.HOUGH_GRADIENT,
                               dp=1,
                               minDist=20,
                               param1=50,
                               param2=30,
                               minRadius=35,
                               maxRadius=45
                               )
    if circles is not None:
        if len(circles) == 2:
            return True


def character_choice_detect(img: np.ndarray) -> bool:
    """
    角色选择检测
    :param img: 输入图像 RGB 格式
    """
    # 判断区域坐标
    x1 = 315
    y1 = 545
    x2 = 965
    y2 = 660
    w = x2 - x1
    h = y2 - y1

    img_crop = img[y1:y2, x1:x2]  # 裁剪出目标判断区域
    img_edge_BGR = canny_edge_detect_BGR(img_crop)
    img_rect_detect = rect_detect(img_crop.copy(), img_edge_BGR)
    img_circle_detect = circle_detect(img_crop.copy(), img_edge_BGR)

    return img_rect_detect or img_circle_detect


# 测试用例
directory = r"d:\ZZZ-Auto\dev\ZenlessZoneZero-Auto\test\screenshots\analyse"

# file = "ZZZAuto_20240727-200101.220.png"
# img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
# print(f"{file}:{character_choice_detect(img)}")

for file in os.listdir(directory):
    path = os.path.join(directory, file)
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    print(f"{file}:{character_choice_detect(img)}")
