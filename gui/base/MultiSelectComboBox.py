# -*- coding: utf-8 -*-
"""
@file:      MultiSelectComboBox
@time:      2024/8/21 19:28
@author:    sMythicalBird
"""
from PySide6.QtWidgets import (
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QCheckBox,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
)
from PySide6.QtCore import Qt, Signal


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.addStretch()  # 添加一个伸缩空间，将元素推到左侧
        self.setStyleSheet("background: transparent; border: none;")


class MultiSelectComboBox(QComboBox):
    selectionChanged = Signal(list)

    def __init__(
        self,
        selected_items: list[str],
        options: list[str],
        max_sel_num: int = 10000,
        parent=None,
    ):
        super().__init__(parent)
        self.setEditable(True)
        self.customLineEdit = CustomLineEdit(self)
        self.setLineEdit(self.customLineEdit)
        self.listWidget = QListWidget()
        self.setModel(self.listWidget.model())
        self.setView(self.listWidget)
        self.selected_items = selected_items
        if (
            len(selected_items) > max_sel_num
        ):  # 如果已经选择的选项超过最大选择数，只保留前max_sel_num个
            self.selected_items = selected_items[:max_sel_num]
        self.addItems(options)  # 添加选项
        self.selected_cnt = max_sel_num
        self.init_select()
        self.update_display()

    # 初始化选项
    def init_select(self):
        for text in self.selected_items:
            for index in range(self.listWidget.count()):
                item = self.listWidget.item(index)
                checkbox: QCheckBox = self.listWidget.itemWidget(item)
                if checkbox.text() == text:
                    checkbox.setCheckState(Qt.CheckState.Checked)

    # 添加选项
    def addItems(self, texts):
        for text in texts:
            item = QListWidgetItem(self.listWidget)
            checkbox = QCheckBox(text)
            checkbox.stateChanged.connect(self.update_selection)
            self.listWidget.setItemWidget(item, checkbox)

    # 更新选择
    def update_selection(self, state):
        checkbox = self.sender()
        if state == 2:
            if checkbox.text() not in self.selected_items:
                if (
                    len(self.selected_items) == self.selected_cnt
                ):  # 如果已经选择了3个，删除第一个
                    self.remove_item(self.selected_items[0])
                self.selected_items.append(checkbox.text())
        else:
            if checkbox.text() in self.selected_items:
                self.selected_items.remove(checkbox.text())
        self.update_display()
        self.selectionChanged.emit(self.selected_items)

    # 更新显示内容
    def update_display(self):
        # 清除所有选项
        while self.customLineEdit.layout.count() > 1:
            item = self.customLineEdit.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # 根据selected_items重新绘制布局
        for item in self.selected_items:
            widget = QWidget()
            layout = QHBoxLayout(widget)
            label = QLabel(item)
            button = QPushButton("x")
            button.setFlat(True)
            button.setStyleSheet("background: transparent;")
            button.setFixedSize(25, 25)
            button.clicked.connect(lambda _, text=item: self.remove_item(text))
            layout.addWidget(label)
            layout.addWidget(button)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(layout)
            widget.setStyleSheet("border-radius: 5px; background-color: #f0f0f0; ")
            self.customLineEdit.layout.insertWidget(
                self.customLineEdit.layout.count() - 1, widget
            )

    # 移除选项
    def remove_item(self, text):
        if text in self.selected_items:
            self.selected_items.remove(text)
            for index in range(self.listWidget.count()):
                item = self.listWidget.item(index)
                checkbox: QCheckBox = self.listWidget.itemWidget(item)
                if checkbox.text() == text:
                    checkbox.setCheckState(Qt.CheckState.Unchecked)
                    break
            self.update_display()

    def set_width(self, width):
        self.setFixedWidth(width)

    def set_height(self, height):
        self.setFixedHeight(height)
