# 🎥 VisionPy Pro - Applicazione Avanzata di Acquisizione e Elaborazione Video

Applicazione multi-dispositivo per acquisire, elaborare e registrare video in tempo reale. Supporta **PC (webcam USB)**, **Jetson Nano** e **Raspberry Pi** con pipeline ottimizzate per ogni hardware.

---

## ✨ Caratteristiche Principali

### 🎯 Multi-Dispositivo
- **PC**: Webcam USB standard (Windows, macOS, Linux)
- **Jetson Nano**: Pipeline OpenCV con accelerazione CUDA
- **Raspberry Pi**: Picamera2 con encoder H264 nativo

### 📹 Funzionalità Video
- ✅ Visualizzazione live della fotocamera
- ✅ Scatto foto (PNG/JPG)
- ✅ Registrazione video (MP4)
- ✅ Timer programmabile per foto/video
- ✅ Galleria media integrata

### 🎨 Elaborazione Immagine
- ✅ Riconoscimento volti (Face Detection)
- ✅ Rilevamento contorni (Edge Detection)
- ✅ Rilevamento oggetti YOLO
- ✅ Conversione HSV e filtri colore
- ✅ Controllo luminosità, contrasto, saturazione
- ✅ Specchiamento orizzontale/verticale

### 🎵 Interfaccia
- ✅ UI moderna e intuitiva (PyQt6)
- ✅ Notifiche on-screen (OSD)
- ✅ Controlli laterali per parametri
- ✅ Menu dispositivo dinamico
- ✅ Selezione webcam multi-camera

---

## 🚀 Installazione Rapida

### Prerequisiti
- Python 3.7+
- Sistema operativo: Linux, Windows o macOS

### Setup automatico

```bash
# Clona o scarica il progetto
cd VisionPy_Pro

# Rendi eseguibili gli script
chmod +x setup.sh run.sh

# Installa le dipendenze
./setup.sh

# Avvia l'applicazione
./run.sh
```

### Dipendenze installate

- `python3-pyqt6` - Framework UI
- `python3-opencv` - Elaborazione video
- `python3-numpy` - Calcoli numerici
- `python3-picamera2` - Camera Raspberry Pi
- `ffmpeg` - Codec video
- `cmake` - Build tools

---

## 📋 Guida Rapida di Utilizzo

### Primo Avvio

1. Esegui `./run.sh`
2. Verrà mostrato il **dialog di selezione dispositivo**
3. Scegli il tuo dispositivo:
   - 🖥️ **PC** (webcam USB)
   - 🟢 **Jetson Nano** (CSI camera)
   - 🍓 **Raspberry Pi** (Picamera2)
4. La scelta viene salvata automaticamente

### Interfaccia Principale

```
┌──────────────────────────────────────────┐
│ VisionPy Pro                             │
├──────────────────────────────────────────┤
│                                          │
│  ┌──────────────────┐  ┌──────────────┐ │
│  │                  │  │   Controlli  │ │
│  │   Feed Video     │  │   Laterali   │ │
│  │                  │  │              │ │
│  └──────────────────┘  └──────────────┘ │
│                                          │
├──────────────────────────────────────────┤
│ Dispositivo: PC | 1280x720 | 30 FPS    │
└──────────────────────────────────────────┘
```

---

## ⌨️ Scorciatoie da Tastiera

| Tasto | Azione |
|-------|--------|
| **C** | Scatta una foto |
| **V** | Avvia/Ferma registrazione video |
| **M** | Attiva/Disattiva specchiamento |
| **T** | Avvia timer (foto/video) |
| **F11** | Attiva/Disattiva schermo intero |
| **ESC** | Chiudi applicazione |

---

## 🎮 Menu Principale

### File
- Salva con nome (esporta immagine)
- Esci

### Visualizza
- Schermo intero

### Dispositivo
- 🖥️ Usa PC
- 🟢 Usa Jetson Nano
- 🍓 Usa Raspberry Pi
- **Seleziona Webcam** (0-4) *su PC/Jetson*

### Scorciatoie
- Elenco scorciatoie da tastiera

### Aiuto
- Informazioni sull'applicazione

---

## 🎛️ Pannello di Controllo Laterale

### Modalità di Elaborazione
Seleziona tra diverse modalità di elaborazione:
- **Normale** - Video senza elaborazione
- **Facce** - Rilevamento volti
- **Contorni** - Edge detection
- **YOLO** - Rilevamento oggetti
- **Filtro Colore** - Filtri HSV personalizzabili

### Controlli Video
- **Luminosità** - Regola luminosità
- **Contrasto** - Regola contrasto
- **Saturazione** - Regola colori

### Filtri Avanzati
- **HSV Min/Max** - Sliders per Hue, Saturation, Value
- **Specchiamento** - Flip verticale/orizzontale
- **OSD** - Visualizza informazioni on-screen

### Audio
- **Musica di Sottofondo** - On/Off

### Timer
- **Azione** - Foto o Video
- **Ritardo** - Secondi prima dell'azione

---

## 📁 Struttura di Progetto

```
VisionPy_Pro/
├── main.py                    # Entry point
├── MainWindow.py              # Finestra principale
├── CameraManager.py           # Gestione fotocamere
├── CameraThread.py            # Thread cattura video
├── RecordingThread.py         # Thread registrazione
├── CVProcessor.py             # Elaborazione OpenCV
├── DeviceManager.py           # Selezione dispositivo
├── SettingsManager.py         # Gestione configurazione
├── ControlPanel.py            # Pannello controlli
├── CameraWidget.py            # Widget visualizzazione
├── GalleryDialog.py           # Galleria media
├── MenuBar.py                 # Barra menu
├── TimerManager.py            # Gestore timer
├── PreviewWidget.py           # Anteprima foto
├── OSDNotification.py         # Notifiche on-screen
├── PreviewDialog.py           # Dialog anteprima
├── MediaThumbnailWidget.py    # Thumbnail media
├── setup.sh                   # Script installazione
├── run.sh                     # Script avvio
└── README.md                  # Questo file

~/VisionPy_Pro/               # Home directory app
├── settings.json             # Configurazione salvata
├── photos/                   # Foto catturate
└── videos/                   # Video registrati
```

---

## 💾 File di Configurazione

### settings.json

Salvato in `~/VisionPy_Pro/settings.json`:

```json
{
    "music_muted": false,
    "device_type": "pc",
    "resolution": [1280, 720],
    "fps": 30,
    "camera_index": 0
}
```

**Campo** | **Descrizione** | **Valori**
---------|---------------|-----------
`music_muted` | Musica di sottofondo | `true` / `false`
`device_type` | Dispositivo in uso | `"pc"`, `"jetson_nano"`, `"raspberry_pi"`
`resolution` | Risoluzione video | `[width, height]`
`fps` | Frame per secondo | `25`, `30`, `60`
`camera_index` | Indice webcam (PC/Jetson) | `0`, `1`, `2`, `3`, `4`

---

## 🎨 Modalità di Elaborazione

### 1. Normale
Visualizza il video senza elaborazione.

### 2. Rilevamento Volti
Rileva e evidenzia i volti nella scena:
- Rettangoli verdi intorno ai volti
- Basato su Haar Cascade
- Tempo reale

### 3. Rilevamento Contorni
Evidenzia i contorni degli oggetti:
- Filtro Canny
- Contorni bianchi su sfondo nero
- Utile per analisi forme

### 4. YOLO Object Detection
Riconoscimento oggetti avanzato:
- Modello YOLO pre-addestrato
- Classe e confidenza per ogni oggetto
- Riquadri colorati con label

### 5. Filtro Colore HSV
Isola colori specifici:
- Regola Hue, Saturation, Value
- Preview in tempo reale
- Utile per tracking colori

---

## 📊 Specifiche Tecnici

### Supporto Dispositivi

#### PC (Webcam USB)
```
Sorgente: cv2.VideoCapture
Codec: H264/H265
Risoluzione: 320x240 → 1920x1080
FPS: 15-60 (dipende webcam)
Latenza: 50-100ms
```

#### Jetson Nano
```
Sorgente: cv2.VideoCapture (V4L2)
GPU: NVIDIA Maxwell (CUDA)
Codec: H264 hardware
Risoluzione: 1280x720, 1920x1080
FPS: 20-30
Latenza: 30-50ms
```

#### Raspberry Pi
```
Sorgente: Picamera2
ISP: Raspberry Pi ISP
Codec: H264 hardware
Risoluzione: 1280x720, 1920x1080
FPS: 25-30
Latenza: 20-40ms
```

### Requisiti Minimi

| Componente | Minimo | Consigliato |
|-----------|--------|-----------|
| **CPU** | Dual-core 1GHz | Quad-core 2GHz+ |
| **RAM** | 512MB | 2GB+ |
| **Storage** | 500MB | 2GB+ |
| **Python** | 3.7 | 3.8+ |

---

## 🔍 Troubleshooting

### Problema: "Fotocamera non trovata"

**Soluzione:**
```bash
# Verifica webcam disponibili
ls -la /dev/video*

# Su Raspberry Pi, abilita la camera
sudo raspi-config
# Vai a: Interface Options → Camera → Enable
# Riavvia
sudo reboot
```

### Problema: YOLO molto lento

**Soluzione:**
- Usa risoluzioni inferiori (640x480 invece di 1920x1080)
- Riduci FPS
- Su Jetson Nano, beneficia dell'accelerazione GPU

### Problema: Picamera2 non trovato

**Soluzione:**
```bash
# Reinstalla picamera2
sudo apt install -y python3-picamera2

# Verifica installazione
python3 -c "from picamera2 import Picamera2"
```

### Problema: "Permessi negati" su setup.sh

**Soluzione:**
```bash
chmod +x setup.sh run.sh
```

---

## 🎓 Per Sviluppatori

### Architettura

```
MainWindow (PyQt6)
    ├─ CameraThread (QThread)
    │   ├─ CameraManager (cattura frame)
    │   └─ CVProcessor (elaborazione)
    ├─ RecordingThread (QThread)
    │   └─ Salvataggio video
    ├─ ControlPanel (UI controlli)
    └─ MenuBar (menu)

SettingsManager (JSON storage)
    └─ ~/VisionPy_Pro/settings.json

DeviceManager (selezione dispositivo)
    ├─ PC
    ├─ Jetson Nano
    └─ Raspberry Pi
```

### Estensibilità

Per aggiungere un nuovo dispositivo:

1. **Aggiorna DeviceManager.py:**
```python
class DeviceType(Enum):
    PC = "pc"
    JETSON_NANO = "jetson_nano"
    RASPBERRY_PI = "raspberry_pi"
    MIO_DISPOSITIVO = "mio_dispositivo"  # ← NUOVO
```

2. **Aggiungi metodi in CameraManager.py:**
```python
def _start_mio_dispositivo(self):
    # Implementa logica di avvio

def _get_frame_mio_dispositivo(self):
    # Implementa cattura frame
```

---

## 📝 License

MIT License - Vedi LICENSE file

---

## 🤝 Contributi

Segnalazioni di bug e pull requests sono benvenuti!

---

## 📞 Supporto

Per domande o problemi:
1. Controlla il troubleshooting sopra
2. Leggi i commenti nel codice
3. Verifica la configurazione in settings.json

---

## 🎉 Buon Utilizzo!

**VisionPy Pro v2.0** - Acquisizione e elaborazione video multi-dispositivo

Supporta: **PC** • **Jetson Nano** • **Raspberry Pi**

Sviluppato con ❤️ usando PyQt6 e OpenCV
