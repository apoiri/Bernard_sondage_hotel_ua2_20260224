# -*- coding: utf-8 -*-
"""
Module 0 – Config étendue (tarification dynamique, types de chambre, etc.)
Simulation « L'Hôtel Boutique Art de Vivre »

Charge la config de base (m01) et, si présent, le fichier config_tarification_dynamique.json.
Expose get_config_etendue() = fusion des deux (config m01 + clés du JSON).
"""

import json
from pathlib import Path

# Répertoire du projet (même dossier que m01)
REP_PROJET = Path(__file__).resolve().parent
FICHIER_CONFIG_ETENDUE = REP_PROJET / "config_tarification_dynamique.json"


def get_config_etendue():
    """
    Retourne un dictionnaire fusionné : config de base (m01) + config étendue (JSON si présent).
    Si config_tarification_dynamique.json n'existe pas, retourne uniquement la config m01.
    """
    from m01_config import get_config
    base = get_config()
    if not FICHIER_CONFIG_ETENDUE.exists():
        return dict(base)
    try:
        with open(FICHIER_CONFIG_ETENDUE, "r", encoding="utf-8") as f:
            etendue = json.load(f)
    except (json.JSONDecodeError, IOError):
        return dict(base)
    # Fusion : base puis clés du JSON (les clés du JSON écrasent en cas de conflit)
    out = dict(base)
    out.update(etendue)
    return out
