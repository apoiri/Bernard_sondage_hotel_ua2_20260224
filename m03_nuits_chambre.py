# -*- coding: utf-8 -*-
"""
Module 3 – Nuits et Rev_Chambre
Simulation « L'Hôtel Boutique Art de Vivre »
Reçoit le DataFrame du Module 2. Ajoute Nuits et Rev_Chambre.
- Nuits : 0 si Externe ou Annulee = Oui ; sinon Poisson(λ), borné [min, max].
- Rev_Chambre : 0 si Externe ou Annulee = Oui ; sinon Nuits × tarif (Basse ou Haute).
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
# Les valeurs par défaut viennent du Module 1 (m01_config). Surcharges optionnelles ici.

LAMBDA_POISSON_NUITS = 2.5    # Moyenne du nombre de nuits (séjour interne)
MIN_NUITS = 1                 # Minimum de nuits (interne)
MAX_NUITS = 14                # Maximum de nuits (interne)
TARIF_CHAMBRE_BASSE = 200     # $/nuit en saison Basse
TARIF_CHAMBRE_HAUTE = 350     # $/nuit en saison Haute
GRAINE_ALEATOIRE = 42         # Reproductibilité (doit être cohérent avec Module 2 si enchaînement)

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m01_config import get_config


def _print_hypotheses():
    """Affiche les hypothèses utilisées."""
    c = get_config()
    print("=" * 60)
    print("HYPOTHÈSES MODULE 3 (Nuits, Rev_Chambre)")
    print("=" * 60)
    print(f"  λ Poisson (nuits)     = {LAMBDA_POISSON_NUITS} (config: {c['LAMBDA_POISSON_NUITS']})")
    print(f"  Min / Max nuits       = {MIN_NUITS} / {MAX_NUITS}")
    print(f"  Tarif chambre Basse   = {TARIF_CHAMBRE_BASSE} $/nuit")
    print(f"  Tarif chambre Haute   = {TARIF_CHAMBRE_HAUTE} $/nuit")
    print(f"  Nuits = 0 si Externe ou Annulee = Oui")
    print("=" * 60)


def run(df):
    """
    Ajoute les colonnes Nuits et Rev_Chambre au DataFrame (sortie Module 2).
    Retourne le même DataFrame avec deux colonnes en plus.
    """
    np.random.seed(GRAINE_ALEATOIRE)
    n = len(df)
    externe = (df["Type_Client"] == "Externe").values
    annulee = (df["Annulee"] == "Oui").values
    saison = df["Saison"].values

    # Nuits : 0 si Externe ou Annulée ; sinon Poisson borné
    nuits = np.zeros(n, dtype=int)
    mask_interne_non_annule = ~externe & ~annulee
    n_interne = mask_interne_non_annule.sum()
    if n_interne > 0:
        tirage = np.random.poisson(LAMBDA_POISSON_NUITS, size=n_interne)
        tirage = np.clip(tirage, MIN_NUITS, MAX_NUITS)
        nuits[mask_interne_non_annule] = tirage

    # Rev_Chambre : 0 si Externe ou Annulée ; sinon Nuits × tarif
    rev_chambre = np.zeros(n, dtype=float)
    tarif_basse = TARIF_CHAMBRE_BASSE
    tarif_haute = TARIF_CHAMBRE_HAUTE
    for i in range(n):
        if mask_interne_non_annule[i]:
            tarif = tarif_basse if saison[i] == "Basse" else tarif_haute
            rev_chambre[i] = nuits[i] * tarif

    df = df.copy()
    df["Nuits"] = nuits
    df["Rev_Chambre"] = rev_chambre
    return df


if __name__ == "__main__":
    _print_hypotheses()
    import m02_segments
    df = m02_segments.run()
    df = run(df)
    print(f"DataFrame : {len(df)} lignes, colonnes : {list(df.columns)}")
    print(df[["ID_Client", "Type_Client", "Annulee", "Saison", "Nuits", "Rev_Chambre"]].head(12).to_string())
    print("\nStatistiques Nuits (Interne, Non annulée uniquement):")
    mask = (df["Type_Client"] == "Interne") & (df["Annulee"] == "Non")
    print(df.loc[mask, "Nuits"].describe().to_string())
    print("\nStatistiques Rev_Chambre (idem):")
    print(df.loc[mask, "Rev_Chambre"].describe().to_string())
