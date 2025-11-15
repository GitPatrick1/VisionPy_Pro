# SettingsManager.py

import os
import json

class SettingsManager:
    def __init__(self):
        # Crea la directory VisionPy_Pro se non esiste e definisce il percorso del file
        self.app_dir = os.path.expanduser("~/VisionPy_Pro")
        self.settings_file = os.path.join(self.app_dir, "settings.json")
        self.default_settings = {
            "music_muted": False
        }

    def load_settings(self):
        """Carica le impostazioni dal file JSON. Se il file non esiste, usa quelle di default."""
        if not os.path.exists(self.settings_file):
            return self.default_settings
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                # Unisce le impostazioni caricate con quelle di default per gestire nuove opzioni
                return {**self.default_settings, **settings}
        except (json.JSONDecodeError, IOError):
            print("Errore nel leggere il file delle impostazioni, uso quelle di default.")
            return self.default_settings

    def save_setting(self, key, value):
        """Salva una singola impostazione nel file JSON."""
        settings = self.load_settings()
        settings[key] = value
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except IOError:
            print(f"Errore nel salvare l'impostazione '{key}'.")