# -*- coding: utf-8 -*-
""" 
@file:      app.py
@time:      2024/8/11 下午1:18
@author:    sMythicalBird
"""
import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
