import os
import cv2
import numpy as np
from PyQt6.QtCore import QObject
from DeviceManager import DeviceType

class CameraManager(QObject):
    """
    Gestisce la cattura video da diversi dispositivi:
    - PC: usa OpenCV con webcam USB
    - Jetson Nano: usa OpenCV con pipeline standard
    - Raspberry Pi: usa picamera2
    """
    
    def __init__(self, device_type=DeviceType.PC):
        super().__init__()
        self.device_type = device_type
        self.picam2 = None
        self.config = None
        self.frame = None
        self.resolution = (1280, 720)
        self.fps = 30
        self.is_recording = False
        self.encoder = None
        self.output = None
        self.cap = None
        self.camera_index = 0  # Per PC e Jetson: indice della webcam
        
    def set_camera_index(self, index):
        """Imposta l'indice della fotocamera per PC/Jetson"""
        self.camera_index = index
        
    def start(self):
        """Inizializza la fotocamera in base al dispositivo selezionato"""
        try:
            if self.device_type == DeviceType.RASPBERRY_PI:
                return self._start_raspberry_pi()
            elif self.device_type == DeviceType.JETSON_NANO:
                return self._start_jetson_nano()
            else:  # PC
                return self._start_pc()
        except Exception as e:
            print(f"Errore nell'avvio della fotocamera: {str(e)}")
            return False
    
    def _start_pc(self):
        """Inizializza la fotocamera per PC (webcam USB)"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                raise Exception("Impossibile aprire la webcam")
            
            # Imposta la risoluzione
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            # Imposta gli FPS
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Imposta buffer size
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            print(f"✓ Webcam PC inizializzata - {self.resolution[0]}x{self.resolution[1]} @ {self.fps} FPS")
            return True
            
        except Exception as e:
            print(f"Errore nell'inizializzazione PC: {str(e)}")
            return False
    
    def _start_jetson_nano(self):
        """Inizializza la fotocamera per Jetson Nano usando OpenCV"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)
            
            if not self.cap.isOpened():
                raise Exception("Impossibile aprire la telecamera (Jetson Nano)")
            
            # Imposta la risoluzione
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            # Imposta gli FPS
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Imposta il formato della fotocamera
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            print(f"✓ Fotocamera Jetson Nano inizializzata - {self.resolution[0]}x{self.resolution[1]} @ {self.fps} FPS")
            return True
            
        except Exception as e:
            print(f"Errore nell'inizializzazione Jetson Nano: {str(e)}")
            return False
    
    def _start_raspberry_pi(self):
        """Inizializza la fotocamera per Raspberry Pi usando picamera2"""
        try:
            from picamera2 import Picamera2
            
            self.picam2 = Picamera2()
            self.config = self.picam2.create_video_configuration(
                main={"size": self.resolution, "format": "XRGB8888"}
            )
            
            self.picam2.configure(self.config)
            self.picam2.start()
            self.picam2.set_controls({"FrameRate": self.fps})
            
            print(f"✓ Fotocamera Raspberry Pi inizializzata - {self.resolution[0]}x{self.resolution[1]} @ {self.fps} FPS")
            return True
            
        except ImportError:
            print("Errore: picamera2 non è installato. Installa con: pip install picamera2")
            return False
        except Exception as e:
            print(f"Errore nell'inizializzazione Raspberry Pi: {str(e)}")
            return False
    
    def stop(self):
        """Arresta la fotocamera"""
        if self.is_recording:
            self.stop_recording()
        
        if self.device_type == DeviceType.RASPBERRY_PI:
            if self.picam2:
                self.picam2.stop()
                self.picam2.close()
        else:
            if self.cap:
                self.cap.release()
    
    def get_frame(self):
        """Cattura un frame dalla fotocamera"""
        try:
            if self.device_type == DeviceType.RASPBERRY_PI:
                return self._get_frame_raspberry_pi()
            elif self.device_type == DeviceType.JETSON_NANO:
                return self._get_frame_jetson_nano()
            else:  # PC
                return self._get_frame_pc()
        except Exception as e:
            print(f"Errore nella cattura del frame: {str(e)}")
            return None
    
    def _get_frame_pc(self):
        """Cattura un frame da PC (webcam USB)"""
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame.copy()
                return frame
        return None
    
    def _get_frame_jetson_nano(self):
        """Cattura un frame da Jetson Nano"""
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame.copy()
                return frame
        return None
    
    def _get_frame_raspberry_pi(self):
        """Cattura un frame da Raspberry Pi"""
        if self.picam2:
            try:
                array = self.picam2.capture_array("main")
                if array.shape[2] == 4:
                    array = array[:, :, :3]
                self.frame = array.copy()
                return array
            except Exception as e:
                print(f"Errore nella cattura del frame: {str(e)}")
                return None
        return None
    
    def capture_frame(self):
        """Restituisce il frame corrente in memoria"""
        if self.frame is not None:
            return self.frame.copy()
        return None
    
    def save_frame(self, frame, path):
        """Salva un frame su disco"""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            cv2.imwrite(path, frame)
            return True
        except Exception as e:
            print(f"Errore nel salvare l'immagine: {str(e)}")
            return False
    
    def start_recording(self, path):
        """Avvia la registrazione video"""
        if self.device_type == DeviceType.RASPBERRY_PI:
            return self._start_recording_raspberry_pi(path)
        else:
            return self._start_recording_jetson_pc(path)
    
    def _start_recording_jetson_pc(self, path):
        """Avvia la registrazione su Jetson Nano o PC (tramite file writer manuale)"""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.is_recording = True
            print(f"✓ Registrazione iniziata: {os.path.basename(path)}")
            return True
        except Exception as e:
            print(f"Errore nell'avviare la registrazione: {str(e)}")
            return False
    
    def _start_recording_raspberry_pi(self, path):
        """Avvia la registrazione su Raspberry Pi usando picamera2"""
        if not self.is_recording and self.picam2:
            try:
                from picamera2.encoders import H264Encoder
                from picamera2.outputs import FfmpegOutput
                
                self.encoder = H264Encoder(bitrate=10000000)
                self.output = FfmpegOutput(path, audio=False)
                self.picam2.start_recording(self.encoder, self.output)
                self.is_recording = True
                print(f"✓ Registrazione iniziata: {os.path.basename(path)}")
                return True
            except Exception as e:
                print(f"Errore nell'avviare la registrazione: {str(e)}")
                self.encoder = None
                self.output = None
                return False
        return False
    
    def stop_recording(self):
        """Ferma la registrazione video"""
        if self.device_type == DeviceType.RASPBERRY_PI:
            return self._stop_recording_raspberry_pi()
        else:
            return self._stop_recording_jetson_pc()
    
    def _stop_recording_jetson_pc(self):
        """Ferma la registrazione su Jetson Nano o PC"""
        try:
            self.is_recording = False
            print("✓ Registrazione fermata")
            return True
        except Exception as e:
            print(f"Errore nel fermare la registrazione: {str(e)}")
            return False
    
    def _stop_recording_raspberry_pi(self):
        """Ferma la registrazione su Raspberry Pi"""
        if self.is_recording and self.picam2:
            try:
                self.picam2.stop_recording()
                self.is_recording = False
                self.encoder = None
                self.output = None
                print("✓ Registrazione fermata")
                return True
            except Exception as e:
                print(f"Errore nel fermare la registrazione: {str(e)}")
                self.encoder = None
                self.output = None
                return False
        return False
    
    def apply_controls(self, frame, brightness, contrast, saturation):
        """Applica controlli di luminosità, contrasto e saturazione"""
        if brightness != 0:
            frame = cv2.convertScaleAbs(frame, alpha=1, beta=brightness)
        
        if contrast != 0:
            alpha = 1.0 + contrast / 100.0
            frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=0)
        
        if saturation != 0:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            s = cv2.add(s, saturation)
            s = np.clip(s, 0, 255)
            hsv = cv2.merge([h, s, v])
            frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return frame
    
    def get_resolution(self):
        """Restituisce la risoluzione impostata"""
        return self.resolution
    
    def get_fps(self):
        """Restituisce gli FPS impostati"""
        return self.fps
    
    def set_resolution(self, resolution):
        """Imposta la risoluzione della fotocamera"""
        self.resolution = resolution
        
        if self.device_type == DeviceType.RASPBERRY_PI:
            if self.picam2:
                self.config = self.picam2.create_video_configuration(
                    main={"size": self.resolution, "format": "XRGB8888"}
                )
                self.picam2.configure(self.config)
        else:
            if self.cap:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
    
    def set_fps(self, fps):
        """Imposta gli FPS della fotocamera"""
        self.fps = fps
        
        if self.device_type == DeviceType.RASPBERRY_PI:
            if self.picam2:
                self.picam2.set_controls({"FrameRate": fps})
        else:
            if self.cap:
                self.cap.set(cv2.CAP_PROP_FPS, fps)
    
    def get_device_type(self):
        """Restituisce il tipo di dispositivo attualmente configurato"""
        return self.device_type
    
    def set_device_type(self, device_type):
        """Cambia il tipo di dispositivo"""
        if self.device_type != device_type:
            self.stop()
            self.device_type = device_type
            self.start()
    
    def list_available_cameras(self):
        """Elenca le webcam disponibili (solo per PC/Jetson)"""
        if self.device_type == DeviceType.RASPBERRY_PI:
            return [0]  # Raspberry Pi ha una sola camera
        
        available = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available.append(i)
                cap.release()
        
        return available if available else [0]
