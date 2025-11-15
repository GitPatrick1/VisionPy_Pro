# ControlPanel.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QComboBox, QSlider, 
                            QGroupBox, QGridLayout, QCheckBox, QSpinBox, 
                            QRadioButton, QButtonGroup)
from PyQt6.QtCore import pyqtSignal, Qt
# ... altri import
# Ora l’uso di QSlider(Qt.Orientation.Horizontal) funziona



class ControlPanel(QWidget):
    mode_changed = pyqtSignal(str)
    brightness_changed = pyqtSignal(int)
    contrast_changed = pyqtSignal(int)
    saturation_changed = pyqtSignal(int)
    hsv_changed = pyqtSignal(int, int, int, int, int, int)
    mirror_changed = pyqtSignal(bool)
    osd_changed = pyqtSignal(bool)
    music_changed = pyqtSignal(bool) # SEGNALE PER LA MUSICA
    capture_photo = pyqtSignal()
    record_clicked = pyqtSignal()
    gallery_clicked = pyqtSignal()
    timer_start = pyqtSignal()
    timer_action_changed = pyqtSignal(str)
    timer_delay_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Gruppo Modalità
        mode_group = QGroupBox("Modalità")
        mode_layout = QVBoxLayout()
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Normale", 
            "Rilevamento Volti", 
            "Rilevamento Contorni",
            "Segmentazione per Colore",
            "Rilevamento Movimento",
            "Sfocatura Sfondo",
            "Rilevamento Oggetti (YOLO)"
        ])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # Gruppo Controlli Foto
        photo_group = QGroupBox("Controlli Foto")
        photo_layout = QGridLayout()
        
        self.capture_btn = QPushButton("SCATTA FOTO")
        self.capture_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9500;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 25px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #FF7700;
            }
        """)
        self.capture_btn.clicked.connect(lambda: self.capture_photo.emit())
        photo_layout.addWidget(self.capture_btn, 0, 0, 1, 2)

        self.record_btn = QPushButton("REGISTRA VIDEO")
        self.record_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 25px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #D70015;
            }
        """)
        self.record_btn.clicked.connect(lambda: self.record_clicked.emit())
        photo_layout.addWidget(self.record_btn, 1, 0, 1, 2)
        
        photo_layout.addWidget(QLabel("Luminosità:"), 2, 0)
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        photo_layout.addWidget(self.brightness_slider, 2, 1)
        
        photo_layout.addWidget(QLabel("Contrasto:"), 3, 0)
        self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        self.contrast_slider.setRange(-100, 100)
        self.contrast_slider.setValue(0)
        self.contrast_slider.valueChanged.connect(self.on_contrast_changed)
        photo_layout.addWidget(self.contrast_slider, 3, 1)
        
        photo_layout.addWidget(QLabel("Saturazione:"), 4, 0)
        self.saturation_slider = QSlider(Qt.Orientation.Horizontal)
        self.saturation_slider.setRange(-100, 100)
        self.saturation_slider.setValue(0)
        self.saturation_slider.valueChanged.connect(self.on_saturation_changed)
        photo_layout.addWidget(self.saturation_slider, 4, 1)
        
        photo_group.setLayout(photo_layout)
        layout.addWidget(photo_group)
        
        # Gruppo Timer / Scatto Programmato
        timer_group = QGroupBox("Timer / Scatto Programmato")
        timer_layout = QVBoxLayout()

        action_layout = QHBoxLayout()
        self.timer_radio_photo = QRadioButton("Scatta Foto")
        self.timer_radio_photo.setChecked(True)
        self.timer_radio_video = QRadioButton("Registra Video")
        self.timer_button_group = QButtonGroup()
        self.timer_button_group.addButton(self.timer_radio_photo)
        self.timer_button_group.addButton(self.timer_radio_video)
        self.timer_radio_photo.toggled.connect(lambda: self.on_timer_action_changed())
        self.timer_radio_video.toggled.connect(lambda: self.on_timer_action_changed())
        action_layout.addWidget(self.timer_radio_photo)
        action_layout.addWidget(self.timer_radio_video)
        timer_layout.addLayout(action_layout)
        
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Ritardo (s):"))
        self.timer_delay_spinbox = QSpinBox()
        self.timer_delay_spinbox.setRange(1, 60)
        self.timer_delay_spinbox.setValue(5)
        self.timer_delay_spinbox.setSuffix(" s")
        self.timer_delay_spinbox.valueChanged.connect(self.on_timer_delay_changed)
        delay_layout.addWidget(self.timer_delay_spinbox)
        timer_layout.addLayout(delay_layout)

        self.timer_start_btn = QPushButton("AVVIA TIMER")
        self.timer_start_btn.setStyleSheet("""
            QPushButton {
                background-color: #5856D6;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #48484A;
            }
            QPushButton:disabled {
                background-color: #3A3A3A;
                color: #AAAAAA;
            }
        """)
        self.timer_start_btn.clicked.connect(lambda: self.timer_start.emit())
        timer_layout.addWidget(self.timer_start_btn)
        
        timer_group.setLayout(timer_layout)
        layout.addWidget(timer_group)
        
        # Gruppo Galleria
        gallery_group = QGroupBox("Galleria")
        gallery_layout = QVBoxLayout()
        
        self.gallery_btn = QPushButton("APRI GALLERIA")
        self.gallery_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
        """)
        self.gallery_btn.clicked.connect(lambda: self.gallery_clicked.emit())
        gallery_layout.addWidget(self.gallery_btn)
        
        gallery_group.setLayout(gallery_layout)
        layout.addWidget(gallery_group)
        
        # Gruppo Effetti Video
        effects_group = QGroupBox("Effetti Video")
        effects_layout = QVBoxLayout()
        
        self.mirror_checkbox = QCheckBox("Specchia Immagine")
        self.mirror_checkbox.stateChanged.connect(self.on_mirror_changed)
        effects_layout.addWidget(self.mirror_checkbox)
        
        effects_group.setLayout(effects_layout)
        layout.addWidget(effects_group)

        # Gruppo OSD e Audio
        osd_group = QGroupBox("OSD e Audio")
        osd_layout = QVBoxLayout()

        self.osd_checkbox = QCheckBox("Mostra informazioni su schermo")
        self.osd_checkbox.setChecked(True)
        self.osd_checkbox.stateChanged.connect(self.on_osd_changed)
        osd_layout.addWidget(self.osd_checkbox)

        self.music_checkbox = QCheckBox("Musica di Sottofondo")
        self.music_checkbox.setChecked(False)
        self.music_checkbox.stateChanged.connect(self.on_music_changed)
        osd_layout.addWidget(self.music_checkbox)

        osd_group.setLayout(osd_layout)
        layout.addWidget(osd_group)

        # Gruppo Controlli CV
        cv_group = QGroupBox("Controlli CV")
        cv_layout = QGridLayout()
        
        cv_layout.addWidget(QLabel("Hue Min:"), 0, 0)
        self.hue_min_slider = QSlider(Qt.Orientation.Horizontal)
        self.hue_min_slider.setRange(0, 179)
        self.hue_min_slider.setValue(0)
        self.hue_min_slider.valueChanged.connect(self.on_hsv_changed)
        self.hue_min_slider.hide()
        cv_layout.addWidget(self.hue_min_slider, 0, 1)
        
        cv_layout.addWidget(QLabel("Hue Max:"), 1, 0)
        self.hue_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.hue_max_slider.setRange(0, 179)
        self.hue_max_slider.setValue(179)
        self.hue_max_slider.valueChanged.connect(self.on_hsv_changed)
        self.hue_max_slider.hide()
        cv_layout.addWidget(self.hue_max_slider, 1, 1)
        
        cv_layout.addWidget(QLabel("Sat Min:"), 2, 0)
        self.sat_min_slider = QSlider(Qt.Orientation.Horizontal)
        self.sat_min_slider.setRange(0, 255)
        self.sat_min_slider.setValue(0)
        self.sat_min_slider.valueChanged.connect(self.on_hsv_changed)
        self.sat_min_slider.hide()
        cv_layout.addWidget(self.sat_min_slider, 2, 1)
        
        cv_layout.addWidget(QLabel("Sat Max:"), 3, 0)
        self.sat_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.sat_max_slider.setRange(0, 255)
        self.sat_max_slider.setValue(255)
        self.sat_max_slider.valueChanged.connect(self.on_hsv_changed)
        self.sat_max_slider.hide()
        cv_layout.addWidget(self.sat_max_slider, 3, 1)
        
        cv_layout.addWidget(QLabel("Val Min:"), 4, 0)
        self.val_min_slider = QSlider(Qt.Orientation.Horizontal)
        self.val_min_slider.setRange(0, 255)
        self.val_min_slider.setValue(0)
        self.val_min_slider.valueChanged.connect(self.on_hsv_changed)
        self.val_min_slider.hide()
        cv_layout.addWidget(self.val_min_slider, 4, 1)
        
        cv_layout.addWidget(QLabel("Val Max:"), 5, 0)
        self.val_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.val_max_slider.setRange(0, 255)
        self.val_max_slider.setValue(255)
        self.val_max_slider.valueChanged.connect(self.on_hsv_changed)
        self.val_max_slider.hide()
        cv_layout.addWidget(self.val_max_slider, 5, 1)
        
        cv_group.setLayout(cv_layout)
        layout.addWidget(cv_group)
        
        layout.addStretch()
        
    def on_mode_changed(self, mode):
        self.mode_changed.emit(mode)
        
        show_hsv = (mode == "Segmentazione per Colore")
        self.hue_min_slider.setVisible(show_hsv)
        self.hue_max_slider.setVisible(show_hsv)
        self.sat_min_slider.setVisible(show_hsv)
        self.sat_max_slider.setVisible(show_hsv)
        self.val_min_slider.setVisible(show_hsv)
        self.val_max_slider.setVisible(show_hsv)
        
    def on_brightness_changed(self, value):
        self.brightness_changed.emit(value)
        
    def on_contrast_changed(self, value):
        self.contrast_changed.emit(value)
        
    def on_saturation_changed(self, value):
        self.saturation_changed.emit(value)
        
    def on_hsv_changed(self):
        self.hsv_changed.emit(
            self.hue_min_slider.value(),
            self.hue_max_slider.value(),
            self.sat_min_slider.value(),
            self.sat_max_slider.value(),
            self.val_min_slider.value(),
            self.val_max_slider.value()
        )
        
    def on_mirror_changed(self, state):
        is_checked = (state == 2)
        self.mirror_changed.emit(is_checked)

    def on_osd_changed(self, state):
        is_checked = (state == 2)
        self.osd_changed.emit(is_checked)
        
    def on_music_changed(self, state):
        is_checked = (state == 2)
        self.music_changed.emit(is_checked)
        
    def on_timer_action_changed(self):
        if self.timer_radio_photo.isChecked():
            self.timer_action_changed.emit("Scatta Foto")
        elif self.timer_radio_video.isChecked():
            self.timer_action_changed.emit("Registra Video")

    def on_timer_delay_changed(self, value):
        self.timer_delay_changed.emit(value)
        
    def update_record_button(self, is_recording):
        if is_recording:
            self.record_btn.setText("FERMA REGISTRAZIONE")
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background-color: #34C759;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    border: 2px solid white;
                    border-radius: 25px;
                    padding: 10px;
                }
            """)
        else:
            self.record_btn.setText("REGISTRA VIDEO")
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF3B30;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    border-radius: 25px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #D70015;
                }
            """)
            
    def set_timer_buttons_enabled(self, enabled):
        self.timer_start_btn.setEnabled(enabled)
        self.capture_btn.setEnabled(enabled)
        self.record_btn.setEnabled(enabled)