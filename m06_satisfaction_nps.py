# -*- coding: utf-8 -*-
"""
Module 6 – Satisfaction NPS avec corrélation Rev_Spa
Simulation « L'Hôtel Boutique Art de Vivre »
Reçoit le DataFrame du Module 5. Ajoute Satisfaction_NPS.
- Si Annulee = Oui : NPS = NaN (pas de sondage).
- Sinon : NPS = 8 - 1,5×Haute + 1,0×(Rev_Spa>100) + bruit, puis composante corrélée à Rev_Spa (r ≈ 0,75), borné 0–10.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
NPS_CONSTANTE = 8.0
NPS_EFFET_HAUTE_SAISON = -1.5
NPS_EFFET_REV_SPA_SUP_100 = 1.0
NPS_ECART_TYPE_BRUIT = 0.5
NPS_CORRELATION_REV_SPA = 0.75   # Cible : corrélation Pearson avec Rev_Spa (observée ≈ 0,75)
NPS_R_ALPHA = 0.68               # Paramètre interne pour atteindre r observé ≈ 0,75 (réduire si r > 0,75)
GRAINE_ALEATOIRE = 42

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m01_config import get_config


def _print_hypotheses():
    """Affiche les hypothèses utilisées."""
    print("=" * 60)
    print("HYPOTHÈSES MODULE 6 (Satisfaction NPS)")
    print("=" * 60)
    print(f"  Formule de base : NPS = {NPS_CONSTANTE} + ({NPS_EFFET_HAUTE_SAISON})×Haute + ({NPS_EFFET_REV_SPA_SUP_100})×(Rev_Spa>100) + N(0, {NPS_ECART_TYPE_BRUIT})")
    print(f"  Corrélation cible Rev_Spa–NPS : r ≈ {NPS_CORRELATION_REV_SPA}")
    print(f"  Si Annulee = Oui : NPS = NaN")
    print(f"  Graine aléatoire = {GRAINE_ALEATOIRE}")
    print("=" * 60)


def run(df):
    """
    Ajoute la colonne Satisfaction_NPS au DataFrame (sortie Module 5).
    Retourne le même DataFrame avec une colonne en plus.
    """
    np.random.seed(GRAINE_ALEATOIRE)
    n = len(df)
    annulee = (df["Annulee"] == "Oui").values
    saison = df["Saison"].values
    rev_spa = df["Rev_Spa"].values.copy()

    satisfaction = np.full(n, np.nan, dtype=float)
    mask = ~annulee
    idx_actif = np.where(mask)[0]
    if len(idx_actif) == 0:
        df = df.copy()
        df["Satisfaction_NPS"] = satisfaction
        return df

    rev_spa_actif = rev_spa[mask]
    mean_spa = np.mean(rev_spa_actif)
    std_spa = np.std(rev_spa_actif)
    if std_spa < 1e-6:
        std_spa = 1.0

    # Formule de base (indépendante de Rev_Spa continu, sauf I(Rev_Spa>100))
    base = NPS_CONSTANTE + (NPS_EFFET_HAUTE_SAISON * (saison[mask] == "Haute")) + (NPS_EFFET_REV_SPA_SUP_100 * (rev_spa_actif > 100)) + np.random.normal(0, NPS_ECART_TYPE_BRUIT, size=mask.sum())
    std_base = np.std(base)
    if std_base < 1e-6:
        std_base = 1.0

    # Composante corrélée à Rev_Spa : NPS = base + alpha * (Rev_Spa - mean_spa)/std_spa
    # Ajuster NPS_R_ALPHA pour que la corrélation observée soit proche de NPS_CORRELATION_REV_SPA
    r = NPS_R_ALPHA
    alpha = r * std_base / np.sqrt(1 - r * r) if r < 1 else std_base * 2
    z_spa = (rev_spa_actif - mean_spa) / std_spa
    nps_actif = base + alpha * z_spa
    nps_actif = np.clip(nps_actif, 0, 10)
    satisfaction[mask] = nps_actif

    df = df.copy()
    df["Satisfaction_NPS"] = satisfaction
    return df


if __name__ == "__main__":
    _print_hypotheses()
    import m02_segments
    import m03_nuits_chambre
    import m04_revenus_centres_profit
    import m05_type_forfait
    df = m02_segments.run()
    df = m03_nuits_chambre.run(df)
    df = m04_revenus_centres_profit.run(df)
    df = m05_type_forfait.run(df)
    df = run(df)
    print(f"DataFrame : {len(df)} lignes")
    print(df[["Annulee", "Rev_Spa", "Satisfaction_NPS"]].head(12).to_string())

    mask = df["Annulee"] == "Non"
    valid = df.loc[mask, ["Rev_Spa", "Satisfaction_NPS"]].dropna()
    if len(valid) >= 2:
        r_obs = valid["Rev_Spa"].corr(valid["Satisfaction_NPS"])
        print(f"\nCorrélation Pearson Rev_Spa – Satisfaction_NPS (Annulee=Non) : r = {r_obs:.3f} (cible ≈ {NPS_CORRELATION_REV_SPA})")
    print("\nStatistiques Satisfaction_NPS (Annulee=Non):")
    print(df.loc[mask, "Satisfaction_NPS"].describe().to_string())

# ========== RÈGLE DE BLOCAGE ==========
# Aucune modification de ce module n'est acceptée sans l'autorisation du maître d'ouvrage du projet.
