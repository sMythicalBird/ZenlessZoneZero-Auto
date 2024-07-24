import cv2
import numpy as np
import matplotlib.pyplot as plt # 调试用，非必须
import os


class LightEffectDetector:
    def __init__(self, img, color_ranges):
        # 初始化图像、颜色范围、形态学操作的卷积核
        self.img = img
        self._preprocess_img()
        self.img_hsv = cv2.cvtColor(self.img_np, cv2.COLOR_RGB2HSV)
        self.color_ranges = color_ranges
        self.kernel = np.ones((5, 5), np.uint8)  # 形态学操作使用的卷积核
        self.kernel_size = 1
        self.kernel_V = cv2.getStructuringElement(
            cv2.MORPH_RECT, (self.kernel_size, self.kernel_size * 60))
        self.kernel_H = cv2.getStructuringElement(
            cv2.MORPH_RECT, (self.kernel_size * 60, self.kernel_size))
        self.results = {}  # 存储检测结果的字典

    def _preprocess_img(self):
        # 预处理图像，裁剪左上角能量显示、右下角技能显示、右上角BOSS血条部分，避免识别黄色光效时干扰
        img = self.img_np = cv2.cvtColor(
            cv2.imread(self.img), cv2.COLOR_BGR2RGB)
        x1, y1, w, h = 60, 120, 220, 40  # 左上角能量显示
        x2, y2 = x1 + w, y1 + h
        img[y1:y2, x1:x2, :] = 0
        x1_1, y1_1, w_1, h_1 = 1160, 520, 50, 160  # 右下角技能显示
        x2_1, y2_1 = x1_1 + w_1, y1_1 + h_1
        img[y1_1:y2_1, x1_1:x2_1, :] = 0
        x2_1, y2_1, w_2, h_2 = 460, 2, 380, 32  # 右上角BOSS血条部分
        x2_1, y2_1 = x2_1 + w_2, y2_1 + h_2
        img[y2_1:y2_1+h_2, x2_1:x2_1+w_2, :] = 0
        self.img_np = img

    def _process_contours(self, img_hsv, color_ranges):
        # 根据颜色范围创建掩码，进行形态学操作，并找到轮廓
        mask1 = np.zeros_like(img_hsv[:, :, 0])
        for _, color_range in color_ranges.items():
            lower_color, upper_color = color_range
            mask = cv2.inRange(img_hsv, lower_color, upper_color)
            mask1 = cv2.bitwise_or(mask1, mask)
        mask2_1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, self.kernel_H)
        mask2_2 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, self.kernel_V)
        mask2 = cv2.bitwise_and(mask2_1, mask2_2)
        contours, _ = cv2.findContours(
            mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours

    def _extract_contour_dimensions(self, contours):
        # 从轮廓中提取尺寸信息
        dimensions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            dimensions.append((w, h))  # 存储宽度和高度
        return dimensions

    def _is_rectangle_fit(self, width, height):
        # 判断尺寸是否符合特定矩形条件
        aspect_ratio = max((width / height), (height / width))
        return (aspect_ratio > 5) and max(width, height) > 50

    def detect_rectangles(self):
        # 检测图像中的矩形效果
        self.results = {}
        for color_name, subranges in self.color_ranges.items():
            contours = self._process_contours(self.img_hsv, subranges)
            dimensions = self._extract_contour_dimensions(contours)
            any_rectangle_like = any(self._is_rectangle_fit(w, h)
                                     for w, h in dimensions)
            self.results[color_name] = {'rect': any_rectangle_like}
        return self.results

    def _is_perimeters_fit(self, contours):
        # 判断轮廓的总周长是否超过特定值
        total_perimeter = sum(cv2.arcLength(contour, True)
                              for contour in contours)
        return total_perimeter > 1000

    def calculate_perimeters(self):
        # 计算并存储每个颜色轮廓的周长信息
        for color_name, subranges in self.color_ranges.items():
            contours = self._process_contours(self.img_hsv, subranges)
            perimeter_exceeds = self._is_perimeters_fit(contours)
            if color_name not in self.results:
                self.results[color_name] = {}
            self.results[color_name]['perimeter'] = perimeter_exceeds

        return self.results

    def detect_light_effects(self, rect=True, peri=False):
        # 根据参数选择性地检测矩形尺寸和计算周长
        # 轮廓周长检测方法默认不开启
        results = {}
        if rect:
            results.update(self.detect_rectangles())
        if peri:
            results.update(self.calculate_perimeters())
        return results

    def debug_show_contours(self):
        # 调试用，显示图像中的轮廓和外扩矩形及数据
        img_np_debug = self.img_np.copy()
        for color_name, subranges in self.color_ranges.items():
            contours = self._process_contours(self.img_hsv, subranges)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = max((w / h), (h / w))
                if max(w, h) > 50 and aspect_ratio > 5:
                    cv2.drawContours(img_np_debug, contour, -1, (0, 0, 255), 1)
                    cv2.rectangle(img_np_debug, (x, y),
                                  (x + w, y + h), (0, 255, 255), 1)
                    format_str = (
                        f"rect:{w}*{h}@({x},{y})"
                        f"aspect ratio:{aspect_ratio:.1f}"
                    )
                    if ((x + 300) < 1280) and ((y + h) < (720 - 15)):
                        x = x
                    elif ((x + 300) < 1280) and ((y + h) > (720 - 15)):
                        x = x + w
                    else:
                        x = 1280 - 300
                    text_pos = (
                        x,
                        (y + h + 15) if (y + h + 15) < (720 - 15) else 720 - 15
                    )
                    cv2.putText(img_np_debug, format_str, text_pos,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        return img_np_debug


# 传入自定义的光效颜色范围参数：黄色
lower_hsv_yellow = np.array([15, 80, 160])
upper_hsv_yellow = np.array([35, 255, 255])
# 传入自定义的光效颜色范围参数：红色
lower_hsv_red_1 = np.array([170, 70, 255])  # 红色HSV范围对应0-180度，需分段处理
upper_hsv_red_1 = np.array([180, 200, 255])
lower_hsv_red_2 = np.array([0, 70, 255])
upper_hsv_red_2 = np.array([10, 200, 255])

color_ranges = {
    'yellow':
        {
            'yellow_1': (lower_hsv_yellow, upper_hsv_yellow),
        },
    'red':
        {
            'red_1': (lower_hsv_red_1, upper_hsv_red_1),
            'red_2': (lower_hsv_red_2, upper_hsv_red_2),
        }
}

# 测试用例


def detector_test(img_path):
    # 创建光效检测器实例
    detector = LightEffectDetector(img_path, color_ranges)

    results = detector.detect_light_effects(rect=True, peri=False)

    img = detector.debug_show_contours()

    fig1, ax1 = plt.subplots(figsize=(12.8, 7.2))
    ax1.axis('off')
    ax1.imshow(img)
    plt.show()

    # 打印结果
    print(os.path.split(img_path)[-1])
    print(results)


for img in os.listdir("screenshots\\fight_sight"):
    detector_test(os.path.join("screenshots\\fight_sight", img))
