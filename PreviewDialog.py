# PreviewDialog.py

import os
import math
from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QScrollArea)
from PyQt6.QtGui import QPixmap, QFont, QKeyEvent
from PyQt6.QtCore import Qt

class PreviewDialog(QDialog):
    def __init__(self, file_paths, initial_index, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Anteprima Media")
        self.setModal(True)
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        
        self.file_paths = sorted(file_paths)
        self.current_index = initial_index
        
        self.init_ui()
        self.load_media(self.current_index)

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.media_label = QLabel()
        self.media_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.media_label)
        main_layout.addWidget(self.scroll_area)

        self.info_label = QLabel()
        self.info_label.setFont(QFont("Arial", 10))
        self.info_label.setStyleSheet("padding: 10px; background-color: #3C3C3C; border-radius: 5px;")
        main_layout.addWidget(self.info_label)

        nav_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("◀ Precedente")
        self.prev_button.clicked.connect(self.show_previous)
        
        self.next_button = QPushButton("Successivo ▶")
        self.next_button.clicked.connect(self.show_next)
        
        self.close_button = QPushButton("Chiudi")
        self.close_button.clicked.connect(self.accept)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.close_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_button)
        
        main_layout.addLayout(nav_layout)

    def load_media(self, index):
        if not 0 <= index < len(self.file_paths):
            return

        self.current_index = index
        file_path = self.file_paths[index]
        file_name = os.path.basename(file_path)
        
        self.prev_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < len(self.file_paths) - 1)

        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.media_label.setPixmap(pixmap)
            else:
                self.media_label.setText("Impossibile caricare l'immagine.")
        else:
            self.media_label.setText(f"🎬\n\n{file_name}\n\n(Per riprodurre, apri con un lettore multimediale esterno)")
            self.media_label.setStyleSheet("font-size: 24px;")

        try:
            size = os.path.getsize(file_path)
            mtime = os.path.getmtime(file_path)
            mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            info_text = (
                f"<b>File:</b> {file_name}<br>"
                f"<b>Percorso:</b> {file_path}<br>"
                f"<b>Dimensione:</b> {self.format_size(size)}<br>"
                f"<b>Modificato il:</b> {mod_time}"
            )
            self.info_label.setText(info_text)
        except Exception as e:
            self.info_label.setText(f"Impossibile leggere le informazioni del file: {e}")

    def format_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
        
    def show_previous(self):
        if self.current_index > 0:
            self.load_media(self.current_index - 1)

    def show_next(self):
        if self.current_index < len(self.file_paths) - 1:
            self.load_media(self.current_index + 1)
            
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Left:
            self.show_previous()
        elif event.key() == Qt.Key.Key_Right:
            self.show_next()
        elif event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)