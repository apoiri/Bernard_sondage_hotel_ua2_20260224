# -*- coding: utf-8 -*-
"""
Module 5 – Variable Type_Forfait (pour Khi-deux)
Simulation « L'Hôtel Boutique Art de Vivre »
Reçoit le DataFrame du Module 4. Ajoute Type_Forfait : « Forfait Gastronomique » ou « Chambre Seule »
selon les probabilités par segment (Loisirs 80 % Forfait, Congressiste 90 % Chambre Seule, etc.).
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
# Probabilité « Forfait Gastronomique » par segment (sinon « Chambre Seule »).
# Ordre : Affaires_Solo, Congressiste, Loisirs_Couple, Local_Gourmet, Local_Spa

PROBA_FORFAIT_GASTRONOMIQUE = [0.30, 0.10, 0.80, 0.50, 0.20]  # Loisirs 80 %, Congressiste 10 %
GRAINE_ALEATOIRE = 42

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m01_config import get_config


def _print_hypotheses():
    """Affiche les hypothèses utilisées."""
    c = get_config()
    seg = c["SEGMENTS_NOMS"]
    print("=" * 60)
    print("HYPOTHÈSES MODULE 5 (Type_Forfait – Khi-deux)")
    print("=" * 60)
    for i, s in enumerate(seg):
        p = PROBA_FORFAIT_GASTRONOMIQUE[i]
        print(f"  {s}: P(Forfait Gastronomique) = {p:.0%}  →  P(Chambre Seule) = {1-p:.0%}")
    print(f"  Graine aléatoire = {GRAINE_ALEATOIRE}")
    print("=" * 60)


def run(df):
    """
    Ajoute la colonne Type_Forfait au DataFrame (sortie Module 4).
    Retourne le même DataFrame avec une colonne en plus.
    """
    c = get_config()
    np.random.seed(GRAINE_ALEATOIRE)
    seg_noms = c["SEGMENTS_NOMS"]
    seg_to_idx = {s: i for i, s in enumerate(seg_noms)}
    probas = PROBA_FORFAIT_GASTRONOMIQUE

    n = len(df)
    segments = df["Segment"].values
    type_forfait = np.empty(n, dtype=object)
    for i in range(n):
        idx = seg_to_idx[segments[i]]
        if np.random.random() < probas[idx]:
            type_forfait[i] = "Forfait Gastronomique"
        else:
            type_forfait[i] = "Chambre Seule"

    df = df.copy()
    df["Type_Forfait"] = type_forfait
    return df


if __name__ == "__main__":
    _print_hypotheses()
    import m02_segments
    import m03_nuits_chambre
    import m04_revenus_centres_profit
    df = m02_segments.run()
    df = m03_nuits_chambre.run(df)
    df = m04_revenus_centres_profit.run(df)
    df = run(df)
    print(f"DataFrame : {len(df)} lignes")
    print(df[["Segment", "Type_Forfait"]].head(10).to_string())
    print("\nTableau croisé Segment × Type_Forfait (pour Khi-deux):")
    ct = pd.crosstab(df["Segment"], df["Type_Forfait"])
    print(ct.to_string())
    print("\n% Forfait Gastronomique par segment:")
    pct = df.groupby("Segment")["Type_Forfait"].apply(
        lambda x: (x == "Forfait Gastronomique").mean() * 100
    ).round(1)
    print(pct.to_string())
