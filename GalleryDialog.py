# GalleryDialog.py (VERSIONE MIGLIORATA)

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QScrollArea, QWidget, QGridLayout, QPushButton,
                            QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from MediaThumbnailWidget import MediaThumbnailWidget
from PreviewDialog import PreviewDialog

class GalleryDialog(QDialog):
    def __init__(self, photo_dir, video_dir, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Galleria")
        self.setModal(False)
        self.setGeometry(150, 150, 900, 700)

        self.photo_dir = photo_dir
        self.video_dir = video_dir
        self.all_media_paths = []

        self.init_ui()
        self.load_media()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.refresh_btn = QPushButton("Aggiorna Galleria")
        self.refresh_btn.clicked.connect(self.load_media)
        layout.addWidget(self.refresh_btn)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")

        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

    def load_media(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        self.all_media_paths.clear()

        self.load_photos()
        self.load_videos()

    def load_photos(self):
        if not os.path.exists(self.photo_dir):
            return
        files = sorted([f for f in os.listdir(self.photo_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        for filename in files:
            path = os.path.join(self.photo_dir, filename)
            self.all_media_paths.append(path)
            self.create_and_add_thumbnail(path)
            
    def load_videos(self):
        if not os.path.exists(self.video_dir):
            return
        files = sorted([f for f in os.listdir(self.video_dir) if f.lower().endswith('.mp4')])
        for filename in files:
            path = os.path.join(self.video_dir, filename)
            self.all_media_paths.append(path)
            self.create_and_add_thumbnail(path)

    def create_and_add_thumbnail(self, path):
        thumbnail = MediaThumbnailWidget(path, self)
        thumbnail.clicked.connect(self.on_thumbnail_clicked)
        thumbnail.delete_requested.connect(self.on_delete_requested)
        
        row, col = divmod(self.grid_layout.count(), 4)
        self.grid_layout.addWidget(thumbnail, row, col)

    def on_thumbnail_clicked(self, file_path):
        try:
            index = self.all_media_paths.index(file_path)
            preview_dialog = PreviewDialog(self.all_media_paths, index, self)
            preview_dialog.exec()
        except ValueError:
            print(f"Errore: percorso {file_path} non trovato nella lista.")

    def on_delete_requested(self, file_path):
        reply = QMessageBox.question(
            self, 'Conferma Cancellazione',
            f"Sei sicuro di voler cancellare '{os.path.basename(file_path)}'?\n\nQuesta azione è irreversibile.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path)
                self.load_media()
            except OSError as e:
                QMessageBox.critical(self, "Errore di Cancellazione", f"Impossibile cancellare il file:\n{e}")