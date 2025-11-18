#!/bin/bash

# Questo script attiva l'ambiente virtuale e lancia l'applicazione.

# Controlla di essere nella directory giusta
if [ ! -d "venv" ]; then
    echo "Errore: ambiente virtuale 'venv' non trovato."
    echo "Esegui prima lo script di installazione con './setup.sh'"
    exit 1
fi

# Attiva il virtual environment
source venv/bin/activate

# Esegui il programma principale (main.py)
python main.py

