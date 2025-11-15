# CameraWidget.py (VERSIONE CORRETTA E ROBUSTA)

import cv2
import numpy as np
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage

class CameraWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #1e1e1e; border-radius: 10px;")
        self.setMinimumSize(800, 600)
        
    def update_frame(self, rgb_frame):
        """
        Aggiorna il widget con un nuovo frame.
        rgb_frame: un array NumPy in formato RGB.
        """
        if rgb_frame is not None:
            h, w, ch = rgb_frame.shape
            
            # --- METODO ROBUSTO PER CREARE LA QIMAGE ---
            # 1. Assicurati che l'array sia C-contiguo e del tipo di dati corretto (uint8)
            try:
                # Calcola i byte per riga
                bytes_per_line = ch * w
                
                # Crea l'immagine usando un puntatore ai dati dell'array
                # Questo è il modo più affidabile per convertire array NumPy in QImage
                qt_image = QImage(rgb_frame.data.tobytes(), w, h, bytes_per_line, QImage.Format.Format_RGB888)
                
                # Crea la QPixmap dalla QImage
                pixmap = QPixmap.fromImage(qt_image)
                
                # Mostra la pixmap scalata per adattarsi al widget
                self.setPixmap(
                    pixmap.scaled(
                        self.size(), 
                        Qt.AspectRatioMode.KeepAspectRatio, 
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
            except Exception as e:
                # In caso di errore di conversione, stampa l'errore e mostra un messaggio
                print(f"Errore nella conversione del frame: {e}")
                self.setText("Errore di visualizzazione")