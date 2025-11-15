# CameraThread.py (VERSIONE FINALE E CORRETTA)

import cv2
from PyQt6.QtCore import QThread, pyqtSignal

class CameraThread(QThread):
    frame_ready = pyqtSignal(object)  # Frame RGB per la visualizzazione
    # Segnale che invia il frame BGR GIA' ELABORATO per la registrazione
    processed_frame_ready = pyqtSignal(object)
    status_update = pyqtSignal(str)
    
    def __init__(self, camera_manager, cv_processor):
        super().__init__()
        self.camera_manager = camera_manager
        self.cv_processor = cv_processor
        self.running = False
        self.mode = "Normale"
        self.brightness = 0
        self.contrast = 0
        self.saturation = 0
        self.hue_min = 0
        self.hue_max = 179
        self.sat_min = 0
        self.sat_max = 255
        self.val_min = 0
        self.val_max = 255
        self.mirror = False
        self.performance_scale = 0.5
        self.show_osd = True
        
    def run(self):
        self.running = True
        self.camera_manager.start()
        self.status_update.emit("Camera avviata")
        
        while self.running:
            frame = self.camera_manager.get_frame()
            if frame is not None:
                # 1. Applica i controlli di base (luminosità, etc.)
                frame = self.camera_manager.apply_controls(
                    frame, self.brightness, self.contrast, self.saturation
                )
                
                # 2. PROCESSA IL FRAME: questo è il passaggio chiave.
                # Il CVProcessor applica TUTTO: effetti, YOLO, OSD, specchiatura.
                # Restituisce un frame BGR finale e completo.
                processed_frame = self.cv_processor.process_frame(
                    frame, self.mode, 
                    performance_scale=self.performance_scale,
                    show_osd=self.show_osd,
                    resolution=self.camera_manager.get_resolution(),
                    fps=self.camera_manager.get_fps(),
                    hue_min=self.hue_min, hue_max=self.hue_max,
                    sat_min=self.sat_min, sat_max=self.sat_max,
                    val_min=self.val_min, val_max=self.val_max,
                    mirror=self.mirror  # Passa lo stato della specchiatura
                )
                
                # 3. EMETTE IL FRAME ELABORATO (BGR) PER LA REGISTRAZIONE
                # Questo è il frame che verrà salvato nel video.
                self.processed_frame_ready.emit(processed_frame)
                
                # 4. Converte il frame elaborato in RGB per la visualizzazione a schermo
                rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                
                # 5. EMETTE IL FRAME RGB PER LA VISUALIZZAZIONE
                self.frame_ready.emit(rgb_frame)
                
    def stop(self):
        self.running = False
        self.camera_manager.stop()
        self.wait()
        
    def set_mode(self, mode):
        self.mode = mode
        
    def set_brightness(self, value):
        self.brightness = value
        
    def set_contrast(self, value):
        self.contrast = value
        
    def set_saturation(self, value):
        self.saturation = value
        
    def set_hsv_values(self, hue_min, hue_max, sat_min, sat_max, val_min, val_max):
        self.hue_min = hue_min
        self.hue_max = hue_max
        self.sat_min = sat_min
        self.sat_max = sat_max
        self.val_min = val_min
        self.val_max = val_max
        
    def set_mirror(self, mirror):
        self.mirror = mirror

    def set_show_osd(self, show_osd):
        self.show_osd = show_osd