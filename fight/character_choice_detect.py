import cv2
import numpy as np

# 以下库调试用
import os


def canny_edge_detect(img: np.ndarray) -> np.ndarray:
    """
    针对BGR三通道的边缘检测
    :param img: 输入图像 RGB 格式
    """
    b, g, r = cv2.split(img)
    threshold = (50, 150)
    edge_b = cv2.Canny(b, threshold[0], threshold[1])
    edge_g = cv2.Canny(g, threshold[0], threshold[1])
    edge_r = cv2.Canny(r, threshold[0], threshold[1])
    edge_BGR = cv2.merge([edge_b, edge_g, edge_r])

    edge_BGR2GRAY = cv2.cvtColor(edge_BGR, cv2.COLOR_BGR2GRAY)

    def h_bar_edge_detect(img, edge):
        """
        水平进度条边缘检测优化
        水平进度条区域使用灰度图像，高斯模糊后进行边缘检测，再与原图边缘对应区域进行合并
        """
        sub_x1 = 85
        sub_y1 = 20
        sub_x2 = 565
        sub_y2 = 68
        sub_img = img[sub_y1:sub_y2, sub_x1:sub_x2]
        sub_img_gray = cv2.cvtColor(sub_img, cv2.COLOR_RGB2GRAY)
        sub_img_blurr = cv2.GaussianBlur(sub_img_gray, (3, 3), 0)
        sub_img_edge = cv2.Canny(sub_img_blurr, 50, 150)
        edge[sub_y1:sub_y2, sub_x1:sub_x2] = sub_img_edge

    h_bar_edge_detect(img, edge_BGR2GRAY)

    return edge_BGR2GRAY


def find_contours(img_edge: np.ndarray) -> tuple:
    """
    轮廓提取
    :param img_edge: 输入轮廓检测结果
    """
    contours, _ = cv2.findContours(img_edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
    circles = cv2.HoughCircles(
        img_edge,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=35,
        maxRadius=45,
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
    img_edge_BGR = canny_edge_detect(img_crop)
    img_circle_detect = circle_detect(img_edge_BGR)
    img_rect_detect = rect_detect(img_edge_BGR)
    return img_rect_detect or img_circle_detect
