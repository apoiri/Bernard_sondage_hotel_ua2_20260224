# -*- coding: utf-8 -*-
"""
Module 03b – Revenus chambre (tarification dynamique)
Simulation « L'Hôtel Boutique Art de Vivre »

Reçoit le DataFrame (sortie m02d, avec Nuits ajoutées par m03). Calcule Rev_Chambre
= Nuits × prix_base(type) × coefficient(mois), 0 si Externe ou Annulée.
Ajoute éventuellement Tarif_applique = prix_base × coefficient (tarif/nuit appliqué).
"""

import numpy as np
import pandas as pd
from pathlib import Path

REP_PROJET = Path(__file__).resolve().parent


def _get_prix_base_par_type():
    """Dictionnaire nom_type -> prix_base."""
    import sys
    sys.path.insert(0, str(REP_PROJET))
    from m02b_types_chambre_calendrier import get_types_chambre
    return {t["nom"]: float(t["prix_base"]) for t in get_types_chambre()}


def _get_coefficient_mois(mois):
    import sys
    sys.path.insert(0, str(REP_PROJET))
    from m02b_types_chambre_calendrier import get_coefficient_mois
    return get_coefficient_mois(int(mois))


def run(df):
    """
    Attend un DataFrame avec colonnes Type_Client, Annulee, Type_chambre, Mois_sejour.
    Si Nuits n'existe pas, appelle m03.run(df) pour l'ajouter.
    Ajoute ou remplace Rev_Chambre (tarification dynamique) et Tarif_applique.
    """
    import sys
    sys.path.insert(0, str(REP_PROJET))
    if "Nuits" not in df.columns:
        from m03_nuits_chambre import run as m03_run
        df = m03_run(df)
    else:
        df = df.copy()

    prix_par_type = _get_prix_base_par_type()
    n = len(df)
    externe = (df["Type_Client"] == "Externe").values
    annulee = (df["Annulee"] == "Oui").values
    mask_interne_non_annule = ~externe & ~annulee

    rev_chambre = np.zeros(n, dtype=float)
    tarif_applique = np.zeros(n, dtype=float)

    for i in range(n):
        type_ch = df["Type_chambre"].iloc[i]
        mois = df["Mois_sejour"].iloc[i]
        prix_base = prix_par_type.get(type_ch, 250.0)
        coeff = _get_coefficient_mois(mois)
        tarif_nuit = prix_base * coeff
        tarif_applique[i] = tarif_nuit
        if mask_interne_non_annule[i]:
            nuits = int(df["Nuits"].iloc[i])
            rev_chambre[i] = nuits * tarif_nuit

    df["Rev_Chambre"] = rev_chambre
    df["Tarif_applique"] = tarif_applique
    return df


if __name__ == "__main__":
    import m02c_reservations_avec_dates
    import m02d_allocation_chambres
    df = m02c_reservations_avec_dates.run()
    df = m02d_allocation_chambres.run(df)
    df = run(df)
    print(f"DataFrame : {len(df)} lignes")
    print(df[["ID_Client", "Type_Client", "Annulee", "Type_chambre", "Mois_sejour", "Nuits", "Tarif_applique", "Rev_Chambre"]].head(10).to_string())
    mask = (df["Type_Client"] == "Interne") & (df["Annulee"] == "Non")
    print("\nRev_Chambre = 0 pour Externe/Annulée:", (df.loc[~mask, "Rev_Chambre"] == 0).all())
    print("Rev_Chambre > 0 pour Interne non annulé (échantillon):", df.loc[mask, "Rev_Chambre"].head(5).tolist())

# ========== RÈGLE DE BLOCAGE ==========
# Aucune modification de ce module n'est acceptée sans l'autorisation du maître d'ouvrage du projet.
