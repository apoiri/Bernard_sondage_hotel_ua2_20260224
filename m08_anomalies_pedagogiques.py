# -*- coding: utf-8 -*-
"""
Module 8 – Anomalies pédagogiques (data cleaning à détecter)
Simulation « L'Hôtel Boutique Art de Vivre »
Reçoit le DataFrame du Module 7. Applique les anomalies volontaires pour l'exercice de nettoyage.
1. Incohérence : 15 Externes avec Nuits > 0
2. Outliers : 3 Satisfaction_NPS = 99 (erreur de saisie)
3. Valeurs manquantes : 5 % dans Rev_Spa et Rev_Resto
4. Doublons : 10 lignes dupliquées (total = N_RESERVATIONS + 10)
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
N_INCOHERENCES_EXTERNES_NUITS = 15   # Externes avec Nuits > 0 (incohérence logique)
N_OUTLIERS_NPS = 3                   # Lignes avec Satisfaction_NPS = 99 (erreur de saisie)
PCT_MANQUANTS = 0.05                 # 5 % de cellules vides dans Rev_Spa et Rev_Resto
N_DOUBLONS = 10                      # Nombre de lignes à dupliquer
GRAINE_ALEATOIRE = 42

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m01_config import get_config


def _print_hypotheses():
    """Affiche les hypothèses utilisées."""
    print("=" * 60)
    print("HYPOTHÈSES MODULE 8 (Anomalies pédagogiques)")
    print("=" * 60)
    print(f"  Incohérence logique : {N_INCOHERENCES_EXTERNES_NUITS} Externes avec Nuits > 0")
    print(f"  Outliers NPS         : {N_OUTLIERS_NPS} lignes avec Satisfaction_NPS = 99")
    print(f"  Valeurs manquantes   : {PCT_MANQUANTS*100:.0f} % dans Rev_Spa et Rev_Resto (chaque colonne)")
    print(f"  Doublons             : {N_DOUBLONS} lignes dupliquées")
    print(f"  Graine aléatoire     = {GRAINE_ALEATOIRE}")
    print("=" * 60)


def run(df):
    """
    Applique les anomalies pédagogiques au DataFrame (sortie Module 7).
    Retourne le DataFrame modifié (plus 10 lignes dupliquées).
    """
    c = get_config()
    np.random.seed(GRAINE_ALEATOIRE)
    df = df.copy()
    n = len(df)

    # 1. Incohérence logique : 15 Externes avec Nuits > 0
    idx_externes = np.where(df["Type_Client"] == "Externe")[0]
    if len(idx_externes) >= N_INCOHERENCES_EXTERNES_NUITS:
        choix = np.random.choice(idx_externes, size=N_INCOHERENCES_EXTERNES_NUITS, replace=False)
        df.loc[df.index[choix], "Nuits"] = np.random.randint(1, 5, size=N_INCOHERENCES_EXTERNES_NUITS)

    # 2. Outliers : 3 Satisfaction_NPS = 99 (sur lignes où NPS existe, i.e. Non annulée)
    idx_avec_nps = df["Satisfaction_NPS"].notna()
    idx_nps_valides = np.where(idx_avec_nps)[0]
    if len(idx_nps_valides) >= N_OUTLIERS_NPS:
        choix_nps = np.random.choice(idx_nps_valides, size=N_OUTLIERS_NPS, replace=False)
        df.loc[df.index[choix_nps], "Satisfaction_NPS"] = 99

    # 3. Valeurs manquantes : 5 % dans Rev_Spa et Rev_Resto (chaque colonne indépendamment)
    n_manquants = max(1, int(n * PCT_MANQUANTS))
    idx_rev_spa = np.random.choice(n, size=min(n_manquants, n), replace=False)
    idx_rev_resto = np.random.choice(n, size=min(n_manquants, n), replace=False)
    df.iloc[idx_rev_spa, df.columns.get_loc("Rev_Spa")] = np.nan
    df.iloc[idx_rev_resto, df.columns.get_loc("Rev_Resto")] = np.nan

    # 4. Doublons : ajouter 10 lignes dupliquées
    idx_doublons = np.random.choice(n, size=N_DOUBLONS, replace=True)
    df_dup = df.iloc[idx_doublons].copy()
    df = pd.concat([df, df_dup], ignore_index=True)

    return df


if __name__ == "__main__":
    _print_hypotheses()
    import m02_segments
    import m03_nuits_chambre
    import m04_revenus_centres_profit
    import m05_type_forfait
    import m06_satisfaction_nps
    import m07_total_facture
    df = m02_segments.run()
    df = m03_nuits_chambre.run(df)
    df = m04_revenus_centres_profit.run(df)
    df = m05_type_forfait.run(df)
    df = m06_satisfaction_nps.run(df)
    df = m07_total_facture.run(df)
    df = run(df)
    print(f"DataFrame après anomalies : {len(df)} lignes (attendu : {get_config()['N_RESERVATIONS']} + {N_DOUBLONS})")
    # Vérifications
    incoh = ((df["Type_Client"] == "Externe") & (df["Nuits"] > 0)).sum()
    nps99 = (df["Satisfaction_NPS"] == 99).sum()
    manq_spa = df["Rev_Spa"].isna().sum()
    manq_resto = df["Rev_Resto"].isna().sum()
    print(f"  Externes avec Nuits > 0 : {incoh} (attendu {N_INCOHERENCES_EXTERNES_NUITS})")
    print(f"  Satisfaction_NPS = 99   : {nps99} (attendu {N_OUTLIERS_NPS})")
    print(f"  Manquants Rev_Spa       : {manq_spa} (~{PCT_MANQUANTS*100:.0f} %)")
    print(f"  Manquants Rev_Resto     : {manq_resto} (~{PCT_MANQUANTS*100:.0f} %)")
    print(f"  Doublons (lignes en plus): {len(df) - get_config()['N_RESERVATIONS']} (attendu {N_DOUBLONS})")
