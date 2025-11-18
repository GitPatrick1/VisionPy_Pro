#!/bin/bash

# Questo script installa tutte le dipendenze per VisionPy Pro.
# Esci immediatamente se un comando fallisce.
set -e

# --- Configurazione ---
# Ottiene la directory corrente dove si trova lo script
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
MODELS_DIR="$PROJECT_DIR/models"
YOLO_DIR="$PROJECT_DIR/yolo"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"

# --- Inizio Script ---
echo "###############################################"
echo "#   Script di Installazione per VisionPy Pro   #"
echo "###############################################"
echo ""
echo "Questa operazione richiede una connessione internet e i privilegi di sudo."
echo "Directory del progetto: $PROJECT_DIR"
echo ""

# 1. Aggiorna la lista dei pacchetti e installa le dipendenze di sistema
echo "[1/6] Aggiornamento dei pacchetti di sistema e installazione delle dipendenze..."
sudo apt update
sudo apt install -y ffmpeg python3-pip python3-venv wget git
sudo apt-get update
sudo apt-get install libcap-dev
echo "✓ Dipendenze di sistema installate."
echo ""

# 2. Crea e attiva l'ambiente virtuale Python
echo "[2/6] Configurazione dell'ambiente virtuale Python..."
if [ ! -d "$VENV_DIR" ]; then
    echo "Creazione dell'ambiente virtuale in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "L'ambiente virtuale esiste già."
fi
source "$VENV_DIR/bin/activate"
echo "✓ Ambiente virtuale attivo."
echo ""

# 3. Installa le dipendenze Python
echo "[3/6] Installazione delle dipendenze Python da requirements.txt..."
if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -r "$REQUIREMENTS_FILE"
    echo "✓ Dipendenze Python installate."
else
    echo "⚠️ Attenzione: requirements.txt non trovato in $PROJECT_DIR. Salto questa fase."
fi
echo ""

# 4. Scarica il modello Haar Cascade per il rilevamento dei volti
echo "[4/6] Download del modello per il rilevamento dei volti..."
if [ ! -d "$MODELS_DIR" ]; then
    echo "Creazione della directory 'models'..."
    mkdir -p "$MODELS_DIR"
fi
if [ ! -f "$MODELS_DIR/haarcascade_frontalface_default.xml" ]; then
    echo "Download del file del modello..."
    wget -O "$MODELS_DIR/haarcascade_frontalface_default.xml" "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    echo "✓ Modello scaricato."
else
    echo "✓ Il file del modello esiste già."
fi
echo ""

# 5. --- NUOVO: Scarica i modelli YOLO ---
echo "[5/6] Download dei modelli YOLO..."
if [ ! -d "$YOLO_DIR" ]; then
    echo "Creazione della directory 'yolo'..."
    mkdir -p "$YOLO_DIR"
fi

if [ ! -f "$YOLO_DIR/yolov4-tiny.weights" ]; then
    echo "Download dei pesi YOLO..."
    wget -O "$YOLO_DIR/yolov4-tiny.weights" "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights"
else
    echo "✓ I pesi YOLO esistono già."
fi

if [ ! -f "$YOLO_DIR/yolov4-tiny.cfg" ]; then
    echo "Download della configurazione YOLO..."
    wget -O "$YOLO_DIR/yolov4-tiny.cfg" "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg"
else
    echo "✓ La configurazione YOLO esiste già."
fi

if [ ! -f "$YOLO_DIR/coco.names" ]; then
    echo "Download dei nomi delle classi YOLO..."
    wget -O "$YOLO_DIR/coco.names" "https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names"
else
    echo "✓ I nomi delle classi YOLO esistono già."
fi
echo "✓ Modelli YOLO pronti."
echo ""

# 6. Finalizzazione e istruzioni
echo "[6/6] Pulizia e finalizzazione..."
deactivate
echo "✓ Ambiente virtuale disattivato."

echo ""
echo "###############################################"
echo "#              Installazione Completata!      #"
echo "###############################################"
echo ""
echo "Per avviare l'applicazione, usa i seguenti comandi:"
echo ""
echo "  1. Entra nella directory del progetto (se non ci sei già):"
echo "     cd $PROJECT_DIR"
echo ""
echo "  2. Attiva l'ambiente virtuale:"
echo "     source venv/bin/activate"
echo ""
echo "  3. Esegui l'applicazione:"
echo "     python main.py"
echo ""
echo "Oppure, usa lo script semplificato:"
echo "  ./run.sh"
echo ""
echo "Goditi VisionPy Pro!"
