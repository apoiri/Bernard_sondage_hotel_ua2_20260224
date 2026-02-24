#!/bin/bash
# Lance l'interface Streamlit et ouvre Chrome sur la page (pas Safari).
# Usage : ./lancer_interface_chrome.sh
# Ou : bash lancer_interface_chrome.sh

cd "$(dirname "$0")"

echo "Démarrage de Streamlit (interface en arrière-plan)..."
# --server.headless true : n'ouvre pas le navigateur par défaut (évite Safari)
streamlit run interface_streamlit_config.py --server.headless true &
PID=$!
echo "Attente du démarrage du serveur..."
sleep 4
echo "Ouverture de Chrome sur http://localhost:8501"
open -a "Google Chrome" "http://localhost:8501"
echo "Interface ouverte dans Chrome. Pour arrêter : Ctrl+C dans ce terminal."
wait $PID
