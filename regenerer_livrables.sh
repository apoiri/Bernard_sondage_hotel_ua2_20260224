#!/bin/bash
# À lancer dans le Terminal macOS (PAS dans le terminal de Cursor) pour régénérer
# les livrables et mettre à jour la date de sondage_hotel_data.csv dans votre dossier.
# (Exécuter depuis le terminal de Cursor peut ne pas mettre à jour les fichiers
# visibles dans le Finder.)
#
# Usage : ouvrir l'app Terminal (Mac), puis :
#   cd "/Users/alainpoirier/Desktop/Bernard_sondage_hotel_ua2_20260224"
#   bash regenerer_livrables.sh
#
# Ou double-cliquer sur ce fichier (si exécution autorisée).

REP="/Users/alainpoirier/Desktop/Bernard_sondage_hotel_ua2_20260224"
cd "$REP" || exit 1
echo "Répertoire : $(pwd)"
echo "--- Date du CSV AVANT ---"
ls -la sondage_hotel_data.csv 2>/dev/null || echo "Fichier absent"
echo ""
echo "--- Exécution du pipeline ---"
python3 run_pipeline.py
echo ""
echo "--- Date du CSV APRÈS ---"
ls -la sondage_hotel_data.csv 2>/dev/null || echo "Fichier absent"
echo ""
echo "Si la date ci-dessus est aujourd'hui, le fichier a bien été mis à jour dans ce dossier."
