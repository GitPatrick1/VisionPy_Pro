# OSDNotification.py

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QTimer, Qt


class OSDNotification(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 180);
                font-size: 28px;
                font-weight: bold;
                padding: 10px 25px;
                border-radius: 15px;
                border: 2px solid white;
            }
        """)
        self.hide()

        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.hide)
        
    def show_notification(self, message, duration=2500):
        self.setText(message)
        self.position_notification()
        self.show()
        self.notification_timer.start(duration)
        
    def position_notification(self):
        if hasattr(self.parent(), 'camera_view'):
            view_rect = self.parent().camera_view.geometry()
            label_size = self.sizeHint()
            
            x = view_rect.x() + (view_rect.width() - label_size.width()) // 2
            y = view_rect.y() + 40
            
            self.setGeometry(x, y, label_size.width(), label_size.height())