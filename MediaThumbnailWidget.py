# MediaThumbnailWidget.py

import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal, QSize

class MediaThumbnailWidget(QWidget):
    clicked = pyqtSignal(str)
    delete_requested = pyqtSignal(str)

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.is_image = self.file_name.lower().endswith(('.png', '.jpg', '.jpeg'))
        
        self.setFixedSize(170, 190)
        self.setStyleSheet("""
            MediaThumbnailWidget {
                border: 1px solid #555; 
                border-radius: 10px;
                background-color: #2D2D30;
            }
            MediaThumbnailWidget:hover {
                border: 2px solid #007AFF;
            }
        """)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.preview_label = QLabel()
        self.preview_label.setFixedSize(160, 120)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background-color: #3C3C3C; border-radius: 5px;")
        
        if self.is_image:
            self.load_image_thumbnail()
        else:
            self.load_video_thumbnail()
            
        layout.addWidget(self.preview_label)

        self.name_label = QLabel(self.file_name)
        self.name_label.setWordWrap(True)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("color: white; font-size: 10px;")
        layout.addWidget(self.name_label)

        self.delete_button = QPushButton("✕")
        self.delete_button.setFixedSize(24, 24)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30;
                color: white;
                font-weight: bold;
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #D70015;
            }
        """)
        self.delete_button.clicked.connect(self.request_delete)
        self.delete_button.hide()

    def load_image_thumbnail(self):
        pixmap = QPixmap(self.file_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(160, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.preview_label.setPixmap(scaled_pixmap)

    def load_video_thumbnail(self):
        self.preview_label.setText("🎬")
        self.preview_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #3C3C3C;
                font-size: 40px;
                border-radius: 5px;
            }
        """)

    def mousePressEvent(self, event):
        if not self.delete_button.geometry().contains(event.pos()):
            self.clicked.emit(self.file_path)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.delete_button.show()
        self.delete_button.move(self.width() - self.delete_button.width() - 5, 5)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.delete_button.hide()
        super().leaveEvent(event)

    def request_delete(self):
        self.delete_requested.emit(self.file_path)