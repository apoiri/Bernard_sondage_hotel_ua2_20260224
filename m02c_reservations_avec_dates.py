# -*- coding: utf-8 -*-
"""
Module 02c – Réservations enrichies (mois de séjour, sexe, revenus, pays, province, ville)
Simulation « L'Hôtel Boutique Art de Vivre »

Appelle m02.run() puis enrichit le DataFrame avec les colonnes :
Mois_sejour, Sexe, Niveau_revenus, Pays, Province, Ville (à partir de la config étendue).
"""

import numpy as np
import pandas as pd
from pathlib import Path

REP_PROJET = Path(__file__).resolve().parent
GRAINE_ALEATOIRE = 43   # Reproductibilité (différente de m02)


def _get_config_etendue():
    import sys
    sys.path.insert(0, str(REP_PROJET))
    from m00_config_etendue import get_config_etendue
    return get_config_etendue()


def run():
    """
    Génère le DataFrame des segments (m02) puis ajoute Mois_sejour, Sexe,
    Niveau_revenus, Pays, Province, Ville. Retourne le DataFrame enrichi.
    """
    import sys
    sys.path.insert(0, str(REP_PROJET))
    from m02_segments import run as m02_run

    df = m02_run()
    cfg = _get_config_etendue()
    n = len(df)
    np.random.seed(GRAINE_ALEATOIRE)

    # --- Mois_sejour (1-12) : pondéré par taux d'occupation si dispo ---
    if "taux_occupation_mois" in cfg and len(cfg["taux_occupation_mois"]) == 12:
        poids_mois = np.array(cfg["taux_occupation_mois"], dtype=float)
        poids_mois = poids_mois / poids_mois.sum()
        mois = np.random.choice(12, size=n, p=poids_mois) + 1
    else:
        mois = np.random.randint(1, 13, size=n)
    df = df.copy()
    df["Mois_sejour"] = mois

    # --- Sexe : répartition config ou défaut 50/50 M-F ---
    if "repartition_sexe" in cfg and cfg["repartition_sexe"]:
        r = cfg["repartition_sexe"]
        codes = list(r.keys())
        poids = np.array([float(r[k]) for k in codes])
        poids = poids / poids.sum()
        df["Sexe"] = np.random.choice(codes, size=n, p=poids)
    else:
        df["Sexe"] = np.random.choice(["M", "F"], size=n, p=[0.5, 0.5])

    # --- Niveau_revenus : libellés des plages (répartition égale si pas de poids) ---
    if "plages_revenus" in cfg and len(cfg["plages_revenus"]) >= 1:
        plages = cfg["plages_revenus"]
        libelles = [p["libelle"] for p in plages]
        df["Niveau_revenus"] = np.random.choice(libelles, size=n)
    else:
        df["Niveau_revenus"] = np.random.choice(["Faible", "Moyen", "Élevé"], size=n)

    # --- Pays → Province → Ville (hiérarchique) ---
    if "pays" in cfg and len(cfg["pays"]) >= 1 and "provinces_par_pays" in cfg:
        pays_list = cfg["pays"]
        codes_pays = [p["code"] for p in pays_list]
        poids_pays = np.array([float(p.get("poids", 1.0)) for p in pays_list])
        poids_pays = poids_pays / poids_pays.sum()
        noms_pays = {p["code"]: p.get("nom", p["code"]) for p in pays_list}
        prov_par_pays = cfg["provinces_par_pays"]
        villes_ex = cfg.get("villes_exemples") or {}

        pays_codes = np.random.choice(codes_pays, size=n, p=poids_pays)
        df["Pays"] = [noms_pays[c] for c in pays_codes]

        provinces_noms = []
        provinces_codes = []
        for code_p in pays_codes:
            prov_list = prov_par_pays.get(code_p)
            if not prov_list:
                provinces_noms.append("—")
                provinces_codes.append("XX")
                continue
            codes_prov = [x["code"] for x in prov_list]
            poids_prov = np.array([float(x.get("poids", 1.0)) for x in prov_list])
            poids_prov = poids_prov / poids_prov.sum()
            idx = np.random.choice(len(codes_prov), p=poids_prov)
            provinces_codes.append(codes_prov[idx])
            provinces_noms.append(prov_list[idx].get("nom", codes_prov[idx]))
        df["Province"] = provinces_noms

        villes_list = []
        for pc in provinces_codes:
            options = villes_ex.get(pc)
            if options and len(options) >= 1:
                villes_list.append(np.random.choice(options))
            else:
                villes_list.append("Non spécifié")
        df["Ville"] = villes_list
    else:
        df["Pays"] = "Canada"
        df["Province"] = "Québec"
        df["Ville"] = "Montréal"

    return df


if __name__ == "__main__":
    df = run()
    print(f"DataFrame enrichi : {len(df)} lignes")
    print("Colonnes :", list(df.columns))
    print(df[["ID_Client", "Mois_sejour", "Sexe", "Niveau_revenus", "Pays", "Province", "Ville"]].head(10).to_string())

# ========== RÈGLE DE BLOCAGE ==========
# Aucune modification de ce module n'est acceptée sans l'autorisation du maître d'ouvrage du projet.
