#!/bin/bash

echo "Aggiornamento pacchetti di sistema e installazione dipendenze di sistema..."

sudo apt update
sudo apt install -y libcamera-dev libcamera-apps cmake ffmpeg python3-pip python3-opencv

echo "Aggiornamento pip..."
pip3 install --upgrade pip

echo "Installazione dipendenze Python globali..."

pip3 install PyQt6 numpy picamera2

echo "Setup completato. Per eseguire il programma usa ./run.sh"
