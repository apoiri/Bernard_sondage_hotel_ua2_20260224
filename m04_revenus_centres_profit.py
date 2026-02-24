# -*- coding: utf-8 -*-
"""
Module 4 – Rev_Banquet, Rev_Resto, Rev_Spa (revenus par segment)
Simulation « L'Hôtel Boutique Art de Vivre »
Reçoit le DataFrame du Module 3. Ajoute Rev_Banquet, Rev_Resto, Rev_Spa.
- Si Annulee = Oui : les trois = 0.
- Sinon : Rev_Banquet = Gamma(k, θ) si Congressiste, 0 sinon ; Rev_Resto et Rev_Spa selon moyennes par segment + bruit.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
# Les valeurs par défaut viennent du Module 1 (m01_config). Surcharges optionnelles ici.

GAMMA_BANQUET_K = 2
GAMMA_BANQUET_THETA = 200
# Moyennes Rev_Resto par segment (Affaires_Solo, Congressiste, Loisirs_Couple, Local_Gourmet, Local_Spa)
MOYENNES_REV_RESTO = [60, 45, 80, 150, 20]
# Moyennes Rev_Spa par segment
MOYENNES_REV_SPA = [0, 0, 180, 0, 120]
# Écart-type du bruit (autour des moyennes) pour garder ANOVA p < 0,05
ECART_TYPE_BRUIT_RESTO = 18
ECART_TYPE_BRUIT_SPA = 25
GRAINE_ALEATOIRE = 42

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m01_config import get_config


def _print_hypotheses():
    """Affiche les hypothèses utilisées."""
    c = get_config()
    print("=" * 60)
    print("HYPOTHÈSES MODULE 4 (Rev_Banquet, Rev_Resto, Rev_Spa)")
    print("=" * 60)
    print(f"  Gamma Banquet (Congressiste) : k={GAMMA_BANQUET_K}, θ={GAMMA_BANQUET_THETA}")
    print(f"  Moyennes Rev_Resto par segment = {MOYENNES_REV_RESTO}")
    print(f"  Moyennes Rev_Spa par segment    = {MOYENNES_REV_SPA}")
    print(f"  σ bruit Resto = {ECART_TYPE_BRUIT_RESTO} ; Spa = {ECART_TYPE_BRUIT_SPA}")
    print(f"  Si Annulee = Oui : Rev_Banquet, Rev_Resto, Rev_Spa = 0")
    print("=" * 60)


def run(df):
    """
    Ajoute les colonnes Rev_Banquet, Rev_Resto, Rev_Spa au DataFrame (sortie Module 3).
    Retourne le même DataFrame avec trois colonnes en plus.
    """
    c = get_config()
    np.random.seed(GRAINE_ALEATOIRE)
    n = len(df)
    annulee = (df["Annulee"] == "Oui").values
    segments = df["Segment"].values
    seg_noms = c["SEGMENTS_NOMS"]
    seg_to_idx = {s: i for i, s in enumerate(seg_noms)}

    rev_banquet = np.zeros(n)
    rev_resto = np.zeros(n)
    rev_spa = np.zeros(n)

    mask_actif = ~annulee
    for i in range(n):
        if not mask_actif[i]:
            continue
        idx_seg = seg_to_idx[segments[i]]

        # Rev_Banquet : Gamma(k, θ) si Congressiste (idx 1), sinon 0
        if segments[i] == "Congressiste":
            rev_banquet[i] = np.random.gamma(GAMMA_BANQUET_K, GAMMA_BANQUET_THETA)
        else:
            rev_banquet[i] = 0.0

        # Rev_Resto : moyenne segment + bruit normal, min 0
        mu_r = MOYENNES_REV_RESTO[idx_seg]
        rev_resto[i] = max(0, mu_r + np.random.normal(0, ECART_TYPE_BRUIT_RESTO))

        # Rev_Spa : moyenne segment + bruit normal, min 0
        mu_s = MOYENNES_REV_SPA[idx_seg]
        rev_spa[i] = max(0, mu_s + np.random.normal(0, ECART_TYPE_BRUIT_SPA))

    df = df.copy()
    df["Rev_Banquet"] = rev_banquet
    df["Rev_Resto"] = rev_resto
    df["Rev_Spa"] = rev_spa
    return df


if __name__ == "__main__":
    _print_hypotheses()
    import m02_segments
    import m03_nuits_chambre
    df = m02_segments.run()
    df = m03_nuits_chambre.run(df)
    df = run(df)
    print(f"DataFrame : {len(df)} lignes")
    print(df[["Segment", "Annulee", "Rev_Banquet", "Rev_Resto", "Rev_Spa"]].head(10).to_string())

    # Vérification ANOVA Rev_Resto par segment (doit donner p < 0,05)
    mask = df["Annulee"] == "Non"
    groups = [df.loc[mask & (df["Segment"] == s), "Rev_Resto"].values for s in df["Segment"].unique()]
    groups = [g for g in groups if len(g) >= 2]
    if len(groups) >= 2:
        f_val, p_val = stats.f_oneway(*groups)
        print(f"\nANOVA Rev_Resto par Segment (Annulee=Non) : F={f_val:.2f}, p={p_val:.4f} {'OK' if p_val < 0.05 else 'À vérifier'}")

    print("\nMoyennes Rev_Resto par segment (Annulee=Non):")
    print(df.loc[mask].groupby("Segment")["Rev_Resto"].agg(["mean", "count"]).round(2).to_string())
    print("\nMoyennes Rev_Spa par segment (Annulee=Non):")
    print(df.loc[mask].groupby("Segment")["Rev_Spa"].agg(["mean", "count"]).round(2).to_string())
