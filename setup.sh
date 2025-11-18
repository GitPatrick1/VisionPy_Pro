#!/bin/bash

echo "Aggiornamento pacchetti di sistema e installazione dipendenze..."

sudo apt update

sudo apt install -y \
python3-pyqt6 \
python3-opencv \
python3-numpy \
python3-picamera2 \
python3-libcamera \
libcamera-dev \
libcamera-apps \
ffmpeg \
cmake

echo "Tutte le dipendenze sono state installate con successo."
echo "Per avviare l'applicazione usa ./run.sh"
