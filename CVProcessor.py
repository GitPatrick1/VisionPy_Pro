# CVProcessor.py (VERSIONE COMPLETA CON YOLO)

import cv2
import numpy as np
import os
from datetime import datetime

class CVProcessor:
    def __init__(self):
        # Carica il classificatore Haar Cascade per il rilevamento dei volti
        face_cascade_path = os.path.join(os.path.dirname(__file__), 'models', 'haarcascade_frontalface_default.xml')
        self.face_cascade = cv2.CascadeClassifier(face_cascade_path)

        # Inizializzazione di YOLO
        self.yolo_net = None
        self.classes = []
        try:
            yolo_dir = os.path.join(os.path.dirname(__file__), 'yolo')
            weights_path = os.path.join(yolo_dir, 'yolov4-tiny.weights')
            config_path = os.path.join(yolo_dir, 'yolov4-tiny.cfg')
            names_path = os.path.join(yolo_dir, 'coco.names')

            self.yolo_net = cv2.dnn.readNet(weights_path, config_path)
            with open(names_path, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]

            layer_names = self.yolo_net.getLayerNames()
            self.yolo_output_layers = [layer_names[i - 1] for i in self.yolo_net.getUnconnectedOutLayers()]
            print("Modello YOLO caricato con successo.")
        except Exception as e:
            print(f"Errore nel caricare il modello YOLO: {e}")
            print("Assicurati che i file del modello siano nella cartella 'yolo/'.")
    
    def draw_osd(self, frame, mode, resolution, fps, show_osd=True):
        if not show_osd or frame is None:
            return frame
            
        osd_frame = frame.copy()
        h, w = osd_frame.shape[:2]
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        color = (255, 255, 255)
        outline_color = (0, 0, 0)
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        texts = [
            f"VisionPy Pro",
            f"Modalita: {mode}",
            f"Risoluzione: {resolution[0]}x{resolution[1]}",
            f"FPS: {fps}",
            f"{now}"
        ]
        
        y_offset = 30
        for text in texts:
            cv2.putText(osd_frame, text, (11, y_offset + 1), font, font_scale, outline_color, thickness + 1)
            cv2.putText(osd_frame, text, (10, y_offset), font, font_scale, color, thickness)
            y_offset += 30
        
        return osd_frame

    def detect_objects_yolo(self, frame):
        if self.yolo_net is None:
            cv2.putText(frame, "Modello YOLO non disponibile", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return frame

        frame = frame.copy()
        height, width, channels = frame.shape

        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.yolo_net.setInput(blob)
        outputs = self.yolo_net.forward(self.yolo_output_layers)

        boxes = []
        confidences = []
        class_ids = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x, y + 30), font, 2, color, 2)
        
        return frame

    def process_frame(self, frame, mode, performance_scale=0.5, show_osd=True, resolution=(1280, 720), fps=30, mirror=False, **kwargs):
        if frame is None:
            return None
            
        original_h, original_w = frame.shape[:2]
        small_frame = cv2.resize(frame, (0,0), fx=performance_scale, fy=performance_scale)
        processed_small_frame = small_frame.copy()
        
        if mode == "Rilevamento Volti":
            processed_small_frame = self.detect_faces(processed_small_frame)
        elif mode == "Rilevamento Contorni":
            processed_small_frame = self.detect_edges(processed_small_frame)
        elif mode == "Segmentazione per Colore":
            hue_min = kwargs.get('hue_min', 0)
            hue_max = kwargs.get('hue_max', 179)
            sat_min = kwargs.get('sat_min', 0)
            sat_max = kwargs.get('sat_max', 255)
            val_min = kwargs.get('val_min', 0)
            val_max = kwargs.get('val_max', 255)
            processed_small_frame = self.segment_by_color(processed_small_frame, hue_min, hue_max, sat_min, sat_max, val_min, val_max)
        elif mode == "Rilevamento Movimento":
            processed_small_frame = self.detect_motion(processed_small_frame)
        elif mode == "Sfocatura Sfondo":
            processed_small_frame = self.background_blur(processed_small_frame)
        elif mode == "Rilevamento Oggetti (YOLO)":
            processed_frame = self.detect_objects_yolo(frame)
            if show_osd:
                processed_frame = self.draw_osd(processed_frame, mode, resolution, fps, show_osd)
            if mirror:
                processed_frame = cv2.flip(processed_frame, 1)
            return processed_frame
            
        result = cv2.resize(processed_small_frame, (original_w, original_h))
        
        if show_osd:
            result = self.draw_osd(result, mode, resolution, fps, show_osd)
        
        if mirror:
            result = cv2.flip(result, 1)
        
        return result

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.circle(frame, (x + w//2, y + h//2), 2, (0, 0, 255), 3)
        return frame
        
    def detect_edges(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return edges_bgr
        
    def segment_by_color(self, frame, hue_min, hue_max, sat_min, sat_max, val_min, val_max):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([hue_min, sat_min, val_min])
        upper = np.array([hue_max, sat_max, val_max])
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        return result
        
    def detect_motion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if not hasattr(self, 'prev_gray') or self.prev_gray is None:
            self.prev_gray = gray.copy()
            return frame
        frame_delta = cv2.absdiff(self.prev_gray, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_mask = np.zeros_like(frame)
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(motion_mask, (x, y), (x + w, y + h), (0, 255, 255), -1)
        result = cv2.addWeighted(frame, 0.7, motion_mask, 0.3, 0)
        self.prev_gray = gray.copy()
        return result
        
    def background_blur(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=4, minSize=(20, 20)
        )
        if len(faces) == 0:
            return cv2.GaussianBlur(frame, (15, 15), 0)
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        for (x, y, w, h) in faces:
            cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1)
        blurred = cv2.GaussianBlur(frame, (51, 51), 0)
        result = np.where(mask[..., None] == 255, frame, blurred)
        return result