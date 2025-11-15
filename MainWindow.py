# MainWindow.py

import os
import sys
import cv2
from datetime import datetime
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                            QMessageBox, QFileDialog, QStatusBar)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
# Import per la gestione multimediale
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # --- VARIABILE DI STATO PER LA REGISTRAZIONE ---
        self.is_recording = False
        
        # Inizializza i componenti
        self.camera_manager = CameraManager()
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
        
        # --- Inizializza il media player per la musica di sottofondo ---
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        # --- CORREZIONE APPLICATA QUI ---
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite) # Imposta la riproduzione infinita
        
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

    def setup_shortcuts(self):
        """Configura le scorciatoie da tastiera globali usando QShortcut."""
        # Scorciatoia C: Scatta Foto
        shortcut_c = QShortcut(QKeySequence('C'), self)
        shortcut_c.activated.connect(self.capture_photo)
        
        # Scorciatoia M: Specchia Immagine
        shortcut_m = QShortcut(QKeySequence('M'), self)
        shortcut_m.activated.connect(self.toggle_mirror_shortcut)
        
        # Scorciatoia V: Avvia/Ferma Registrazione
        shortcut_v = QShortcut(QKeySequence('V'), self)
        shortcut_v.activated.connect(self.on_record_clicked)
        
        # Scorciatoia T: Avvia Timer
        shortcut_t = QShortcut(QKeySequence('T'), self)
        shortcut_t.activated.connect(self.start_timer)
        
        # Scorciatoia ESC: Gestisce uscita da schermo intero e chiusura app
        shortcut_esc = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        shortcut_esc.activated.connect(self.handle_escape)

    def handle_escape(self):
        """Gestisce la logica per il tasto ESC."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.close()
        
    def init_ui(self):
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
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
        # --- Collega il segnale della checkbox della musica ---
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
        
        # Crea la barra di stato
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")
        
        # Widget per l'anteprima
        self.preview_widget = PreviewWidget(self)
        
        # Widget per le notifiche On-Screen
        self.osd_notification = OSDNotification(self)
        
    def apply_style(self):
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
        try:
            self.camera_thread = CameraThread(self.camera_manager, self.cv_processor)

            self.camera_thread.frame_ready.connect(self.update_frame)
            self.camera_thread.status_update.connect(self.update_status)
            self.camera_thread.start()
            
            resolution = self.camera_manager.get_resolution()
            fps = self.camera_manager.get_fps()
            self.status_bar.showMessage(f"Risoluzione: {resolution[0]}x{resolution[1]} | FPS: {fps} | Modalità: Normale")
        except Exception as e:
            QMessageBox.critical(self, "Errore della Fotocamera", 
                                f"Impossibile inizializzare la fotocamera: {str(e)}")
            self.camera_view.setText("Errore: Fotocamera non disponibile")

    def update_frame(self, rgb_frame):
        self.camera_view.update_frame(rgb_frame)
        
    def update_status(self, message):
        mode = self.control_panel.mode_combo.currentText()
        resolution = self.camera_manager.get_resolution()
        fps = self.camera_manager.get_fps()
        
        if "Camera" in message:
            self.status_bar.showMessage(f"Risoluzione: {resolution[0]}x{resolution[1]} | FPS: {fps} | Modalità: {mode}")
        else:
            self.status_bar.showMessage(f"{message} | Risoluzione: {resolution[0]}x{resolution[1]} | FPS: {fps} | Modalità: {mode}")
            
    def capture_photo(self):
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
                self.status_bar.showMessage(f"Errore nel salvare l'immagine")

    def on_record_clicked(self):
        # Usiamo la nostra variabile di stato self.is_recording
        if not self.is_recording:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.mp4"
            path = os.path.expanduser(f"~/VisionPy_Pro/videos/{filename}")
            
            # Crea e avvia il thread di registrazione
            self.recording_thread = RecordingThread(self.camera_manager)
            self.recording_thread.recording_finished.connect(self.on_recording_finished)
            self.recording_thread.status_update.connect(self.update_status)
            
            width, height = self.camera_manager.get_resolution()
            fps = self.camera_manager.get_fps()
            self.recording_thread.start_recording(path, width, height, fps)
            
            # --- FONDAMENTALE: Aggiorna lo stato e collega i segnali ---
            self.is_recording = True
            self.camera_manager.is_recording = True # Manteniamo sincronizzato anche il manager
            self.camera_thread.processed_frame_ready.connect(self.recording_thread.add_frame_to_queue)
            
            self.control_panel.update_record_button(True)
            self.osd_notification.show_notification("Registrazione Iniziata!")
        else:
            # Ferma la registrazione
            if self.recording_thread and self.recording_thread.isRunning():
                self.camera_thread.processed_frame_ready.disconnect(self.recording_thread.add_frame_to_queue)
                self.recording_thread.stop_recording()
            else:
                # Questo blocco ora è quasi ridondante, ma lo teniamo per sicurezza
                self.on_recording_finished(True)
                
    def on_recording_finished(self, success):
        # --- FONDAMENTALE: Resetta lo stato quando la registrazione finisce ---
        self.is_recording = False
        self.camera_manager.is_recording = False

        self.control_panel.update_record_button(False)
        if success:
            self.status_bar.showMessage("Registrazione fermata e salvata.")
            self.osd_notification.show_notification("Registrazione Fermata!")
        else:
            self.status_bar.showMessage("Errore durante la registrazione.")
            self.osd_notification.show_notification("Errore Registrazione!")
            
    def on_mode_changed(self, mode):
        if self.camera_thread:
            self.camera_thread.set_mode(mode)
            
        resolution = self.camera_manager.get_resolution()
        fps = self.camera_manager.get_fps()
        self.status_bar.showMessage(f"Risoluzione: {resolution[0]}x{resolution[1]} | FPS: {fps} | Modalità: {mode}")
        
    def on_brightness_changed(self, value):
        if self.camera_thread:
            self.camera_thread.set_brightness(value)
            
    def on_contrast_changed(self, value):
        if self.camera_thread:
            self.camera_thread.set_contrast(value)
            
    def on_saturation_changed(self, value):
        if self.camera_thread:
            self.camera_thread.set_saturation(value)
            
    def on_hsv_changed(self, hue_min, hue_max, sat_min, sat_max, val_min, val_max):
        if self.camera_thread:
            self.camera_thread.set_hsv_values(hue_min, hue_max, sat_min, sat_max, val_min, val_max)
            
    def on_mirror_changed(self, is_checked):
        if self.camera_thread:
            self.camera_thread.set_mirror(is_checked)

    def on_osd_changed(self, is_checked):
        if self.camera_thread:
            self.camera_thread.set_show_osd(is_checked)

    # --- Metodo per gestire la musica di sottofondo ---
    def on_music_changed(self, is_checked):
        music_path = "/home/scuola/VisionPy_Pro/assets/background.mp3"
        if is_checked:
            try:
                if os.path.exists(music_path):
                    self.media_player.setSource(QUrl.fromLocalFile(music_path))
                    self.media_player.play()
                    self.status_bar.showMessage("Musica di sottofondo avviata")
                    self.osd_notification.show_notification("Musica Avviata!")
                else:
                    self.status_bar.showMessage(f"File musicale non trovato: {music_path}")
                    self.osd_notification.show_notification("File Musicale Non Trovato!")
                    # Resetta lo stato del checkbox per coerenza
                    self.control_panel.music_checkbox.setChecked(False)
            except Exception as e:
                self.status_bar.showMessage(f"Errore nell'avviare la musica: {str(e)}")
                self.osd_notification.show_notification("Errore Musica!")
                self.control_panel.music_checkbox.setChecked(False)
        else:
            try:
                self.media_player.stop()
                self.status_bar.showMessage("Musica di sottofondo fermata")
                self.osd_notification.show_notification("Musica Fermata!")
            except Exception as e:
                self.status_bar.showMessage(f"Errore nel fermare la musica: {str(e)}")

    def on_timer_action_changed(self, action):
        self.timer_manager.set_timer_action(action)

    def on_timer_delay_changed(self, value):
        self.timer_manager.set_timer_delay(value)

    def start_timer(self):
        # Disabilita i pulsanti per evitare conflitti
        self.control_panel.set_timer_buttons_enabled(False)
        
        # Mostra il messaggio iniziale nella barra di stato
        self.status_bar.showMessage(f"Timer avviato. {self.timer_manager.timer_action} in {self.timer_manager.timer_delay_seconds} secondi...")
        self.osd_notification.show_notification("Timer Avviato!")
        
        # Avvia il timer del countdown
        self.timer_manager.start_timer()

    def update_countdown(self, remaining):
        if remaining > 0:
            # Aggiorna la barra di stato con il tempo rimanente
            self.status_bar.showMessage(f"{self.timer_manager.timer_action} in {remaining} secondi...")
            
    def on_timer_finished(self):
        # Esegui l'azione scelta
        if self.timer_manager.timer_action == "Scatta Foto":
            self.capture_photo()
        elif self.timer_manager.timer_action == "Registra Video":
            self.on_record_clicked()
        
        # Riabilita i pulsanti
        self.control_panel.set_timer_buttons_enabled(True)
        
        self.status_bar.showMessage("Azione eseguita.")
        self.osd_notification.show_notification("Azione Eseguita!")

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def toggle_mirror_shortcut(self):
        self.control_panel.mirror_checkbox.setChecked(not self.control_panel.mirror_checkbox.isChecked())
            
    def save_as(self):
        frame = self.camera_manager.capture_frame()
        if frame is not None:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Salva Immagine", "", 
                "Immagini (*.jpg *.jpeg *.png);;Tutti i file (*)"
            )
            
            if filename:
                success = self.camera_manager.save_frame(frame, filename)
                
                if success:
                    self.status_bar.showMessage(f"Immagine salvata: {filename}")
                else:
                    self.status_bar.showMessage(f"Errore nel salvare l'immagine")

    def show_gallery(self):
        photo_path = os.path.expanduser("~/VisionPy_Pro/photos")
        video_path = os.path.expanduser("~/VisionPy_Pro/videos")
        dialog = GalleryDialog(photo_path, video_path, self)
        dialog.exec()
            
    def show_about(self):
        QMessageBox.about(self, "Informazioni su VisionPy Pro", 
                         "VisionPy Pro v1.0\n\n"
                         "Un'applicazione avanzata di computer vision per Raspberry Pi.\n\n"
                         "Sviluppato con PyQt6, picamera2 e OpenCV")
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Se la notifica è visibile, riposizionala quando la finestra viene ridimensionata
        if self.osd_notification.isVisible():
            self.osd_notification.position_notification()
        
    def closeEvent(self, event):
        self.status_bar.showMessage("Chiusura in corso...")

        # --- MODIFICA: Usa la nostra variabile di stato ---
        if self.is_recording and self.recording_thread and self.recording_thread.isRunning():
            self.camera_thread.processed_frame_ready.disconnect(self.recording_thread.add_frame_to_queue)
            self.recording_thread.stop_recording()
            if not self.recording_thread.wait(3000):
                self.status_bar.showMessage("Attenzione: il thread di registrazione non ha chiuso in tempo.")

        if self.camera_thread and self.camera_thread.isRunning():
            self.camera_thread.stop()
            if not self.camera_thread.wait(5000):
                self.status_bar.showMessage("Attenzione: il thread della fotocamera non ha chiuso in tempo. Uscita forzata.")

        # Ferma il timer del countdown se è attivo
        self.timer_manager.stop_timer()

        # --- Ferma la musica di sottofondo all'uscita ---
        self.media_player.stop()

        event.accept()