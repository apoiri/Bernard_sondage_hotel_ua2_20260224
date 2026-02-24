# -*- coding: utf-8 -*-
"""
Module 2 – Génération des segments, canal de réservation et annulation
Simulation « L'Hôtel Boutique Art de Vivre »
Lit la config du Module 1 (m01_config.get_config()). Génère ID_Client, Segment, Type_Client, Saison, Canal_reservation, Type_canal, Annulee.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
# Les valeurs par défaut viennent du Module 1 (m01_config). Pour changer les hypothèses
# globales (répartitions segments, canaux, taux d'annulation), modifier m01_config.py.
# Ci-dessous : uniquement des surcharges optionnelles et le seed de hasard.

GRAINE_ALEATOIRE = 42   # Pour reproductibilité ; changer pour un autre tirage.
SAUVEGARDER_ETAPE_CSV = False   # True pour écrire etape2_segments.csv

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

# Import de la config (Module 1 bloqué)
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m01_config import get_config


def _print_hypotheses():
    """Affiche les hypothèses utilisées (lecture config Module 1)."""
    c = get_config()
    print("=" * 60)
    print("HYPOTHÈSES MODULE 2 (segments, canal, annulation)")
    print("=" * 60)
    print(f"  N_RESERVATIONS        = {c['N_RESERVATIONS']}")
    print(f"  Segments              = {c['SEGMENTS_NOMS']}")
    print(f"  Répartition %         = {c['SEGMENTS_POURCENTAGES']}")
    print(f"  Part direct           = {c['PART_RESERVATIONS_DIRECT']}")
    print(f"  Taux annulation direct = {c['TAUX_ANNULATION_DIRECT']} ; intermédiaire = {c['TAUX_ANNULATION_INTERMEDIAIRE']}")
    print(f"  Graine aléatoire      = {GRAINE_ALEATOIRE}")
    print("=" * 60)


def _effectifs_par_segment(n_total, pourcentages):
    """Répartit n_total en effectifs par segment (somme = n_total)."""
    n_seg = len(pourcentages)
    effectifs = [int(round(n_total * p / 100)) for p in pourcentages]
    diff = n_total - sum(effectifs)
    if diff != 0:
        effectifs[0] += diff
    return effectifs


def run():
    """Génère le DataFrame segments + canal + annulation. Retourne le DataFrame."""
    c = get_config()
    np.random.seed(GRAINE_ALEATOIRE)
    n = c["N_RESERVATIONS"]
    n_seg = len(c["SEGMENTS_NOMS"])

    # --- ID_Client : AB-0001 ... AB-10512 ---
    id_clients = [f"AB-{i:05d}" for i in range(1, n + 1)]

    # --- Segment : répartition selon % ---
    effectifs = _effectifs_par_segment(n, c["SEGMENTS_POURCENTAGES"])
    segment_list = []
    for i, nom in enumerate(c["SEGMENTS_NOMS"]):
        segment_list.extend([nom] * effectifs[i])
    # Mélanger pour ne pas avoir tous les Affaires_Solo en tête
    segment_arr = np.array(segment_list)
    perm = np.random.permutation(n)
    segment_arr = segment_arr[perm]

    # --- Type_Client : Interne sauf Local_Gourmet, Local_Spa ---
    type_client = np.array(
        ["Externe" if s in ("Local_Gourmet", "Local_Spa") else "Interne" for s in segment_arr]
    )

    # --- Saison : Haute / Basse selon proba par segment ---
    seg_to_idx = {nom: i for i, nom in enumerate(c["SEGMENTS_NOMS"])}
    proba_basse = np.array(c["PROBA_SAISON_BASSE_PAR_SEGMENT"])
    saison_list = []
    for s in segment_arr:
        idx = seg_to_idx[s]
        if np.random.random() < proba_basse[idx]:
            saison_list.append("Basse")
        else:
            saison_list.append("Haute")
    saison = np.array(saison_list)

    # --- Canal_reservation et Type_canal : 50 % direct, 50 % intermédiaire ---
    part_direct = c["PART_RESERVATIONS_DIRECT"]
    canaux_direct = c["CANAUX_DIRECT"]
    poids_direct = np.array(c["CANAUX_DIRECT_POIDS"])
    poids_direct = poids_direct / poids_direct.sum()
    canaux_inter = c["CANAUX_INTERMEDIAIRES"]
    poids_inter = np.array(c["CANAUX_INTERMEDIAIRES_POIDS"])
    poids_inter = poids_inter / poids_inter.sum()

    canal_list = []
    type_canal_list = []
    for _ in range(n):
        if np.random.random() < part_direct:
            type_canal_list.append("Direct")
            canal_list.append(np.random.choice(canaux_direct, p=poids_direct))
        else:
            type_canal_list.append("Intermediaire")
            canal_list.append(np.random.choice(canaux_inter, p=poids_inter))
    canal_reservation = np.array(canal_list)
    type_canal = np.array(type_canal_list)

    # --- Annulee : 7 % si Direct, 29 % si Intermédiaire ---
    taux_direct = c["TAUX_ANNULATION_DIRECT"]
    taux_inter = c["TAUX_ANNULATION_INTERMEDIAIRE"]
    annulee_list = []
    for tc in type_canal:
        if tc == "Direct":
            annulee_list.append("Oui" if np.random.random() < taux_direct else "Non")
        else:
            annulee_list.append("Oui" if np.random.random() < taux_inter else "Non")
    annulee = np.array(annulee_list)

    df = pd.DataFrame({
        "ID_Client": id_clients,
        "Segment": segment_arr,
        "Type_Client": type_client,
        "Saison": saison,
        "Canal_reservation": canal_reservation,
        "Type_canal": type_canal,
        "Annulee": annulee,
    })
    return df


if __name__ == "__main__":
    _print_hypotheses()
    df = run()
    print(f"DataFrame généré : {len(df)} lignes")
    print(df.head(10).to_string())
    print("\nEffectifs Segment:")
    print(df["Segment"].value_counts().sort_index().to_string())
    print("\nEffectifs Type_canal:")
    print(df["Type_canal"].value_counts().to_string())
    print("\nEffectifs Annulee:")
    print(df["Annulee"].value_counts().to_string())
    print(f"\nTaux d'annulation observé : {(df['Annulee'] == 'Oui').mean()*100:.1f} %")

    if SAUVEGARDER_ETAPE_CSV:
        out_path = Path(__file__).parent / "etape2_segments.csv"
        df.to_csv(out_path, index=False, encoding="utf-8-sig", sep=";")
        print(f"\nSauvegardé : {out_path}")
