# RecordingThread.py (VERSIONE FINALE E CORRETTA)

import os
import cv2
import queue
from PyQt6.QtCore import QThread, pyqtSignal

class RecordingThread(QThread):
    recording_finished = pyqtSignal(bool)
    status_update = pyqtSignal(str)
    
    def __init__(self, camera_manager):
        super().__init__()
        self.camera_manager = camera_manager
        self.recording_path = None
        self.is_recording = False
        self.video_writer = None
        self.frame_queue = queue.Queue(maxsize=30)

    def add_frame_to_queue(self, frame):
        """Aggiunge un frame alla coda per la registrazione."""
        if self.is_recording:
            if self.frame_queue.full():
                try:
                    self.frame_queue.get_nowait()
                except queue.Empty:
                    pass
            self.frame_queue.put(frame)

    def start_recording(self, path, width, height, fps):
        self.recording_path = path
        self.width = width
        self.height = height
        self.fps = fps
        self.is_recording = True
        self.start()
        
    def run(self):
        try:
            os.makedirs(os.path.dirname(self.recording_path), exist_ok=True)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(
                self.recording_path, 
                fourcc, 
                self.fps, 
                (self.width, self.height)
            )

            if not self.video_writer.isOpened():
                raise Exception("Impossibile aprire il file video per la scrittura.")

            self.status_update.emit(f"Registrazione in corso: {os.path.basename(self.recording_path)}")
            
            while self.is_recording:
                try:
                    frame = self.frame_queue.get(timeout=1.0)
                    self.video_writer.write(frame)
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Errore durante la scrittura del frame: {e}")
                    break
            
        except Exception as e:
            self.status_update.emit(f"Errore durante la registrazione: {str(e)}")
            self.recording_finished.emit(False)
            return
            
    def stop_recording(self):
        self.is_recording = False
        if self.isRunning():
            self.wait(5000)

        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        
        self.status_update.emit("Registrazione fermata e salvata.")
        self.recording_finished.emit(True)