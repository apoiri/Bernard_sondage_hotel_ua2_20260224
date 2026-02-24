# -*- coding: utf-8 -*-
"""
Module 7 – Total_Facture (modèle de régression)
Simulation « L'Hôtel Boutique Art de Vivre »
Reçoit le DataFrame du Module 6. Ajoute Total_Facture.
Total_Facture = Rev_Chambre + 1,1×Rev_Resto + 1,3×Rev_Spa + ε (ε petit bruit).
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
COEFF_REV_RESTO = 1.1
COEFF_REV_SPA = 1.3
ECART_TYPE_BRUIT_TOTAL = 10.0   # Écart-type du bruit ε
GRAINE_ALEATOIRE = 42

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m01_config import get_config


def _print_hypotheses():
    """Affiche les hypothèses utilisées."""
    print("=" * 60)
    print("HYPOTHÈSES MODULE 7 (Total_Facture)")
    print("=" * 60)
    print(f"  Formule : Total_Facture = Rev_Chambre + {COEFF_REV_RESTO}×Rev_Resto + {COEFF_REV_SPA}×Rev_Spa + ε")
    print(f"  ε ~ N(0, {ECART_TYPE_BRUIT_TOTAL})")
    print(f"  Graine aléatoire = {GRAINE_ALEATOIRE}")
    print("=" * 60)


def run(df):
    """
    Ajoute la colonne Total_Facture au DataFrame (sortie Module 6).
    Retourne le même DataFrame avec une colonne en plus.
    """
    np.random.seed(GRAINE_ALEATOIRE)
    n = len(df)
    rev_chambre = df["Rev_Chambre"].values
    rev_resto = df["Rev_Resto"].values
    rev_spa = df["Rev_Spa"].values
    epsilon = np.random.normal(0, ECART_TYPE_BRUIT_TOTAL, size=n)
    total = rev_chambre + COEFF_REV_RESTO * rev_resto + COEFF_REV_SPA * rev_spa + epsilon
    total = np.maximum(total, 0.0)   # pas de facture négative
    df = df.copy()
    df["Total_Facture"] = total
    return df


if __name__ == "__main__":
    _print_hypotheses()
    import m02_segments
    import m03_nuits_chambre
    import m04_revenus_centres_profit
    import m05_type_forfait
    import m06_satisfaction_nps
    df = m02_segments.run()
    df = m03_nuits_chambre.run(df)
    df = m04_revenus_centres_profit.run(df)
    df = m05_type_forfait.run(df)
    df = m06_satisfaction_nps.run(df)
    df = run(df)
    print(f"DataFrame : {len(df)} lignes")
    cols = ["Rev_Chambre", "Rev_Resto", "Rev_Spa", "Total_Facture"]
    print(df[cols].head(10).to_string())
    print("\nStatistiques Total_Facture:")
    print(df["Total_Facture"].describe().to_string())
    # Vérification rapide : Total_Facture ≈ Rev_Chambre + 1.1*Rev_Resto + 1.3*Rev_Spa
    attendu = df["Rev_Chambre"] + COEFF_REV_RESTO * df["Rev_Resto"] + COEFF_REV_SPA * df["Rev_Spa"]
    diff = (df["Total_Facture"] - attendu).describe()
    print("\nDifférence (Total_Facture - formule sans ε) – doit être proche de 0 en moyenne:")
    print(diff.to_string())
