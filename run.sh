#!/bin/bash

MAIN_SCRIPT="main.py"
PYTHON_CMD="python3"

if [ ! -f "$MAIN_SCRIPT" ]; then
    echo -e "\n[ERRORE] Lo script principale '$MAIN_SCRIPT' non è stato trovato."
    echo -e "Assicurati di essere nella cartella corretta e che il file esista.\n"
    exit 1
fi

echo -e "--- Avvio dell'applicazione ---"
echo "Esecuzione di: $PYTHON_CMD $MAIN_SCRIPT"
echo "------------------------------------"

 $PYTHON_CMD "$MAIN_SCRIPT"

echo -e "\n--- Applicazione terminata ---"
