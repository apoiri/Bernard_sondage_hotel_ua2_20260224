# -*- coding: utf-8 -*-
"""
Module 9 – Types de données et export CSV
Simulation « L'Hôtel Boutique Art de Vivre »
Reçoit le DataFrame du Module 8. Force les types, exporte vers sondage_hotel_data.csv.
"""

import pandas as pd
from pathlib import Path

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
FICHIER_CSV_SORTIE = "sondage_hotel_data.csv"
ENCODAGE_CSV = "utf-8-sig"
SEPARATEUR_CSV = ";"
AFFICHER_APERCU = True          # Afficher les 20 premières lignes et un résumé
REPERTOIRE_SORTIE = None        # None = même dossier que ce script ; ou chemin absolu

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m01_config import get_config


def _print_hypotheses():
    """Affiche les hypothèses utilisées."""
    print("=" * 60)
    print("HYPOTHÈSES MODULE 9 (Export CSV)")
    print("=" * 60)
    print(f"  Fichier de sortie  = {FICHIER_CSV_SORTIE}")
    print(f"  Encodage           = {ENCODAGE_CSV}")
    print(f"  Séparateur         = {SEPARATEUR_CSV}")
    print(f"  Aperçu (20 lignes) = {AFFICHER_APERCU}")
    print("=" * 60)


def _forcer_types(df):
    """Force les types des colonnes pour l'export."""
    df = df.copy()
    # Catégories
    for col in ["Segment", "Type_Client", "Saison", "Canal_reservation", "Type_canal", "Annulee", "Type_Forfait"]:
        if col in df.columns:
            df[col] = df[col].astype("category")
    # Entier
    if "Nuits" in df.columns:
        df["Nuits"] = pd.to_numeric(df["Nuits"], errors="coerce").fillna(0).astype(int)
    # Flottants (revenus, Total_Facture, Satisfaction_NPS)
    for col in ["Rev_Chambre", "Rev_Banquet", "Rev_Resto", "Rev_Spa", "Total_Facture", "Satisfaction_NPS"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def run(df):
    """
    Force les types du DataFrame (sortie Module 8), exporte en CSV.
    Retourne le DataFrame (avec types forcés) et le chemin du fichier écrit.
    """
    df = _forcer_types(df)
    rep = Path(REPERTOIRE_SORTIE) if REPERTOIRE_SORTIE else Path(__file__).resolve().parent
    chemin = rep / FICHIER_CSV_SORTIE
    df.to_csv(chemin, index=False, encoding=ENCODAGE_CSV, sep=SEPARATEUR_CSV, decimal=".")
    return df, chemin


if __name__ == "__main__":
    _print_hypotheses()
    import m02_segments
    import m03_nuits_chambre
    import m04_revenus_centres_profit
    import m05_type_forfait
    import m06_satisfaction_nps
    import m07_total_facture
    import m08_anomalies_pedagogiques
    df = m02_segments.run()
    df = m03_nuits_chambre.run(df)
    df = m04_revenus_centres_profit.run(df)
    df = m05_type_forfait.run(df)
    df = m06_satisfaction_nps.run(df)
    df = m07_total_facture.run(df)
    df = m08_anomalies_pedagogiques.run(df)
    df, chemin = run(df)
    print(f"Exporté : {chemin} ({len(df)} lignes)")

    if AFFICHER_APERCU:
        print("\n--- 20 premières lignes ---")
        print(df.head(20).to_string())
        print("\n--- Résumé (effectifs par segment) ---")
        print(df["Segment"].value_counts().sort_index().to_string())
        print("\n--- Min/Max (variables numériques) ---")
        num = ["Nuits", "Rev_Chambre", "Rev_Resto", "Rev_Spa", "Total_Facture", "Satisfaction_NPS"]
        num = [c for c in num if c in df.columns]
        print(df[num].agg(["min", "max"]).to_string())
