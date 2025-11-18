from enum import Enum
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class DeviceType(Enum):
    """Enum per i tipi di dispositivo supportati"""
    PC = "pc"
    JETSON_NANO = "jetson_nano"
    RASPBERRY_PI = "raspberry_pi"

class DeviceSelectionDialog(QDialog):
    """Dialog per la selezione del dispositivo all'avvio dell'applicazione"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("VisionPy Pro - Selezione Dispositivo")
        self.setModal(True)
        self.setGeometry(400, 250, 550, 450)
        self.selected_device = None
        self.init_ui()
        
    def init_ui(self):
        """Inizializza l'interfaccia utente"""
        layout = QVBoxLayout(self)
        
        # Titolo
        title = QLabel("Seleziona il tuo dispositivo")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Descrizione
        description = QLabel(
            "VisionPy Pro supporta diversi dispositivi con pipeline ottimizzate.\n"
            "Seleziona il dispositivo che stai utilizzando:"
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("color: #888; margin: 10px 0px;")
        layout.addWidget(description)
        
        # Gruppo PC (Webcam USB)
        pc_group = QGroupBox("🖥️ PC (Webcam USB)")
        pc_layout = QVBoxLayout()
        pc_info = QLabel(
            "• Supporto webcam USB standard\n"
            "• OpenCV nativo (cv2.VideoCapture)\n"
            "• Ideale per sviluppo e testing\n"
            "• Windows, macOS, Linux"
        )
        pc_info.setStyleSheet("color: #666; font-size: 11px;")
        pc_layout.addWidget(pc_info)
        pc_btn = QPushButton("Seleziona PC")
        pc_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        pc_btn.clicked.connect(self.select_pc)
        pc_layout.addWidget(pc_btn)
        pc_group.setLayout(pc_layout)
        layout.addWidget(pc_group)
        
        # Gruppo Jetson Nano
        jetson_group = QGroupBox("🟢 NVIDIA Jetson Nano")
        jetson_layout = QVBoxLayout()
        jetson_info = QLabel(
            "• Pipeline OpenCV/CUDA ottimizzata\n"
            "• Supporto per accelerazione GPU\n"
            "• Ideale per applicazioni IA avanzate\n"
            "• CSI Camera Module"
        )
        jetson_info.setStyleSheet("color: #666; font-size: 11px;")
        jetson_layout.addWidget(jetson_info)
        jetson_btn = QPushButton("Seleziona Jetson Nano")
        jetson_btn.setStyleSheet("""
            QPushButton {
                background-color: #76B900;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5FA800;
            }
        """)
        jetson_btn.clicked.connect(self.select_jetson)
        jetson_layout.addWidget(jetson_btn)
        jetson_group.setLayout(jetson_layout)
        layout.addWidget(jetson_group)
        
        # Gruppo Raspberry Pi
        rpi_group = QGroupBox("🍓 Raspberry Pi (con picamera2)")
        rpi_layout = QVBoxLayout()
        rpi_info = QLabel(
            "• Pipeline picamera2 nativa\n"
            "• Ottimizzato per Raspberry Pi Camera\n"
            "• Supporto completo per Pi OS Bullseye+\n"
            "• CSI/MIPI Camera Module"
        )
        rpi_info.setStyleSheet("color: #666; font-size: 11px;")
        rpi_layout.addWidget(rpi_info)
        rpi_btn = QPushButton("Seleziona Raspberry Pi")
        rpi_btn.setStyleSheet("""
            QPushButton {
                background-color: #C51A4A;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #A01540;
            }
        """)
        rpi_btn.clicked.connect(self.select_raspberry_pi)
        rpi_layout.addWidget(rpi_btn)
        rpi_group.setLayout(rpi_layout)
        layout.addWidget(rpi_group)
        
        # Note
        notes = QLabel(
            "Puoi cambiare il dispositivo in qualsiasi momento\n"
            "dalle impostazioni dell'applicazione."
        )
        notes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notes.setStyleSheet("color: #999; font-size: 10px; margin-top: 10px;")
        layout.addWidget(notes)
        
        layout.addStretch()
        
    def select_pc(self):
        """Seleziona PC"""
        self.selected_device = DeviceType.PC
        self.accept()
        
    def select_jetson(self):
        """Seleziona Jetson Nano"""
        self.selected_device = DeviceType.JETSON_NANO
        self.accept()
        
    def select_raspberry_pi(self):
        """Seleziona Raspberry Pi"""
        self.selected_device = DeviceType.RASPBERRY_PI
        self.accept()