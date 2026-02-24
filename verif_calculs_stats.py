# -*- coding: utf-8 -*-
"""
Vérification indépendante des calculs statistiques du rapport de validation.
Lit le CSV, recalcule les mêmes indicateurs (sans utiliser m10), affiche les résultats
pour comparaison avec rapport_validation_sondage_hotel.xlsx ou la sortie de m10.

Usage : python3 verif_calculs_stats.py [chemin_sondage_hotel_data.csv]
        Si aucun chemin n'est donné, utilise sondage_hotel_data.csv dans le dossier du script.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REP = Path(__file__).resolve().parent
FICHIER_CSV_DEFAUT = REP / "sondage_hotel_data.csv"
SEP = ";"


def ic_proportion(p, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    rad = z * np.sqrt(p * (1 - p) / n)
    return max(0, p - rad), min(1, p + rad)


def main():
    chemin_csv = Path(sys.argv[1]) if len(sys.argv) > 1 else FICHIER_CSV_DEFAUT
    if not chemin_csv.exists():
        print(f"Fichier introuvable : {chemin_csv}")
        sys.exit(1)

    df = pd.read_csv(chemin_csv, sep=SEP, encoding="utf-8-sig", decimal=".")
    n_total = len(df)
    mask_non_annule = df["Annulee"] == "Non"

    print("=" * 60)
    print("VÉRIFICATION INDÉPENDANTE DES CALCULS (à comparer au rapport)")
    print("=" * 60)
    print(f"Source : {chemin_csv}  ({n_total} lignes)\n")

    # --- Proportions + IC ---
    p_annule = (df["Annulee"] == "Oui").mean()
    ic_annule = ic_proportion(p_annule, n_total)
    p_spa = ((df["Rev_Spa"] > 0) & df["Rev_Spa"].notna()).mean()
    ic_spa = ic_proportion(p_spa, n_total)
    p_forfait = (df["Type_Forfait"] == "Forfait Gastronomique").mean()
    ic_forfait = ic_proportion(p_forfait, n_total)
    print("--- Proportions et IC 95 % ---")
    print(f"  % Annulées     : {p_annule*100:.4f} %  IC : [{ic_annule[0]*100:.4f} % ; {ic_annule[1]*100:.4f} %]")
    print(f"  % Rev_Spa > 0  : {p_spa*100:.4f} %  IC : [{ic_spa[0]*100:.4f} % ; {ic_spa[1]*100:.4f} %]")
    print(f"  % Forfait Gast.: {p_forfait*100:.4f} %  IC : [{ic_forfait[0]*100:.4f} % ; {ic_forfait[1]*100:.4f} %]")

    # --- Khi-deux ---
    ct = pd.crosstab(df["Segment"], df["Type_Forfait"])
    chi2, p_chi2, ddl, expected = stats.chi2_contingency(ct)
    print("\n--- Khi-deux (Segment × Type_Forfait) ---")
    print(f"  Khi² = {chi2:.4f}  ddl = {ddl}  p-value = {p_chi2:.6f}")

    # --- Pearson ---
    sub = df.loc[mask_non_annule, ["Rev_Spa", "Satisfaction_NPS"]].dropna()
    if len(sub) >= 2:
        r_pearson, p_pearson = stats.pearsonr(sub["Rev_Spa"], sub["Satisfaction_NPS"])
    else:
        r_pearson, p_pearson = np.nan, np.nan
    print("\n--- Pearson (Rev_Spa × Satisfaction_NPS, non annulées) ---")
    print(f"  r = {r_pearson:.6f}  p-value = {p_pearson:.6f}  n = {len(sub)}")

    # --- ANOVA ---
    groups = [
        df.loc[mask_non_annule & (df["Segment"] == s), "Rev_Resto"].dropna().values
        for s in df["Segment"].unique()
    ]
    groups = [g for g in groups if len(g) >= 2]
    if len(groups) >= 2:
        f_anova, p_anova = stats.f_oneway(*groups)
    else:
        f_anova, p_anova = np.nan, np.nan
    print("\n--- ANOVA (Rev_Resto par Segment, non annulées) ---")
    print(f"  F = {f_anova:.6f}  p-value = {p_anova:.6f}")

    # --- Régression ---
    reg_df = df[["Total_Facture", "Rev_Chambre", "Rev_Resto", "Rev_Spa"]].dropna()
    if len(reg_df) >= 4:
        y = reg_df["Total_Facture"].values
        X = reg_df[["Rev_Chambre", "Rev_Resto", "Rev_Spa"]].values
        X1 = np.column_stack([np.ones(len(X)), X])
        beta, _, _, _ = np.linalg.lstsq(X1, y, rcond=None)
        y_pred = X1 @ beta
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        print("\n--- Régression (Total_Facture ~ Rev_Chambre + Rev_Resto + Rev_Spa) ---")
        print(f"  Constante = {beta[0]:.6f}  Rev_Chambre = {beta[1]:.6f}  Rev_Resto = {beta[2]:.6f}  Rev_Spa = {beta[3]:.6f}")
        print(f"  R² = {r2:.6f}  n = {len(reg_df)}")
    else:
        print("\n--- Régression : données insuffisantes ---")

    # --- Annulations par canal ---
    n_direct = (df["Type_canal"] == "Direct").sum()
    n_direct_annule = ((df["Type_canal"] == "Direct") & (df["Annulee"] == "Oui")).sum()
    n_inter = (df["Type_canal"] == "Intermediaire").sum()
    n_inter_annule = ((df["Type_canal"] == "Intermediaire") & (df["Annulee"] == "Oui")).sum()
    taux_direct = n_direct_annule / n_direct if n_direct > 0 else np.nan
    taux_inter = n_inter_annule / n_inter if n_inter > 0 else np.nan
    print("\n--- Annulations par canal ---")
    print(f"  Taux Direct       : {taux_direct*100:.4f} %  (n_direct = {n_direct})")
    print(f"  Taux Intermédiaire: {taux_inter*100:.4f} %  (n_inter = {n_inter})")

    # --- Qualité ---
    incoh = ((df["Type_Client"] == "Externe") & (df["Nuits"] > 0)).sum()
    nps99 = (df["Satisfaction_NPS"] == 99).sum()
    manq_spa = df["Rev_Spa"].isna().sum()
    manq_resto = df["Rev_Resto"].isna().sum()
    n_unique = df.drop_duplicates().shape[0]
    doublons = n_total - n_unique
    print("\n--- Qualité (anomalies pédagogiques) ---")
    print(f"  Externes Nuits>0 : {incoh}  |  NPS=99 : {nps99}  |  Manquants Rev_Spa : {manq_spa}  Rev_Resto : {manq_resto}  |  Doublons : {doublons}")

    print("\n" + "=" * 60)
    print("Comparez ces valeurs à rapport_validation_sondage_hotel.xlsx (ou à la sortie de m10).")
    print("Des écarts d’arrondi (ex. 0.01) sont normaux ; des écarts importants signaleraient une incohérence.")
    print("=" * 60)


if __name__ == "__main__":
    main()
