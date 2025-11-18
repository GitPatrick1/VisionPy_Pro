#!/bin/bash

echo "Aggiornamento pacchetti di sistema e installazione dipendenze di sistema..."
sudo apt update
sudo apt install -y libcamera-dev libcamera-apps cmake ffmpeg python3-venv python3-pip

echo "Creazione ambiente virtuale (venv)..."
python3 -m venv venv

echo "Attivazione dell'ambiente virtuale..."
source venv/bin/activate

echo "Aggiornamento pip..."
pip install --upgrade pip

echo "Installazione dipendenze Python da requirements.txt..."
pip install -r requirements.txt

echo "Setup completato. Per eseguire il programma:"
echo "source venv/bin/activate"
echo "./run.sh"
