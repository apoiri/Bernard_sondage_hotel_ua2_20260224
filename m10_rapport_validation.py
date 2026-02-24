# -*- coding: utf-8 -*-
"""
Module 10 – Sommaire analytique et rapport de validation
Simulation « L'Hôtel Boutique Art de Vivre »
Lit le CSV produit (Module 9), exécute les analyses statistiques prévues pour les étudiants,
affiche un sommaire dans le terminal et produit un fichier Excel de rapport.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
FICHIER_CSV_ENTREE = "sondage_hotel_data.csv"   # CSV produit par le Module 9
FICHIER_EXCEL_SORTIE = "rapport_validation_sondage_hotel.xlsx"
REPERTOIRE = None   # None = même dossier que ce script
SEPARATEUR_CSV = ";"

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))


def _repertoire():
    return Path(REPERTOIRE) if REPERTOIRE else Path(__file__).resolve().parent


def _ic_proportion(p, n, alpha=0.05):
    """IC 95 % pour une proportion (Wilson ou approximation normale)."""
    if n == 0:
        return np.nan, np.nan
    z = 1.96
    rad = z * np.sqrt(p * (1 - p) / n)
    return max(0, p - rad), min(1, p + rad)


def _run_analyses(df):
    """Exécute toutes les analyses, retourne un dict de résultats et DataFrames pour Excel."""
    res = {}
    mask_non_annule = df["Annulee"] == "Non"
    n_total = len(df)
    n_non_annule = mask_non_annule.sum()

    # --- 1. Statistiques descriptives ---
    num_cols = ["Nuits", "Rev_Chambre", "Rev_Resto", "Rev_Spa", "Total_Facture", "Satisfaction_NPS"]
    num_cols = [c for c in num_cols if c in df.columns]
    desc = df[num_cols].describe().round(4)
    effectifs_segment = df["Segment"].value_counts().sort_index()
    effectifs_type = df["Type_Client"].value_counts()
    effectifs_saison = df["Saison"].value_counts()
    effectifs_annulee = df["Annulee"].value_counts()
    res["descriptif"] = {"desc": desc, "effectifs_segment": effectifs_segment, "effectifs_type": effectifs_type, "effectifs_saison": effectifs_saison, "effectifs_annulee": effectifs_annulee}

    # --- 2. Proportions et IC ---
    p_annule = (df["Annulee"] == "Oui").mean()
    ic_annule = _ic_proportion(p_annule, n_total)
    mask_spa = (df["Rev_Spa"] > 0) & df["Rev_Spa"].notna()
    p_spa = mask_spa.mean()
    ic_spa = _ic_proportion(p_spa, n_total)
    p_forfait = (df["Type_Forfait"] == "Forfait Gastronomique").mean()
    ic_forfait = _ic_proportion(p_forfait, n_total)
    res["proportions"] = {"p_annule": p_annule, "ic_annule": ic_annule, "p_spa": p_spa, "ic_spa": ic_spa, "p_forfait": p_forfait, "ic_forfait": ic_forfait}

    # --- 3. Khi-deux Segment × Type_Forfait ---
    ct = pd.crosstab(df["Segment"], df["Type_Forfait"])
    chi2, p_chi2, ddl, expected = stats.chi2_contingency(ct)
    res["khi2"] = {"tableau": ct, "chi2": chi2, "p_value": p_chi2, "ddl": ddl}

    # --- 4. Pearson Rev_Spa vs Satisfaction_NPS (non annulées, sans NaN) ---
    sub = df.loc[mask_non_annule, ["Rev_Spa", "Satisfaction_NPS"]].dropna()
    if len(sub) >= 2:
        r_pearson, p_pearson = stats.pearsonr(sub["Rev_Spa"], sub["Satisfaction_NPS"])
    else:
        r_pearson, p_pearson = np.nan, np.nan
    res["pearson"] = {"r": r_pearson, "p_value": p_pearson, "n": len(sub)}

    # --- 5. ANOVA Rev_Resto par Segment (non annulées) ---
    groups = [df.loc[mask_non_annule & (df["Segment"] == s), "Rev_Resto"].dropna().values for s in df["Segment"].unique()]
    groups = [g for g in groups if len(g) >= 2]
    if len(groups) >= 2:
        f_anova, p_anova = stats.f_oneway(*groups)
        moy_resto = df.loc[mask_non_annule].groupby("Segment")["Rev_Resto"].agg(["mean", "count"]).round(4)
    else:
        f_anova, p_anova = np.nan, np.nan
        moy_resto = pd.DataFrame()
    res["anova"] = {"f": f_anova, "p_value": p_anova, "moyennes": moy_resto}

    # --- 6. Régression Total_Facture ~ Rev_Chambre + Rev_Resto + Rev_Spa ---
    reg_df = df[["Total_Facture", "Rev_Chambre", "Rev_Resto", "Rev_Spa"]].dropna()
    if len(reg_df) >= 4:
        y = reg_df["Total_Facture"].values
        X = reg_df[["Rev_Chambre", "Rev_Resto", "Rev_Spa"]].values
        X1 = np.column_stack([np.ones(len(X)), X])
        beta, _, _, _ = np.linalg.lstsq(X1, y, rcond=None)
        y_pred = X1 @ beta
        r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2) if np.sum((y - y.mean()) ** 2) > 0 else 0
        res["regression"] = {"constante": beta[0], "coef_chambre": beta[1], "coef_resto": beta[2], "coef_spa": beta[3], "r2": r2, "n": len(reg_df)}
    else:
        res["regression"] = {"constante": np.nan, "coef_chambre": np.nan, "coef_resto": np.nan, "coef_spa": np.nan, "r2": np.nan, "n": len(reg_df)}

    # --- 7. Annulations par canal ---
    taux_annule_direct = (df["Type_canal"] == "Direct") & (df["Annulee"] == "Oui")
    n_direct = (df["Type_canal"] == "Direct").sum()
    n_direct_annule = taux_annule_direct.sum()
    taux_direct = n_direct_annule / n_direct if n_direct > 0 else np.nan
    n_inter = (df["Type_canal"] == "Intermediaire").sum()
    n_inter_annule = ((df["Type_canal"] == "Intermediaire") & (df["Annulee"] == "Oui")).sum()
    taux_inter = n_inter_annule / n_inter if n_inter > 0 else np.nan
    res["annulations"] = {"taux_direct": taux_direct, "taux_inter": taux_inter, "n_direct": n_direct, "n_inter": n_inter}
    by_canal = df.groupby("Canal_reservation").agg({"Annulee": lambda x: (x == "Oui").sum(), "ID_Client": "count"}).rename(columns={"ID_Client": "n"})
    by_canal["taux_annule"] = (by_canal["Annulee"] / by_canal["n"]).round(4)
    res["annulations_table"] = by_canal

    # --- 8. Contrôle qualité (anomalies pédagogiques) ---
    incoh = ((df["Type_Client"] == "Externe") & (df["Nuits"] > 0)).sum()
    nps99 = (df["Satisfaction_NPS"] == 99).sum()
    manq_spa = df["Rev_Spa"].isna().sum()
    manq_resto = df["Rev_Resto"].isna().sum()
    pct_manq_spa = manq_spa / n_total * 100
    pct_manq_resto = manq_resto / n_total * 100
    n_unique = df.drop_duplicates().shape[0]
    n_doublons = n_total - n_unique
    res["qualite"] = {"incoherences": incoh, "nps_99": nps99, "manquants_spa": manq_spa, "manquants_resto": manq_resto, "pct_manq_spa": pct_manq_spa, "pct_manq_resto": pct_manq_resto, "doublons": n_doublons}

    return res


def _print_rapport(res):
    """Affiche le sommaire dans le terminal."""
    print("\n" + "=" * 60)
    print("RAPPORT DE VALIDATION – Sondage Hôtel Art de Vivre")
    print("=" * 60)

    print("\n--- 1. Descriptif (effectifs par segment) ---")
    print(res["descriptif"]["effectifs_segment"].to_string())
    print("\n--- 2. Proportions et IC 95 % ---")
    p = res["proportions"]
    print(f"  % Annulées     : {p['p_annule']*100:.1f} %  IC 95 % : [{p['ic_annule'][0]*100:.1f} % ; {p['ic_annule'][1]*100:.1f} %]")
    print(f"  % Rev_Spa > 0  : {p['p_spa']*100:.1f} %  IC 95 % : [{p['ic_spa'][0]*100:.1f} % ; {p['ic_spa'][1]*100:.1f} %]")
    print(f"  % Forfait Gast.: {p['p_forfait']*100:.1f} %  IC 95 % : [{p['ic_forfait'][0]*100:.1f} % ; {p['ic_forfait'][1]*100:.1f} %]")

    print("\n--- 3. Khi-deux (Segment × Type_Forfait) ---")
    print(f"  Khi² = {res['khi2']['chi2']:.2f}  ddl = {res['khi2']['ddl']}  p-value = {res['khi2']['p_value']:.4f}")
    print("  Verdict : OK (liaison significative)" if res["khi2"]["p_value"] < 0.05 else "  Verdict : À vérifier")

    print("\n--- 4. Corrélation Pearson (Rev_Spa × Satisfaction_NPS) ---")
    print(f"  r = {res['pearson']['r']:.3f}  p-value = {res['pearson']['p_value']:.4f}  n = {res['pearson']['n']}")
    print("  Verdict : OK (r ≈ 0,75)" if 0.6 <= res["pearson"]["r"] <= 0.9 else "  Verdict : À vérifier")

    print("\n--- 5. ANOVA (Rev_Resto par Segment) ---")
    print(f"  F = {res['anova']['f']:.2f}  p-value = {res['anova']['p_value']:.4f}")
    print("  Verdict : OK (segments diffèrent)" if res["anova"]["p_value"] < 0.05 else "  Verdict : À vérifier")

    print("\n--- 6. Régression (Total_Facture ~ Rev_Chambre + Rev_Resto + Rev_Spa) ---")
    r = res["regression"]
    print(f"  Constante ≈ {r['constante']:.2f}  coef Rev_Chambre ≈ {r['coef_chambre']:.2f}  Rev_Resto ≈ {r['coef_resto']:.2f}  Rev_Spa ≈ {r['coef_spa']:.2f}  R² = {r['r2']:.4f}")
    print("  Verdict : OK (coefficients ≈ 1 ; 1,1 ; 1,3)" if (0.9 <= r["coef_chambre"] <= 1.1 and 1.0 <= r["coef_resto"] <= 1.2 and 1.2 <= r["coef_spa"] <= 1.4) else "  Verdict : À vérifier")

    print("\n--- 7. Annulations par canal ---")
    print(f"  Taux annulation Direct       : {res['annulations']['taux_direct']*100:.1f} % (attendu ~7 %)")
    print(f"  Taux annulation Intermédiaire : {res['annulations']['taux_inter']*100:.1f} % (attendu ~29 %)")
    print("  Verdict : OK" if 0.05 <= res["annulations"]["taux_direct"] <= 0.12 and 0.22 <= res["annulations"]["taux_inter"] <= 0.36 else "  Verdict : À vérifier")

    print("\n--- 8. Contrôle qualité (anomalies pédagogiques) ---")
    q = res["qualite"]
    print(f"  Externes avec Nuits > 0 : {q['incoherences']}  |  NPS = 99 : {q['nps_99']}  |  Manquants Rev_Spa : {q['manquants_spa']} ({q['pct_manq_spa']:.1f} %)  |  Rev_Resto : {q['manquants_resto']} ({q['pct_manq_resto']:.1f} %)  |  Doublons : {q['doublons']}")
    print("  Verdict : OK (anomalies présentes pour exercice nettoyage)" if q["incoherences"] >= 10 and q["nps_99"] >= 1 and q["doublons"] >= 1 else "  Verdict : À vérifier")
    print("=" * 60)


def _export_excel(res, df, chemin_excel):
    """Écrit le rapport dans un fichier Excel (un onglet par section)."""
    rep = _repertoire()
    path = Path(chemin_excel) if Path(chemin_excel).is_absolute() else rep / Path(chemin_excel).name
    with pd.ExcelWriter(path, engine="openpyxl") as w:
        res["descriptif"]["desc"].to_excel(w, sheet_name="Descriptif_numerique")
        res["descriptif"]["effectifs_segment"].to_frame("Effectif").to_excel(w, sheet_name="Effectifs_Segment")
        res["descriptif"]["effectifs_annulee"].to_frame("Effectif").to_excel(w, sheet_name="Effectifs_Annulee")
        # Proportions
        prop_df = pd.DataFrame({
            "Indicateur": ["% Annulées", "% Rev_Spa > 0", "% Forfait Gastronomique"],
            "Proportion": [res["proportions"]["p_annule"], res["proportions"]["p_spa"], res["proportions"]["p_forfait"]],
            "IC95_bas": [res["proportions"]["ic_annule"][0], res["proportions"]["ic_spa"][0], res["proportions"]["ic_forfait"][0]],
            "IC95_haut": [res["proportions"]["ic_annule"][1], res["proportions"]["ic_spa"][1], res["proportions"]["ic_forfait"][1]],
        })
        prop_df.to_excel(w, sheet_name="Proportions_IC", index=False)
        res["khi2"]["tableau"].to_excel(w, sheet_name="Khi2_Tableau")
        pd.DataFrame({"Khi2": [res["khi2"]["chi2"]], "ddl": [res["khi2"]["ddl"]], "p_value": [res["khi2"]["p_value"]]}).to_excel(w, sheet_name="Khi2_Resultat", index=False)
        pd.DataFrame({"r_Pearson": [res["pearson"]["r"]], "p_value": [res["pearson"]["p_value"]], "n": [res["pearson"]["n"]]}).to_excel(w, sheet_name="Pearson", index=False)
        if not res["anova"]["moyennes"].empty:
            res["anova"]["moyennes"].to_excel(w, sheet_name="ANOVA_Moyennes")
        pd.DataFrame({"F": [res["anova"]["f"]], "p_value": [res["anova"]["p_value"]]}).to_excel(w, sheet_name="ANOVA_Resultat", index=False)
        r = res["regression"]
        coef_vals = [r["constante"], r["coef_chambre"], r["coef_resto"], r["coef_spa"]]
        pd.DataFrame({"Coefficient": ["Constante", "Rev_Chambre", "Rev_Resto", "Rev_Spa"], "Valeur": coef_vals}).to_excel(w, sheet_name="Regression", index=False)
        pd.DataFrame({"R2": [r["r2"]], "n": [r["n"]]}).to_excel(w, sheet_name="Regression_R2", index=False)
        res["annulations_table"].to_excel(w, sheet_name="Annulations_Canal")
        pd.DataFrame({"Taux_Direct": [res["annulations"]["taux_direct"]], "Taux_Intermediaire": [res["annulations"]["taux_inter"]]}).to_excel(w, sheet_name="Annulations_Resume", index=False)
        q = res["qualite"]
        pd.DataFrame({"Anomalie": ["Externes Nuits>0", "NPS=99", "Manquants Rev_Spa", "Manquants Rev_Resto", "Doublons"], "Valeur": [q["incoherences"], q["nps_99"], q["manquants_spa"], q["manquants_resto"], q["doublons"]]}).to_excel(w, sheet_name="Qualite", index=False)
    return path


def run(chemin_csv=None, chemin_excel=None):
    """
    Charge le CSV, exécute les analyses, affiche dans le terminal et exporte en Excel.
    chemin_csv : chemin vers sondage_hotel_data.csv (défaut : REPERTOIRE / FICHIER_CSV_ENTREE)
    chemin_excel : chemin de sortie Excel (défaut : REPERTOIRE / FICHIER_EXCEL_SORTIE)
    """
    rep = _repertoire()
    chemin_csv = chemin_csv or rep / FICHIER_CSV_ENTREE
    chemin_excel = chemin_excel or rep / FICHIER_EXCEL_SORTIE
    if not Path(chemin_csv).exists():
        raise FileNotFoundError(f"Fichier CSV introuvable : {chemin_csv}")
    df = pd.read_csv(chemin_csv, sep=SEPARATEUR_CSV, encoding="utf-8-sig", decimal=".")
    print(f"Données chargées : {len(df)} lignes depuis {chemin_csv}")
    res = _run_analyses(df)
    _print_rapport(res)
    path_excel = _export_excel(res, df, chemin_excel)
    print(f"\nRapport Excel enregistré : {path_excel}")
    return res


if __name__ == "__main__":
    print("=" * 60)
    print("HYPOTHÈSES MODULE 10 (Rapport de validation)")
    print("=" * 60)
    print(f"  Fichier CSV entrée  = {FICHIER_CSV_ENTREE}")
    print(f"  Fichier Excel sortie = {FICHIER_EXCEL_SORTIE}")
    print("=" * 60)
    run()

# ========== RÈGLE DE BLOCAGE ==========
# Aucune modification de ce module n'est acceptée sans l'autorisation du maître d'ouvrage du projet.
