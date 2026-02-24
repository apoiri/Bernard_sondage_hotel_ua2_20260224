# -*- coding: utf-8 -*-
"""
Module 02e – Saison calendrier (alignée sur la tarification dynamique)
Simulation « L'Hôtel Boutique Art de Vivre »

Reçoit le DataFrame (sortie m02c) et ajoute la colonne **Saison_calendrier** dérivée du
**Mois_sejour**, pour que les analyses "haute vs basse saison" soient cohérentes avec
la tarification dynamique (Tarif_applique / Rev_Chambre basés sur le mois, pas sur Saison).

Définition (ex. Ottawa / Québec) :
- Haute  = juin, juillet, août (6, 7, 8)
- Basse  = décembre, janvier, février (12, 1, 2)
- Épaule = mars à mai, septembre à novembre (3, 4, 5, 9, 10, 11)
"""

import pandas as pd
from pathlib import Path

REP_PROJET = Path(__file__).resolve().parent

MOIS_HAUTE = (6, 7, 8)    # juin, juil, août
MOIS_BASSE = (12, 1, 2)   # déc, janv, fév


def run(df):
    """
    Ajoute la colonne Saison_calendrier : Haute | Basse | Épaule selon Mois_sejour.
    """
    df = df.copy()
    if "Mois_sejour" not in df.columns:
        df["Saison_calendrier"] = "Épaule"
        return df
    mois = df["Mois_sejour"].astype(int)
    saison = pd.Series("Épaule", index=df.index)
    saison[mois.isin(MOIS_HAUTE)] = "Haute"
    saison[mois.isin(MOIS_BASSE)] = "Basse"
    df["Saison_calendrier"] = saison.values
    return df


if __name__ == "__main__":
    import m02c_reservations_avec_dates
    df = m02c_reservations_avec_dates.run()
    df = run(df)
    print(df[["Mois_sejour", "Saison_calendrier"]].drop_duplicates().sort_values("Mois_sejour").to_string())

# ========== RÈGLE DE BLOCAGE ==========
# Aucune modification de ce module n'est acceptée sans l'autorisation du maître d'ouvrage du projet.
