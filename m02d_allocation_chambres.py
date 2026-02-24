# -*- coding: utf-8 -*-
"""
Module 02d – Allocation des chambres (type + numéro) à chaque réservation
Simulation « L'Hôtel Boutique Art de Vivre »

Reçoit le DataFrame (sortie m02c), attribue Type_chambre et Numero_chambre à chaque ligne
à partir des types de chambre (m02b), et garantit que chaque chambre a au moins une réservation.
"""

import numpy as np
import pandas as pd
from pathlib import Path

REP_PROJET = Path(__file__).resolve().parent
GRAINE_ALEATOIRE = 44   # Reproductibilité


def _get_rooms_list():
    """Liste des (type_nom, numero_global) pour toutes les chambres. Numéro global 1..N."""
    import sys
    sys.path.insert(0, str(REP_PROJET))
    from m02b_types_chambre_calendrier import get_types_chambre
    types = get_types_chambre()
    rooms = []
    start = 1
    for t in types:
        n = int(t["nb_chambres"])
        nom = t["nom"]
        for i in range(n):
            rooms.append((nom, start + i))
        start += n
    return rooms


def run(df):
    """
    Enrichit le DataFrame avec Type_chambre et Numero_chambre.
    Garantit que chaque chambre (chaque numéro) a au moins une réservation.
    """
    df = df.copy()
    rooms = _get_rooms_list()
    n_rooms = len(rooms)
    n_rows = len(df)

    np.random.seed(GRAINE_ALEATOIRE)

    if n_rows < n_rooms:
        # Plus de chambres que de réservations : on ne peut pas couvrir toutes les chambres
        # Attribution aléatoire ; verifier_toutes_chambres_reservees() retournera False
        idx_perm = np.random.permutation(n_rows)
        type_chambre = [rooms[i % n_rooms][0] for i in range(n_rows)]
        num_chambre = [rooms[i % n_rooms][1] for i in range(n_rows)]
        df["Type_chambre"] = type_chambre
        df["Numero_chambre"] = num_chambre
        return df

    # Permutation des indices : les n_rooms premiers (après perm) reçoivent chaque chambre une fois
    perm = np.random.permutation(n_rows)
    type_chambre = [None] * n_rows
    num_chambre = [None] * n_rows

    for i in range(n_rooms):
        idx = perm[i]
        type_chambre[idx] = rooms[i][0]
        num_chambre[idx] = rooms[i][1]

    for i in range(n_rooms, n_rows):
        idx = perm[i]
        r = rooms[np.random.randint(0, n_rooms)]
        type_chambre[idx] = r[0]
        num_chambre[idx] = r[1]

    df["Type_chambre"] = type_chambre
    df["Numero_chambre"] = num_chambre
    return df


def verifier_toutes_chambres_reservees(df):
    """
    Retourne True si chaque chambre (type + numéro) a au moins une réservation.
    """
    if "Type_chambre" not in df.columns or "Numero_chambre" not in df.columns:
        return False
    rooms = _get_rooms_list()
    present = set(zip(df["Type_chambre"].astype(str), df["Numero_chambre"].astype(int)))
    for t, n in rooms:
        if (t, n) not in present:
            return False
    return True


if __name__ == "__main__":
    import m02c_reservations_avec_dates
    df = m02c_reservations_avec_dates.run()
    df = run(df)
    print(f"DataFrame : {len(df)} lignes, colonnes : {list(df.columns)}")
    print(df[["ID_Client", "Type_chambre", "Numero_chambre"]].head(10).to_string())
    ok = verifier_toutes_chambres_reservees(df)
    print(f"\nToutes chambres réservées au moins 1 fois : {ok}")

# ========== RÈGLE DE BLOCAGE ==========
# Aucune modification de ce module n'est acceptée sans l'autorisation du maître d'ouvrage du projet.
