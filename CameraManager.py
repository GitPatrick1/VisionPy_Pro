# CameraManager.py

import os
import cv2
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from PyQt6.QtCore import QObject

class CameraManager(QObject):
    def __init__(self):
        super().__init__()
        self.picam2 = None
        self.config = None
        self.frame = None
        self.resolution = (1920, 1080)
        self.fps = 30
        self.is_recording = False
        self.encoder = None
        self.output = None
        
    def start(self):
        try:
            self.picam2 = Picamera2()
            self.config = self.picam2.create_video_configuration(
                main={"size": self.resolution, "format": "XRGB8888"}
            )
            self.picam2.configure(self.config)
            self.picam2.start()
            self.picam2.set_controls({"FrameRate": self.fps})
            return True
        except Exception as e:
            print(f"Errore nell'avvio della fotocamera: {str(e)}")
            return False
            
    def stop(self):
        if self.picam2:
            if self.is_recording:
                self.stop_recording()
            self.picam2.stop()
            self.picam2.close()
            
    def get_frame(self):
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
        if self.frame is not None:
            return self.frame.copy()
        return None
        
    def save_frame(self, frame, path):
        try:
            cv2.imwrite(path, frame)
            return True
        except Exception as e:
            print(f"Errore nel salvare l'immagine: {str(e)}")
            return False
            
    def start_recording(self, path):
        if not self.is_recording and self.picam2:
            try:
                self.encoder = H264Encoder(bitrate=10000000)
                self.output = FfmpegOutput(path, audio=False)
                self.picam2.start_recording(self.encoder, self.output)
                self.is_recording = True
                return True
            except Exception as e:
                print(f"Errore nell'avviare la registrazione: {str(e)}")
                self.encoder = None
                self.output = None
                return False
        return False

    def stop_recording(self):
        if self.is_recording and self.picam2:
            try:
                self.picam2.stop_recording()
                self.is_recording = False
                self.encoder = None
                self.output = None
                return True
            except Exception as e:
                print(f"Errore nel fermare la registrazione: {str(e)}")
                self.encoder = None
                self.output = None
                return False
        return False
            
    def apply_controls(self, frame, brightness, contrast, saturation):
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
        return self.resolution
        
    def get_fps(self):
        return self.fps
        
    def set_resolution(self, resolution):
        self.resolution = resolution
        if self.picam2:
            self.config = self.picam2.create_video_configuration(
                main={"size": self.resolution, "format": "XRGB8888"}
            )
            self.picam2.configure(self.config)
            
    def set_fps(self, fps):
        self.fps = fps
        if self.picam2:
            self.picam2.set_controls({"FrameRate": fps})