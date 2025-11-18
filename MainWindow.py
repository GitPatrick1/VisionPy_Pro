import os
import sys
import cv2
from datetime import datetime
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QMessageBox, QFileDialog, QStatusBar, QMenu, QDialog)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from CameraManager import CameraManager
from CVProcessor import CVProcessor
from GalleryDialog import GalleryDialog
from CameraThread import CameraThread
from RecordingThread import RecordingThread
from CameraWidget import CameraWidget
from ControlPanel import ControlPanel
from OSDNotification import OSDNotification
from PreviewWidget import PreviewWidget
from MenuBar import MenuBar
from TimerManager import TimerManager
from SettingsManager import SettingsManager
from DeviceManager import DeviceSelectionDialog, DeviceType

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # === INIZIALIZZA IL GESTORE DELLE IMPOSTAZIONI ===
        self.settings_manager = SettingsManager()
        
        # === LEGGI IL DISPOSITIVO DALLE IMPOSTAZIONI ===
        device_type_str = self.settings_manager.get_device_type()
        
        if device_type_str == "jetson_nano":
            device_type = DeviceType.JETSON_NANO
        elif device_type_str == "raspberry_pi":
            device_type = DeviceType.RASPBERRY_PI
        else:
            device_type = DeviceType.PC
        
        settings_path = os.path.expanduser("~/VisionPy_Pro/settings.json")
        
        # === MOSTRA DIALOGO SOLO AL PRIMO AVVIO ===
        show_dialog = not os.path.exists(settings_path)
        
        if show_dialog:
            device_dialog = DeviceSelectionDialog(self)
            if device_dialog.exec() == QDialog.DialogCode.Accepted:
                device_type = device_dialog.selected_device
                self.settings_manager.set_device_type(device_type.value)
            else:
                sys.exit(0)
        
        # === VARIABILE DI STATO PER LA REGISTRAZIONE ===
        self.is_recording = False
        
        # Inizializza i componenti con il dispositivo selezionato
        self.camera_manager = CameraManager(device_type)
        self.cv_processor = CVProcessor()
        self.camera_thread = None
        self.recording_thread = None
        
        # Inizializza il gestore del timer
        self.timer_manager = TimerManager(self)
        self.timer_manager.countdown_update.connect(self.update_countdown)
        self.timer_manager.countdown_finished.connect(self.on_timer_finished)
        
        # Impostazioni fisse e ottimizzate
        self.camera_manager.set_resolution((1280, 720))
        self.camera_manager.set_fps(30)
        
        # === Inizializza il media player per la musica di sottofondo ===
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite)
        
        # Configura la finestra principale
        self.setWindowTitle("VisionPy Pro")
        self.setGeometry(100, 100, 1200, 800)
        
        # Applica lo stile
        self.apply_style()
        
        # Crea l'interfaccia utente
        self.init_ui()
        
        # Imposta le scorciatoie globali
        self.setup_shortcuts()
        
        # Inizializza la fotocamera
        self.init_camera()
        
        # Visualizza il dispositivo attuale nella barra di stato
        device_name = "Jetson Nano" if device_type == DeviceType.JETSON_NANO else "Raspberry Pi" if device_type == DeviceType.RASPBERRY_PI else "PC"
        print(f"✓ VisionPy Pro avviato con {device_name}")

    def setup_shortcuts(self):
        """Configura le scorciatoie da tastiera globali"""
        shortcut_c = QShortcut(QKeySequence('C'), self)
        shortcut_c.activated.connect(self.capture_photo)
        
        shortcut_m = QShortcut(QKeySequence('M'), self)
        shortcut_m.activated.connect(self.toggle_mirror_shortcut)
        
        shortcut_v = QShortcut(QKeySequence('V'), self)
        shortcut_v.activated.connect(self.on_record_clicked)
        
        shortcut_t = QShortcut(QKeySequence('T'), self)
        shortcut_t.activated.connect(self.start_timer)
        
        shortcut_esc = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        shortcut_esc.activated.connect(self.handle_escape)

    def handle_escape(self):
        """Gestisce la logica per il tasto ESC"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.close()

    def init_ui(self):
        """Inizializza l'interfaccia utente"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Area di visualizzazione della fotocamera (80%)
        self.camera_view = CameraWidget(self)
        main_layout.addWidget(self.camera_view, 3)
        
        # Pannello di controllo laterale (20%)
        self.control_panel = ControlPanel(self)
        self.control_panel.mode_changed.connect(self.on_mode_changed)
        self.control_panel.brightness_changed.connect(self.on_brightness_changed)
        self.control_panel.contrast_changed.connect(self.on_contrast_changed)
        self.control_panel.saturation_changed.connect(self.on_saturation_changed)
        self.control_panel.hsv_changed.connect(self.on_hsv_changed)
        self.control_panel.mirror_changed.connect(self.on_mirror_changed)
        self.control_panel.osd_changed.connect(self.on_osd_changed)
        self.control_panel.music_changed.connect(self.on_music_changed)
        self.control_panel.capture_photo.connect(self.capture_photo)
        self.control_panel.record_clicked.connect(self.on_record_clicked)
        self.control_panel.gallery_clicked.connect(self.show_gallery)
        self.control_panel.timer_start.connect(self.start_timer)
        self.control_panel.timer_action_changed.connect(self.on_timer_action_changed)
        self.control_panel.timer_delay_changed.connect(self.on_timer_delay_changed)
        main_layout.addWidget(self.control_panel, 1)
        
        # Crea la barra dei menu
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # Aggiungi un menu per il cambio dispositivo
        self.add_device_menu()
        
        # Crea la barra di stato
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")
        
        # Widget per l'anteprima
        self.preview_widget = PreviewWidget(self)
        
        # Widget per le notifiche On-Screen
        self.osd_notification = OSDNotification(self)

    def add_device_menu(self):
        """Aggiunge il menu per il cambio dispositivo"""
        device_menu = self.menu_bar.addMenu("Dispositivo")
        
        pc_action = device_menu.addAction("Usa PC")
        pc_action.triggered.connect(lambda: self.switch_device(DeviceType.PC))
        
        jetson_action = device_menu.addAction("Usa Jetson Nano")
        jetson_action.triggered.connect(lambda: self.switch_device(DeviceType.JETSON_NANO))
        
        rpi_action = device_menu.addAction("Usa Raspberry Pi")
        rpi_action.triggered.connect(lambda: self.switch_device(DeviceType.RASPBERRY_PI))

    def switch_device(self, device_type):
        """Cambia il dispositivo della fotocamera"""
        if self.camera_manager.get_device_type() == device_type:
            QMessageBox.information(self, "Dispositivo",
                "Il dispositivo è già configurato per questo tipo.")
            return
        
        reply = QMessageBox.question(self, "Cambio Dispositivo",
            "Questa operazione riavvierà la fotocamera. Continuare?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Ferma la fotocamera attuale
                if self.camera_thread:
                    self.camera_thread.stop()
                    self.camera_thread.wait()
                
                # Cambia il dispositivo
                self.camera_manager.set_device_type(device_type)
                self.settings_manager.set_device_type(device_type.value)
                
                # Riavvia la fotocamera
                self.init_camera()
                
                device_name = "PC" if device_type == DeviceType.PC else "Jetson Nano" if device_type == DeviceType.JETSON_NANO else "Raspberry Pi"
                QMessageBox.information(self, "Dispositivo",
                    f"Dispositivo cambiato in {device_name}")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore nel cambio dispositivo: {str(e)}")

    def apply_style(self):
        """Applica lo stile all'applicazione"""
        style = """
        QMainWindow {
            background-color: #2D2D30;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #555;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QComboBox {
            background-color: #3C3C3C;
            color: white;
            border: 1px solid #555;
            border-radius: 3px;
            padding: 5px;
        }
        
        QSlider::groove:horizontal {
            height: 6px;
            background: #3C3C3C;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            background: #007ACC;
            border: 1px solid #5C5C5C;
            width: 14px;
            margin: -4px 0;
            border-radius: 7px;
        }
        
        QLabel {
            color: white;
        }
        
        QCheckBox {
            color: white;
        }
        
        QRadioButton {
            color: white;
        }
        
        QMenuBar {
            background-color: #2D2D30;
            color: white;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 5px 10px;
        }
        
        QMenuBar::item:selected {
            background-color: #3C3C3C;
        }
        
        QMenu {
            background-color: #2D2D30;
            color: white;
            border: 1px solid #555;
        }
        
        QMenu::item:selected {
            background-color: #3C3C3C;
        }
        
        QStatusBar {
            background-color: #007ACC;
            color: white;
        }
        """
        self.setStyleSheet(style)

    def init_camera(self):
        """Inizializza la fotocamera"""
        try:
            self.camera_thread = CameraThread(self.camera_manager, self.cv_processor)
            self.camera_thread.frame_ready.connect(self.update_frame)
            self.camera_thread.status_update.connect(self.update_status)
            self.camera_thread.start()
            
            resolution = self.camera_manager.get_resolution()
            fps = self.camera_manager.get_fps()
            device_type = self.camera_manager.get_device_type()
            device_name = "PC" if device_type == DeviceType.PC else "Jetson Nano" if device_type == DeviceType.JETSON_NANO else "Raspberry Pi"
            
            self.status_bar.showMessage(f"Dispositivo: {device_name} | Risoluzione: {resolution[0]}x{resolution[1]} | FPS: {fps} | Modalità: Normale")
        except Exception as e:
            QMessageBox.critical(self, "Errore della Fotocamera",
                f"Impossibile inizializzare la fotocamera: {str(e)}")
            self.camera_view.setText("Errore: Fotocamera non disponibile")

    def update_frame(self, rgb_frame):
        """Aggiorna il frame visualizzato"""
        self.camera_view.update_frame(rgb_frame)

    def update_status(self, message):
        """Aggiorna la barra di stato"""
        mode = self.control_panel.mode_combo.currentText()
        resolution = self.camera_manager.get_resolution()
        fps = self.camera_manager.get_fps()
        device_type = self.camera_manager.get_device_type()
        device_name = "PC" if device_type == DeviceType.PC else "Jetson Nano" if device_type == DeviceType.JETSON_NANO else "Raspberry Pi"
        
        if "Camera" in message:
            self.status_bar.showMessage(f"Dispositivo: {device_name} | Risoluzione: {resolution[0]}x{resolution[1]} | FPS: {fps} | Modalità: {mode}")
        else:
            self.status_bar.showMessage(f"{message} | Dispositivo: {device_name} | Risoluzione: {resolution[0]}x{resolution[1]} | FPS: {fps} | Modalità: {mode}")

    def capture_photo(self):
        """Cattura una foto"""
        frame = self.camera_manager.capture_frame()
        if frame is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.jpg"
            path = os.path.expanduser(f"~/VisionPy_Pro/photos/{filename}")
            
            success = self.camera_manager.save_frame(frame, path)
            if success:
                self.status_bar.showMessage(f"Immagine salvata: {filename}")
                self.preview_widget.show_preview(frame)
                self.osd_notification.show_notification("Foto Scattata!")
            else:
                self.status_bar.showMessage("Errore nel salvare l'immagine")

    def on_record_clicked(self):
        """Gestisce l'avvio/arresto della registrazione"""
        if not self.is_recording:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.mp4"
            path = os.path.expanduser(f"~/VisionPy_Pro/videos/{filename}")
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            resolution = self.camera_manager.get_resolution()
            fps = self.camera_manager.get_fps()
            
            self.recording_thread = RecordingThread(self.camera_manager)
            self.recording_thread.recording_finished.connect(self.on_recording_finished)
            self.recording_thread.status_update.connect(self.update_status)
            
            self.camera_thread.processed_frame_ready.connect(
                self.recording_thread.add_frame_to_queue
            )
            
            self.recording_thread.start_recording(path, resolution[0], resolution[1], fps)
            self.is_recording = True
            
            self.control_panel.record_btn.setStyleSheet("""
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
            self.control_panel.record_btn.setText("FERMA REGISTRAZIONE")
            self.osd_notification.show_notification("Registrazione Avviata!")
            self.status_bar.showMessage(f"Registrazione in corso: {filename}")
        else:
            if self.recording_thread:
                self.recording_thread.stop_recording()
            self.is_recording = False
            
            self.control_panel.record_btn.setStyleSheet("""
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
            self.control_panel.record_btn.setText("REGISTRA VIDEO")
            self.osd_notification.show_notification("Registrazione Fermata!")

    def on_recording_finished(self, success):
        """Callback quando la registrazione è terminata"""
        if success:
            self.status_bar.showMessage("Registrazione salvata con successo")
        else:
            self.status_bar.showMessage("Errore durante la registrazione")

    def show_gallery(self):
        """Mostra la galleria"""
        photo_dir = os.path.expanduser("~/VisionPy_Pro/photos")
        video_dir = os.path.expanduser("~/VisionPy_Pro/videos")
        gallery_dialog = GalleryDialog(photo_dir, video_dir, self)
        gallery_dialog.show()

    def on_mode_changed(self, mode):
        """Gestisce il cambio modalità"""
        self.camera_thread.set_mode(mode)

    def on_brightness_changed(self, value):
        """Gestisce il cambio di luminosità"""
        self.camera_thread.set_brightness(value)

    def on_contrast_changed(self, value):
        """Gestisce il cambio di contrasto"""
        self.camera_thread.set_contrast(value)

    def on_saturation_changed(self, value):
        """Gestisce il cambio di saturazione"""
        self.camera_thread.set_saturation(value)

    def on_hsv_changed(self, hue_min, hue_max, sat_min, sat_max, val_min, val_max):
        """Gestisce il cambio dei valori HSV"""
        self.camera_thread.set_hsv_values(hue_min, hue_max, sat_min, sat_max, val_min, val_max)

    def on_mirror_changed(self, mirror):
        """Gestisce il cambio dello specchiamento"""
        self.camera_thread.set_mirror(mirror)

    def on_osd_changed(self, show_osd):
        """Gestisce il cambio della visualizzazione OSD"""
        self.camera_thread.set_show_osd(show_osd)

    def on_music_changed(self, muted):
        """Gestisce il cambio dello stato della musica"""
        if muted:
            self.media_player.play()
        else:
            self.media_player.stop()

    def toggle_mirror_shortcut(self):
        """Attiva/disattiva lo specchiamento via scorciatoia"""
        self.control_panel.mirror_checkbox.setChecked(not self.control_panel.mirror_checkbox.isChecked())

    def start_timer(self):
        """Avvia il timer"""
        action = "Scatta Foto" if self.control_panel.timer_radio_photo.isChecked() else "Registra Video"
        delay = self.control_panel.timer_delay_spinbox.value()
        
        self.timer_manager.start_timer(delay, action)
        self.osd_notification.show_notification(f"Timer: {delay}s")

    def on_timer_action_changed(self):
        """Callback per il cambio dell'azione del timer"""
        action = "Scatta Foto" if self.control_panel.timer_radio_photo.isChecked() else "Registra Video"
        self.timer_manager.set_timer_action(action)

    def on_timer_delay_changed(self, value):
        """Callback per il cambio del ritardo del timer"""
        self.timer_manager.set_timer_delay(value)

    def update_countdown(self, remaining):
        """Aggiorna il countdown del timer"""
        self.osd_notification.show_notification(f"Timer: {remaining}s", duration=800)

    def on_timer_finished(self):
        """Callback quando il timer è terminato"""
        action = self.timer_manager.timer_action
        if action == "Scatta Foto":
            self.capture_photo()
        else:
            self.on_record_clicked()

    def toggle_fullscreen(self):
        """Attiva/disattiva la modalità schermo intero"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def show_about(self):
        """Mostra le informazioni sull'applicazione"""
        QMessageBox.information(self, "Informazioni",
            "VisionPy Pro v1.0\n\n"
            "Applicazione avanzata di acquisizione e elaborazione video\n"
            "Supporta PC, Jetson Nano e Raspberry Pi\n\n"
            "© 2024")

    def closeEvent(self, event):
        """Gestisce la chiusura dell'applicazione"""
        if self.camera_thread:
            self.camera_thread.stop()
        
        if self.recording_thread and self.is_recording:
            self.recording_thread.stop_recording()
        
        if self.media_player.isPlaying():
            self.media_player.stop()
        
        event.accept()
