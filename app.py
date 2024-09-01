# -*- coding: utf-8 -*-
""" 
@file:      app.py
@time:      2024/8/11 下午1:18
@author:    sMythicalBird
"""
import os
import sys
from pathlib import Path

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


import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
