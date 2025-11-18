import os
import json

class SettingsManager:
    """Gestisce le impostazioni dell'applicazione per tutti i dispositivi"""
    
    def __init__(self):
        # Crea la directory VisionPy_Pro se non esiste
        self.app_dir = os.path.expanduser("~/VisionPy_Pro")
        self.settings_file = os.path.join(self.app_dir, "settings.json")
        
        # Impostazioni di default
        self.default_settings = {
            "music_muted": False,
            "device_type": "raspberry_pi",          # DEFAULT: PC
            "resolution": [1280, 720],
            "fps": 30,
            "camera_index": 0             # NEW: Per PC/Jetson, quale webcam usare
        }
        
        # Crea la directory se non esiste
        os.makedirs(self.app_dir, exist_ok=True)
    
    def load_settings(self):
        """Carica le impostazioni dal file JSON"""
        if not os.path.exists(self.settings_file):
            return self.default_settings.copy()
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Unisce le impostazioni caricate con quelle di default
            return {**self.default_settings, **settings}
        except (json.JSONDecodeError, IOError):
            print("Errore nel leggere il file delle impostazioni, uso quelle di default.")
            return self.default_settings.copy()
    
    def save_setting(self, key, value):
        """Salva una singola impostazione nel file JSON"""
        settings = self.load_settings()
        settings[key] = value
        
        try:
            os.makedirs(self.app_dir, exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
        except IOError as e:
            print(f"Errore nel salvare l'impostazione '{key}': {e}")
    
    def get_device_type(self):
        """Restituisce il tipo di dispositivo salvato"""
        settings = self.load_settings()
        return settings.get("device_type", "pc")
    
    def set_device_type(self, device_type):
        """Salva il tipo di dispositivo"""
        self.save_setting("device_type", device_type)
    
    def get_camera_index(self):
        """Restituisce l'indice della webcam (per PC/Jetson)"""
        settings = self.load_settings()
        return settings.get("camera_index", 0)
    
    def set_camera_index(self, index):
        """Salva l'indice della webcam"""
        self.save_setting("camera_index", index)
    
    def get_resolution(self):
        """Restituisce la risoluzione salvata"""
        settings = self.load_settings()
        res = settings.get("resolution", [1280, 720])
        return tuple(res)
    
    def set_resolution(self, resolution):
        """Salva la risoluzione"""
        self.save_setting("resolution", list(resolution))
    
    def get_fps(self):
        """Restituisce gli FPS salvati"""
        settings = self.load_settings()
        return settings.get("fps", 30)
    
    def set_fps(self, fps):
        """Salva gli FPS"""
        self.save_setting("fps", fps)
