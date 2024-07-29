import os
import sys
from pathlib import Path

# Ensure DLL paths are set correctly
dll_path = Path(sys.executable).parent / "Library" / "bin"
current_path = os.environ.get("PATH", "")
if dll_path.exists() and str(dll_path) not in current_path:
    # 将新的目录添加到 PATH 的开始或结束
    # 这里我们添加到末尾，并用分号或冒号（取决于操作系统）分隔
    current_path = str(dll_path) + os.pathsep + current_path

nvidia_path = Path(sys.executable).parent / "Lib" / "site-packages" / "nvidia"
if nvidia_path.exists():
    for bin_path in nvidia_path.iterdir():
        bin_path = bin_path / "bin"
        if bin_path.is_dir() and str(bin_path) not in current_path:
            current_path = str(bin_path) + os.pathsep + current_path
os.environ["PATH"] = current_path  # 重设 PATH 环境变量
sys.path.append(str(Path(__file__).parent))  # 将当前目录添加到 sys.path 中

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from threading import Thread, Event
from pynput.keyboard import Key, Listener
from utils.task import task
from utils import logger, load_characters
import utils
from schema import ZoneMap
from handle import *

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QComboBox, QSlider, QGroupBox, QGridLayout, QLineEdit, QCheckBox, QStackedWidget,
                               QTabWidget, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from component.toggle_switch import ToggleSwitch

# Set the QT_PLUGIN_PATH to the appropriate directory
plugin_path = os.path.join(sys.prefix, "Lib", "site-packages", "PySide6", "plugins")
os.environ["QT_PLUGIN_PATH"] = plugin_path
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(plugin_path, "platforms")


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

        self.tabs.addTab(self.tab1, "零号空洞")
        self.tabs.addTab(self.tab2, "自动战斗(可以直接用零号空洞自动战斗）")
        self.tabs.addTab(self.tab3, "待开发")

        # Set tab layout
        self.tab1.layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2.layout)

        self.tab3.layout = QVBoxLayout()
        self.tab3.setLayout(self.tab3.layout)


        # Add components to tab1 (零号空洞)
        self.add_zero_hollow_tab_components()
        # TODO: use different connect function, then uncomment this
        # self.add_auto_battle_tab_components()

        self.layout.addWidget(self.tabs)

        self.task_thread = None
        self.stop_event = Event()


    def add_hollow_config_components(self, tab):
        # zone/level group
        self.zone_level_group = QGroupBox("地图设置")
        self.zone_level_layout = QHBoxLayout()
        self.zone_combo = QComboBox()
        self.zone_combo.addItems([zone_info["name"] for zone_info in ZoneMap.values()])
        self.level_combo = QComboBox()
        self.level_combo.addItems(ZoneMap[utils.config.targetMap.zone]["level"].values())
        self.zone_combo.setCurrentIndex(utils.config.targetMap.zone - 1)
        self.level_combo.setCurrentIndex(utils.config.targetMap.level - 1)
        self.zone_level_layout.addWidget(self.zone_combo)
        self.zone_level_layout.addWidget(self.level_combo)
        self.zone_level_group.setLayout(self.zone_level_layout)

        self.zone_combo.currentIndexChanged.connect(self.zone_changed)
        self.level_combo.currentIndexChanged.connect(self.level_changed)

        # mode group
        self.mode_input_group = QGroupBox("模式设置")
        self.mode_input_layout = QHBoxLayout()
        self.mode_input_combo = QComboBox()
        self.mode_input_combo.addItems([str(i) for i in range(1, 4)])
        self.mode_input_combo.setCurrentIndex(utils.config.modeSelect-1)
        self.mode_input_layout.addWidget(self.mode_input_combo)
        self.mode_input_group.setLayout(self.mode_input_layout)

        self.mode_input_combo.currentIndexChanged.connect(self.mode_changed)

        # time group
        self.time_group = QGroupBox("时间设置")
        self.time_layout = QHBoxLayout()
        self.max_map_time_input = QLineEdit(str(utils.config.maxMapTime))
        self.max_fight_time_input = QLineEdit(str(utils.config.maxFightTime))
        self.time_layout.addWidget(QLabel("最大地图时间"))
        self.time_layout.addWidget(self.max_map_time_input)
        self.time_layout.addWidget(QLabel("最大战斗时间"))
        self.time_layout.addWidget(self.max_fight_time_input)
        self.time_group.setLayout(self.time_layout)

        self.max_map_time_input.editingFinished.connect(self.update_max_map_time)
        self.max_fight_time_input.editingFinished.connect(self.update_max_fight_time)

        # Check group
        self.check_group = QGroupBox("勾选设置")
        self.check_layout = QHBoxLayout()  # Use QHBoxLayout to keep them on the same row

        # Use a QVBoxLayout to group each label and toggle switch closer together
        group1_layout = QVBoxLayout()
        row1_layout = QHBoxLayout()
        self.has_boom_label = QLabel("使用炸弹")
        self.has_boom_input = ToggleSwitch()
        self.has_boom_input.setChecked(utils.config.hasBoom)
        row1_layout.addWidget(self.has_boom_label)
        row1_layout.addWidget(self.has_boom_input)
        row1_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        group1_layout.addLayout(row1_layout)

        group2_layout = QVBoxLayout()
        row2_layout = QHBoxLayout()
        self.use_gpu_label = QLabel("使用GPU")
        self.use_gpu_input = ToggleSwitch()
        self.use_gpu_input.setChecked(utils.config.useGpu)
        row2_layout.addWidget(self.use_gpu_label)
        row2_layout.addWidget(self.use_gpu_input)
        row2_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        group2_layout.addLayout(row2_layout)

        # Add both group layouts to the main horizontal layout
        self.check_layout.addLayout(group1_layout)
        self.check_layout.addLayout(group2_layout)

        self.check_group.setLayout(self.check_layout)

        self.has_boom_input.stateChanged.connect(self.update_has_boom)
        self.use_gpu_input.stateChanged.connect(self.update_use_gpu)

        # 鸣徽 group
        self.sel_buff_group = QGroupBox("鸣徽设置")
        self.sel_buff_layout = QHBoxLayout()
        self.sel_buff_input = QLineEdit(", ".join(utils.config.selBuff))
        self.sel_buff_layout.addWidget(self.sel_buff_input)
        self.sel_buff_group.setLayout(self.sel_buff_layout)

        self.sel_buff_input.editingFinished.connect(self.update_sel_buff)

        # characters group
        self.characters_group = QGroupBox("人物设置")
        self.characters_layout = QHBoxLayout()
        self.characters_input = QLineEdit(", ".join(utils.config.characters))
        self.characters_layout.addWidget(self.characters_input)
        self.characters_group.setLayout(self.characters_layout)

        self.characters_input.editingFinished.connect(self.update_characters)


        tab.layout.addWidget(self.zone_level_group)
        tab.layout.addWidget(self.mode_input_group)
        tab.layout.addWidget(self.time_group)
        tab.layout.addWidget(self.check_group)
        tab.layout.addWidget(self.sel_buff_group)
        tab.layout.addWidget(self.characters_group)

    # TODO: use different connect function
    def add_auto_battle_config_components(self, tab):
        # time group
        self.time_group_tab2 = QGroupBox("时间设置")
        self.time_layout_tab2 = QHBoxLayout()
        self.max_fight_time_input_tab2 = QLineEdit(str(utils.config.maxFightTime))
        self.time_layout_tab2.addWidget(QLabel("最大战斗时间"))
        self.time_layout_tab2.addWidget(self.max_fight_time_input_tab2)
        self.time_group_tab2.setLayout(self.time_layout_tab2)

        self.max_fight_time_input_tab2.editingFinished.connect(
            lambda: self.update_max_fight_time(self.max_fight_time_input_tab2))

        # check group
        self.check_group_tab2 = QGroupBox("勾选设置")
        self.check_layout_tab2 = QHBoxLayout()
        self.use_gpu_input_tab2 = QCheckBox("Use GPU")
        self.use_gpu_input_tab2.setChecked(utils.config.useGpu)
        self.check_layout_tab2.addWidget(self.use_gpu_input_tab2)
        self.check_group_tab2.setLayout(self.check_layout_tab2)

        self.use_gpu_input_tab2.stateChanged.connect(lambda: self.update_use_gpu(self.use_gpu_input_tab2))

        # characters group
        self.characters_group_tab2 = QGroupBox("人物设置")
        self.characters_layout_tab2 = QHBoxLayout()
        self.characters_input_tab2 = QLineEdit(", ".join(utils.config.characters))
        self.characters_layout_tab2.addWidget(self.characters_input_tab2)
        self.characters_group_tab2.setLayout(self.characters_layout_tab2)

        self.characters_input_tab2.editingFinished.connect(lambda: self.update_characters(self.characters_input_tab2))

        tab.layout.addWidget(self.time_group_tab2)
        tab.layout.addWidget(self.check_group_tab2)
        tab.layout.addWidget(self.characters_group_tab2)

    def add_status_components(self, tab):
        # Status Group
        self.status_group = QGroupBox("当前状态 空闲")
        self.status_layout = QHBoxLayout()
        self.start_button = QPushButton("开始 (F9)")
        self.restart_button = QPushButton("恢复 (F10)")
        self.pause_button = QPushButton("暂停 (F11)")
        self.stop_button = QPushButton("停止 (F12)")

        self.status_layout.addWidget(self.start_button)
        self.status_layout.addWidget(self.restart_button)
        self.status_layout.addWidget(self.pause_button)
        self.status_layout.addWidget(self.stop_button)
        self.status_group.setLayout(self.status_layout)

        # Connect the buttons to their functions
        self.start_button.clicked.connect(self.start_action)
        self.restart_button.clicked.connect(self.restart_action)
        self.pause_button.clicked.connect(self.pause_action)
        self.stop_button.clicked.connect(self.stop_action)

        # Add groups to the tab layout
        tab.layout.addWidget(self.status_group)

    def add_zero_hollow_tab_components(self):
        self.add_hollow_config_components(self.tab1)
        self.add_status_components(self.tab1)

    def add_auto_battle_tab_components(self):
        self.add_auto_battle_config_components(self.tab2)
        self.add_status_components(self.tab2)

    # TODO: keep level unchanged when zone changed
    def update_level_combo(self, zone_index):
        self.level_combo.clear()
        levels = ZoneMap[zone_index]["level"].values()
        self.level_combo.addItems(levels)
        utils.config.targetMap.level = len(levels)
        self.level_combo.setCurrentIndex(utils.config.targetMap.level - 1)

    def zone_changed(self, index):
        zone_index = index + 1  # Adjust for 1-based indexing
        utils.config.targetMap.zone = zone_index
        self.update_level_combo(zone_index)
        zone_name = ZoneMap[utils.config.targetMap.zone]["name"]
        logger.info(f"zone设为: {zone_name}")

    def level_changed(self, index):
        utils.config.targetMap.level = index + 1
        if utils.config.targetMap.level in ZoneMap[utils.config.targetMap.zone]["level"]:
            level_name = ZoneMap[utils.config.targetMap.zone]["level"][utils.config.targetMap.level]
            logger.info(f"level设为: {level_name}")

    def mode_changed(self, index):
        utils.config.modeSelect = index + 1
        logger.info(f"模式设为: {utils.config.modeSelect}")

    def update_max_map_time(self):
        utils.config.maxMapTime = int(self.max_map_time_input.text())
        logger.info(f"最大跑图时间设为: {utils.config.maxMapTime}")

    def update_max_fight_time(self):
        utils.config.maxFightTime = int(self.max_fight_time_input.text())
        logger.info(f"最大战斗时间设为: {utils.config.maxFightTime}")

    def update_has_boom(self):
        utils.config.hasBoom = self.has_boom_input.isChecked()
        logger.info(f"使用炸弹设为: {utils.config.hasBoom}")

    def update_use_gpu(self):
        utils.config.useGpu = self.use_gpu_input.isChecked()
        logger.info(f"使用gpu设为: {utils.config.useGpu}")

    def update_sel_buff(self):
        utils.config.selBuff = self.sel_buff_input.text().split(", ")
        logger.info(f"鸣徽buff设为: {utils.config.selBuff}")

    def update_characters(self):
        utils.config.characters = self.characters_input.text().split(", ")
        utils.characters_icons = load_characters(utils.config)
        logger.info(f"角色设为: {utils.characters_icons.keys()}")

    def start_action(self):
        if self.task_thread is None:
            logger.debug("Starting task thread...")
            self.stop_event.clear()
            self.task_thread = Thread(target=self.run_task)
            self.task_thread.start()

    def restart_action(self):
        if self.task_thread is not None:
            logger.debug("Restarting task...")
            task.restart()

    def pause_action(self):
        if self.task_thread is not None:
            logger.debug("Pausing task...")
            task.pause()

    def stop_action(self):
        if self.task_thread is not None:
            logger.debug("Stopping task thread...")
            self.stop_event.set()
            task.stop()
            self.task_thread.join()
            logger.debug("Task thread completed.")
            self.task_thread = None

    def run_task(self):
        def key_event():
            def on_press(key):
                if key == Key.f10:
                    self.restart_action()
                elif key == Key.f11:
                    self.pause_action()
                elif key == Key.f12:
                    self.stop_action()
                    self.stop_event.set()

            listener = Listener(on_press=on_press)
            listener.start()

            while not self.stop_event.is_set():
                self.stop_event.wait(1)

            listener.stop()

        key_thread = Thread(target=key_event)
        key_thread.start()

        logger.debug("Starting task run...")
        while not self.stop_event.is_set():
            task.run()
        logger.debug("Task run completed.")
        key_thread.join()
        logger.debug("Key thread completed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())