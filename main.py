#!/usr/bin/env python3
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from MainWindow import MainWindow

def main():
    # Assicurati che le directory necessarie esistano
    os.makedirs(os.path.expanduser("~/VisionPy_Pro/photos"), exist_ok=True)
    os.makedirs(os.path.expanduser("~/VisionPy_Pro/videos"), exist_ok=True)
    
    # Crea l'applicazione PyQt6
    app = QApplication(sys.argv)
    app.setApplicationName("VisionPy Pro")
    
    # Imposta uno stile moderno per una migliore resa grafica
    app.setStyle("Fusion")
    
    # Crea e mostra la finestra principale
    window = MainWindow()
    window.show()
    
    # Esegui il loop dell'applicazione
    sys.exit(app.exec())

if __name__ == "__main__":
    main()