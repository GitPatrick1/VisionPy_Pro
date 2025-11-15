# PreviewWidget.py

import cv2
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class PreviewWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); border-radius: 10px;")
        self.hide()
        
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.hide)
        
    def show_preview(self, frame, duration=3000):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        preview_size = min(self.parent().width() // 3, self.parent().height() // 3)
        self.setPixmap(
            pixmap.scaled(
                preview_size, preview_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        
        self.resize(preview_size + 20, preview_size + 20)
        self.move(
            (self.parent().width() - preview_size) // 2,
            (self.parent().height() - preview_size) // 2
        )
        self.show()
        self.preview_timer.start(duration)