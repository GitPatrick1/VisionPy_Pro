#!/bin/bash

set -e

echo -e "\n--- Inizio Installazione Dipendenze ---\n"

echo "1. Aggiornamento della lista dei pacchetti di sistema..."
sudo apt update

echo -e "\n2. Installazione delle librerie e dipendenze richieste..."
echo "   Questo potrebbe richiedere alcuni minuti."

if grep -qi 'raspberry' /proc/device-tree/model 2>/dev/null; then
    echo "Dispositivo rilevato: Raspberry Pi"
    echo -e "\nInstallazione dipendenze aggiuntive per Raspberry Pi...\n"
    sudo apt install -y \
        python3-picamera2 \
        python3-libcamera \
        libcamera-dev \
        libcamera-apps
else
    echo "Dispositivo rilevato: Non Raspberry Pi (PC/Jetson etc.)"
    # Prova comunque a installare queste dipendenze (non appesantisce)
    sudo apt install -y python3-picamera2 python3-libcamera libcamera-dev libcamera-apps || true
fi

# Dipendenze comuni a tutti i dispositivi
sudo apt install -y \
    python3-pyqt6 \
    python3-opencv \
    python3-numpy \
    ffmpeg \
    cmake

echo -e "\n--- Installazione Completata con Successo! ---"
echo -e "Tutte le dipendenze necessarie sono state installate.\n"
echo "Per avviare l'applicazione, esegui:"
echo -e "\t./run.sh\n"
