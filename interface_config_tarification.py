# -*- coding: utf-8 -*-
"""
Interface – Génération de config_tarification_dynamique.json
Simulation « L'Hôtel Boutique Art de Vivre »

Script en ligne de commande : écrit le fichier JSON de config étendue
(types de chambre, 12 taux d'occupation, sexe, revenus, pays/provinces/villes).
Ne modifie aucun module m00, m02b, m02c, m02d, m03b.
"""

import json
import sys
from pathlib import Path

REP_PROJET = Path(__file__).resolve().parent
FICHIER_EXEMPLE = REP_PROJET / "config_tarification_dynamique_exemple.json"
FICHIER_SORTIE = REP_PROJET / "config_tarification_dynamique.json"

# Config par défaut (utilisée si le fichier exemple est absent)
CONFIG_DEFAUT = {
    "types_chambre": [
        {"nom": "Standard", "nb_chambres": 35, "prix_base": 180},
        {"nom": "Supérieure", "nb_chambres": 25, "prix_base": 280},
        {"nom": "Confort", "nb_chambres": 20, "prix_base": 350},
        {"nom": "Luxe", "nb_chambres": 12, "prix_base": 420},
        {"nom": "Suite", "nb_chambres": 8, "prix_base": 550},
    ],
    "taux_occupation_mois": [0.55, 0.52, 0.58, 0.62, 0.68, 0.75, 0.88, 0.85, 0.72, 0.65, 0.6, 0.58],
    "repartition_sexe": {"M": 0.48, "F": 0.5, "Autre": 0.02},
    "plages_revenus": [
        {"libelle": "Faible", "min": 0, "max": 40000},
        {"libelle": "Moyen", "min": 40000, "max": 80000},
        {"libelle": "Élevé", "min": 80000, "max": 200000},
    ],
    "pays": [
        {"code": "CA", "nom": "Canada", "poids": 0.45},
        {"code": "US", "nom": "États-Unis", "poids": 0.35},
        {"code": "EU", "nom": "Europe", "poids": 0.15},
        {"code": "Autre", "nom": "Autre", "poids": 0.05},
    ],
    "provinces_par_pays": {
        "CA": [{"code": "QC", "nom": "Québec", "poids": 0.5}, {"code": "ON", "nom": "Ontario", "poids": 0.35}, {"code": "Autre", "nom": "Autre", "poids": 0.15}],
        "US": [{"code": "NY", "nom": "New York", "poids": 0.4}, {"code": "CA", "nom": "California", "poids": 0.3}, {"code": "Autre", "nom": "Autre", "poids": 0.3}],
        "EU": [{"code": "FR", "nom": "France", "poids": 0.5}, {"code": "Autre", "nom": "Autre", "poids": 0.5}],
        "Autre": [{"code": "XX", "nom": "—", "poids": 1}],
    },
    "villes_exemples": {
        "QC": ["Montréal", "Québec", "Laval", "Gatineau"],
        "ON": ["Toronto", "Ottawa", "Mississauga"],
        "NY": ["New York", "Buffalo", "Rochester"],
        "FR": ["Paris", "Lyon", "Marseille"],
    },
}


def charger_config():
    """Charge la config (exemple ou défaut)."""
    if FICHIER_EXEMPLE.exists():
        with open(FICHIER_EXEMPLE, "r", encoding="utf-8") as f:
            return json.load(f)
    return dict(CONFIG_DEFAUT)


def ecrire_config(config, path=None):
    """Écrit la config en JSON (indent pour lisibilité)."""
    path = path or FICHIER_SORTIE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    return path


def mode_interactif():
    """Saisie simplifiée : types chambre, 12 taux, puis écrit le reste par défaut."""
    config = charger_config()
    print("=== Saisie simplifiée (entrée = garder la valeur par défaut) ===\n")

    # Types de chambre
    types = config.get("types_chambre", CONFIG_DEFAUT["types_chambre"])
    print("Types de chambre actuels:", [t["nom"] for t in types])
    rep = input("Modifier les types de chambre ? (o/n) [n]: ").strip().lower() or "n"
    if rep == "o":
        n = int(input("Nombre de types [3]: ").strip() or "3")
        types = []
        for i in range(n):
            nom = input(f"  Type {i+1} nom [Standard]: ").strip() or "Standard"
            nb = int(input(f"  Type {i+1} nb_chambres [50]: ").strip() or "50")
            prix = float(input(f"  Type {i+1} prix_base [180]: ").strip() or "180")
            types.append({"nom": nom, "nb_chambres": nb, "prix_base": prix})
        config["types_chambre"] = types

    # 12 taux
    taux = config.get("taux_occupation_mois", CONFIG_DEFAUT["taux_occupation_mois"])
    print("\n12 taux d'occupation (janvier à décembre) actuels:", [round(t, 2) for t in taux])
    rep = input("Modifier les 12 taux ? (o/n) [n]: ").strip().lower() or "n"
    if rep == "o":
        mois_noms = ["janv", "fév", "mar", "avr", "mai", "juin", "juil", "août", "sept", "oct", "nov", "déc"]
        taux = []
        for i, m in enumerate(mois_noms):
            v = input(f"  {m} [{(CONFIG_DEFAUT['taux_occupation_mois'][i])}]: ").strip()
            taux.append(float(v) if v else CONFIG_DEFAUT["taux_occupation_mois"][i])
        config["taux_occupation_mois"] = taux

    return config


def main():
    interactif = "--interactif" in sys.argv or "-i" in sys.argv
    if interactif:
        config = mode_interactif()
    else:
        config = charger_config()
        print("Utilisation du fichier exemple ou de la config par défaut.")
        print("Pour une saisie pas à pas : python3 interface_config_tarification.py --interactif")
    path = ecrire_config(config)
    print(f"Fichier écrit : {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
