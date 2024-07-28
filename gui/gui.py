import os
import sys
import subprocess
import pyautogui
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QComboBox, QSlider, QGroupBox, QGridLayout, QLineEdit, QCheckBox, QStackedWidget,
                               QTabWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("绝区零-自动化")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Create tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "闪避助手")
        self.tabs.addTab(self.tab2, "自动战斗")
        self.tabs.addTab(self.tab3, "指令调试")

        # Set tab layout
        self.tab1.layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2.layout)

        self.tab3.layout = QVBoxLayout()
        self.tab3.setLayout(self.tab3.layout)

        # Add components to tab2 (自动战斗)
        self.add_auto_battle_tab_components()

        self.layout.addWidget(self.tabs)

    def add_auto_battle_tab_components(self):
        # Fight Configuration Group
        self.fight_config_group = QGroupBox("战斗配置")
        self.fight_config_layout = QVBoxLayout()
        self.fight_config_label = QLabel("请选以当前窗口做一次清晰截图，配置文件存在 config/auto_battle 文件夹，删除会恢复默认配置")
        self.fight_config_buttons_layout = QHBoxLayout()
        self.fight_config_button1 = QPushButton("击破战场-强攻进刃")
        self.fight_config_button1.setShortcut("F12")
        self.fight_config_button2 = QPushButton("删除")

        self.fight_config_buttons_layout.addWidget(self.fight_config_button1)
        self.fight_config_buttons_layout.addWidget(self.fight_config_button2)
        self.fight_config_layout.addWidget(self.fight_config_label)
        self.fight_config_layout.addLayout(self.fight_config_buttons_layout)
        self.fight_config_group.setLayout(self.fight_config_layout)

        # GPU Computation Group
        self.gpu_computation_group = QGroupBox("GPU运算")
        self.gpu_computation_layout = QHBoxLayout()
        self.gpu_computation_label = QLabel("游戏画面结构稳定性，可以不用启用。保证在硬解码推动时在50ms内即可")
        self.gpu_computation_checkbox = QCheckBox()
        self.gpu_computation_checkbox.setChecked(True)
        self.gpu_computation_layout.addWidget(self.gpu_computation_label)
        self.gpu_computation_layout.addWidget(self.gpu_computation_checkbox)
        self.gpu_computation_group.setLayout(self.gpu_computation_layout)

        # Screenshot Interval Group
        self.screenshot_interval_group = QGroupBox("截图间隔(秒)")
        self.screenshot_interval_layout = QHBoxLayout()
        self.screenshot_interval_label = QLabel("游戏画面结构稳定性，可以通过加大截图间隔（保证在极短间隔+推动时在50ms内即可）")
        self.screenshot_interval_input = QLineEdit("0.02")
        self.screenshot_interval_layout.addWidget(self.screenshot_interval_label)
        self.screenshot_interval_layout.addWidget(self.screenshot_interval_input)
        self.screenshot_interval_group.setLayout(self.screenshot_interval_layout)

        # Controller Type Group
        self.controller_type_group = QGroupBox("手柄类型")
        self.controller_type_layout = QHBoxLayout()
        self.controller_type_combo = QComboBox()
        self.controller_type_combo.addItems(["无"])
        self.controller_type_layout.addWidget(self.controller_type_combo)
        self.controller_type_group.setLayout(self.controller_type_layout)

        # Status Group
        self.status_group = QGroupBox("当前状态 空闲")
        self.status_layout = QHBoxLayout()
        self.start_button = QPushButton("开始 F9")
        self.stop_button = QPushButton("停止 F10")
        self.status_layout.addWidget(self.start_button)
        self.status_layout.addWidget(self.stop_button)
        self.status_group.setLayout(self.status_layout)

        # Add groups to the tab layout
        self.tab2.layout.addWidget(self.fight_config_group)
        self.tab2.layout.addWidget(self.gpu_computation_group)
        self.tab2.layout.addWidget(self.screenshot_interval_group)
        self.tab2.layout.addWidget(self.controller_type_group)
        self.tab2.layout.addWidget(self.status_group)

        # Connect the start button to the function
        self.start_button.clicked.connect(self.start_action)
    def start_action(self):
        try:
            subprocess.run(["python", "main.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the command: {e}")

    def stop_action(self):
        try:
            pyautogui.press('enter')
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the command: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
