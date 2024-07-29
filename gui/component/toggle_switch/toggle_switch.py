import sys
from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QBrush, QColor

class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super(ToggleSwitch, self).__init__(parent)
        self.setFixedSize(40, 20)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stateChanged.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        radius = rect.height() / 2

        # Draw the background
        painter.setPen(Qt.PenStyle.NoPen)
        if self.isChecked():
            painter.setBrush(QBrush(QColor(0, 150, 136)))
        else:
            painter.setBrush(QBrush(QColor(204, 204, 204)))
        painter.drawRoundedRect(rect, radius, radius)

        # Draw the handle
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        if self.isChecked():
            handle_rect = QRectF(rect.width() - rect.height(), 0, rect.height(), rect.height())
        else:
            handle_rect = QRectF(0, 0, rect.height(), rect.height())
        painter.drawEllipse(handle_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self.isChecked())
            event.accept()
        else:
            event.ignore()
