import cv2
import numpy as np


class lightDetector:
    def __init__(self):
        # 传入自定义的光效颜色范围参数：黄色
        lower_hsv_yellow = np.array([25, 80, 160])
        upper_hsv_yellow = np.array([33, 255, 255])
        # 传入自定义的光效颜色范围参数：红色
        lower_hsv_red_1 = np.array([170, 70, 255])  # 红色HSV范围对应0-180度，需分段处理
        upper_hsv_red_1 = np.array([180, 200, 255])
        lower_hsv_red_2 = np.array([0, 70, 255])
        upper_hsv_red_2 = np.array([10, 200, 255])

        self.color_ranges = {
            "yellow": {
                "yellow_1": (lower_hsv_yellow, upper_hsv_yellow),
            },
            "red": {
                "red_1": (lower_hsv_red_1, upper_hsv_red_1),
                "red_2": (lower_hsv_red_2, upper_hsv_red_2),
            },
        }

        self.kernel = np.ones((5, 5), np.uint8)  # 形态学操作使用的卷积核
        self.kernel_size = 1
        self.kernel_V = cv2.getStructuringElement(
            cv2.MORPH_RECT, (self.kernel_size, self.kernel_size * 60)
        )
        self.kernel_H = cv2.getStructuringElement(
            cv2.MORPH_RECT, (self.kernel_size * 60, self.kernel_size)
        )

    @staticmethod
    def _preprocess_img(img: np.ndarray) -> np.ndarray:
        """
        预处理图像，裁剪左上角能量显示、右下角技能显示、右上角BOSS血条部分，避免识别黄色光效时干扰
        """
        x1, y1, w, h = 60, 120, 220, 40  # 左上角能量显示
        x2, y2 = x1 + w, y1 + h
        img[y1:y2, x1:x2, :] = 0
        x1_1, y1_1, w_1, h_1 = 1160, 520, 50, 160  # 右下角技能显示
        x2_1, y2_1 = x1_1 + w_1, y1_1 + h_1
        img[y1_1:y2_1, x1_1:x2_1, :] = 0
        x2_1, y2_1, w_2, h_2 = 460, 2, 380, 32  # 右上角BOSS血条部分
        x2_1, y2_1 = x2_1 + w_2, y2_1 + h_2
        img[y2_1 : y2_1 + h_2, x2_1 : x2_1 + w_2, :] = 0
        return img

    def _process_contours(self, img_hsv, color_ranges):
        """
        根据颜色范围创建掩码，进行形态学操作，并找到轮廓
        """
        mask1 = np.zeros_like(img_hsv[:, :, 0])
        for _, color_range in color_ranges.items():
            lower_color, upper_color = color_range
            mask = cv2.inRange(img_hsv, lower_color, upper_color)
            mask1 = cv2.bitwise_or(mask1, mask)
        mask2_1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, self.kernel_H)
        mask2_2 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, self.kernel_V)
        mask2 = cv2.bitwise_and(mask2_1, mask2_2)
        contours, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours

    @staticmethod
    def _extract_contour_dimensions(contours):
        """
        提取轮廓的宽度和高度
        """
        dimensions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            dimensions.append((w, h))  # 存储宽度和高度
        return dimensions

    @staticmethod
    def _is_rectangle_fit(width, height):
        """
        判断轮廓的宽高比是否符合条件
        """
        aspect_ratio = max((width / height), (height / width))
        return (aspect_ratio > 10) and max(width, height) > 300 and min(width, height) < 50

    def detect_rectangles(self, img_hsv: np.ndarray) -> dict:
        """
        检测图像中的矩形效果
        """
        results = {}
        for color_name, sub_ranges in self.color_ranges.items():
            contours = self._process_contours(img_hsv, sub_ranges)
            dimensions = self._extract_contour_dimensions(contours)
            any_rectangle_like = any(
                self._is_rectangle_fit(w, h) for w, h in dimensions
            )
            results[color_name] = {"rect": any_rectangle_like}
        return results

    @staticmethod
    def _is_perimeters_fit(contours):
        """
        判断轮廓的周长是否符合条件
        """
        total_perimeter = sum(cv2.arcLength(contour, True) for contour in contours)
        return total_perimeter > 1000

    def calculate_perimeters(self, img_hsv: np.ndarray, results: dict) -> dict:
        """
        计算图像中轮廓的周长
        :param img_hsv: 输入图像 HSV 格式
        :param results: 矩形检测结果
        :return: 周长检测结果
        """
        for color_name, sub_ranges in self.color_ranges.items():
            contours = self._process_contours(img_hsv, sub_ranges)
            perimeter_exceeds = self._is_perimeters_fit(contours)
            if color_name not in results:
                results[color_name] = {}
            results[color_name]["perimeter"] = perimeter_exceeds
        return results

    def detect_light_effects(self, img: np.ndarray, rect=True, peri=False):
        """
        检测图像中的光效 根据参数选择性地检测矩形尺寸和计算周长 轮廓周长检测方法默认不开启
        :param img: 输入图像 RGB 格式
        :param rect: 是否检测矩形效果
        :param peri: 是否计算周长
        """
        # 预处理图像
        img = self._preprocess_img(img)
        # 转换图像为HSV格式
        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        results = {}
        if rect:
            results.update(self.detect_rectangles(img_hsv))
        if peri:
            results.update(self.calculate_perimeters(img_hsv, results))
        return results

    def debug_show_contours(self, img: np.ndarray) -> np.ndarray:
        """
        调试显示图像中的轮廓信息
        """
        img_debug = img.copy()
        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        for color_name, sub_ranges in self.color_ranges.items():
            contours = self._process_contours(img_hsv, sub_ranges)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = max((w / h), (h / w))
                if max(w, h) > 100 and aspect_ratio > 10:
                    cv2.drawContours(img_debug, contour, -1, (0, 0, 255), 1)
                    cv2.rectangle(img_debug, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    format_str = (
                        f"{color_name}:{w}*{h}@({x},{y})" + f"as_rat:{aspect_ratio:.1f}"
                    )
                    if ((x + 300) < 1280) and ((y + h) < (720 - 15)):
                        x = x
                    elif ((x + 300) < 1280) and ((y + h) > (720 - 15)):
                        x = x + w
                    else:
                        x = 1280 - 300
                    text_pos = (
                        x,
                        (y + h + 15) if (y + h + 15) < (720 - 15) else 720 - 15,
                    )
                    cv2.putText(
                        img_debug,
                        format_str,
                        text_pos,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2,
                    )
        return img_debug


detector = lightDetector()
