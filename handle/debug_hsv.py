#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：大汉头
@Date    ：2024/7/24 23:43 
"""
from functools import reduce
import numpy as np
import os
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

masks_dict = {}  # 用于存储已有hsv范围


def analyze_image(img):
    # 创建一个窗口
    cv2.namedWindow('HSV Range')
    cv2.resizeWindow('HSV Range', 640, 250)

    # 定义回调函数，用于更新HSV阈值
    def nothing(x):
        pass

    # 创建六个滑块，分别对应HSV的最小和最大值，red
    cv2.createTrackbar('H Min', 'HSV Range', 0, 179, nothing)
    cv2.createTrackbar('S Min', 'HSV Range', 0, 255, nothing)
    cv2.createTrackbar('V Min', 'HSV Range', 0, 255, nothing)
    cv2.createTrackbar('H Max', 'HSV Range', 179, 179, nothing)
    cv2.createTrackbar('S Max', 'HSV Range', 255, 255, nothing)
    cv2.createTrackbar('V Max', 'HSV Range', 255, 255, nothing)

    # 加载图像并转换到HSV颜色空间
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    while True:

        # 获取滑块的位置值
        h_min = cv2.getTrackbarPos('H Min', 'HSV Range')
        s_min = cv2.getTrackbarPos('S Min', 'HSV Range')
        v_min = cv2.getTrackbarPos('V Min', 'HSV Range')
        h_max = cv2.getTrackbarPos('H Max', 'HSV Range')
        s_max = cv2.getTrackbarPos('S Max', 'HSV Range')
        v_max = cv2.getTrackbarPos('V Max', 'HSV Range')

        # 根据HSV范围创建掩码
        lower_bound = np.array([h_min, s_min, v_min])
        upper_bound = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(hsv_img, lower_bound, upper_bound)
        masks_list = [mask]

        # 读取masks_dict中的mask
        for key, value in masks_dict.items():
            masks_list.append(cv2.inRange(hsv_img, np.array(value[0]), np.array(value[1])))
        final_mask = reduce(cv2.bitwise_or, masks_list)

        # 使用掩码对原图进行处理
        result = cv2.bitwise_and(img, img, mask=final_mask)
        kernel = np.ones((5, 5), np.uint8)
        final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
        final_mask_3d = cv2.cvtColor(final_mask, cv2.COLOR_GRAY2BGR)
        # 显示结果

        contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            rectangle_info = []
            # 绘制矩形框
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                rectangle_info.append((w, h))
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(final_mask_3d, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.imshow('Result', cv2.resize(np.hstack((result, final_mask_3d)), None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA))

        # 按下ESC键退出
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()

class VideoPlayer:
    def __init__(self, root, video_path):
        self.frame = None
        self.file_name = os.path.basename(video_path)
        self.root = root
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            print("Error: Could not open video.")
            return

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0
        self.updating_progress = False

        self.root.title("Video Player")
        self.root.geometry("1200x800")

        self.canvas = tk.Canvas(root, width=1200, height=700)
        self.canvas.pack()

        self.progress = ttk.Scale(root, from_=0, to=self.total_frames - 1, orient=tk.HORIZONTAL,
                                  command=self.on_progress)
        self.progress.pack(fill=tk.X, padx=10, pady=10)

        self.update_frame()
        self.root.bind('<Left>', self.on_left_key)
        self.root.bind('<Right>', self.on_right_key)
        self.root.bind('<Down>', self.save_current_frame_down)

    def update_frame(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, frame = self.cap.read()
        if not ret:
            return

        text = f"Frame: {self.current_frame}/{self.total_frames}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1152, 648))
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.updating_progress = True
        self.progress.set(self.current_frame)
        self.updating_progress = False
        self.frame = frame  # 添加这行代码来保存当前帧

    def save_current_frame_down(self, event):
        """当按下down键时，分析当前帧"""

        # 将当前帧从BGR转换为RGB
        frame_ = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
        analyze_image(frame_)

    def on_progress(self, value):
        if not self.updating_progress:
            self.current_frame = int(float(value))
            self.update_frame()

    def on_left_key(self, event):
        self.current_frame = max(0, self.current_frame - 1)
        self.update_frame()

    def on_right_key(self, event):
        self.current_frame = min(self.total_frames - 1, self.current_frame + 1)
        self.update_frame()




if __name__ == "__main__":

    video_path = r'D:\Captures\zzz2024-07-19 21-40-19.mp4'  # 替换为你的视频文件路径
    if '.mp4' in video_path:
        root = tk.Tk()
        player = VideoPlayer(root, video_path)
        root.mainloop()
    else:
        analyze_image(video_path)  # 直接识别图片
