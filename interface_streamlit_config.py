# -*- coding: utf-8 -*-
"""
Interface utilisateur (Streamlit) – Modification de la config tarification dynamique
Simulation « L'Hôtel Boutique Art de Vivre »

Permet de modifier types de chambre, 12 taux d'occupation, répartition sexe,
plages de revenus, pays/provinces/villes, puis d'exporter config_tarification_dynamique.json.
Ne modifie aucun module m00, m02b, m02c, m02d, m03b.

Lancer : streamlit run interface_streamlit_config.py
(ou : python3 -m streamlit run interface_streamlit_config.py)
"""

import json
from pathlib import Path

import streamlit as st

REP_PROJET = Path(__file__).resolve().parent
FICHIER_EXEMPLE = REP_PROJET / "config_tarification_dynamique_exemple.json"
FICHIER_SORTIE = REP_PROJET / "config_tarification_dynamique.json"

MOIS_NOMS = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
             "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]


def charger_config():
    if FICHIER_SORTIE.exists():
        try:
            with open(FICHIER_SORTIE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    if FICHIER_EXEMPLE.exists():
        with open(FICHIER_EXEMPLE, "r", encoding="utf-8") as f:
            return json.load(f)
    return config_defaut()


def config_defaut():
    return {
        "types_chambre": [
            {"nom": "Standard", "nb_chambres": 35, "prix_base": 180},
            {"nom": "Supérieure", "nb_chambres": 25, "prix_base": 280},
            {"nom": "Confort", "nb_chambres": 20, "prix_base": 350},
            {"nom": "Luxe", "nb_chambres": 12, "prix_base": 420},
            {"nom": "Suite", "nb_chambres": 8, "prix_base": 550},
        ],
        "taux_occupation_mois": [0.55, 0.52, 0.58, 0.62, 0.68, 0.75, 0.88, 0.85, 0.72, 0.65, 0.6, 0.58],
        "repartition_sexe": {"M": 0.48, "F": 0.5, "Autre": 0.02},
        "plages_revenus": [
            {"libelle": "Faible", "min": 0, "max": 40000},
            {"libelle": "Moyen", "min": 40000, "max": 80000},
            {"libelle": "Élevé", "min": 80000, "max": 200000},
        ],
        "pays": [
            {"code": "CA", "nom": "Canada", "poids": 0.45},
            {"code": "US", "nom": "États-Unis", "poids": 0.35},
            {"code": "EU", "nom": "Europe", "poids": 0.15},
            {"code": "Autre", "nom": "Autre", "poids": 0.05},
        ],
        "provinces_par_pays": {
            "CA": [{"code": "QC", "nom": "Québec", "poids": 0.5}, {"code": "ON", "nom": "Ontario", "poids": 0.35}, {"code": "Autre", "nom": "Autre", "poids": 0.15}],
            "US": [{"code": "NY", "nom": "New York", "poids": 0.4}, {"code": "CA", "nom": "California", "poids": 0.3}, {"code": "Autre", "nom": "Autre", "poids": 0.3}],
            "EU": [{"code": "FR", "nom": "France", "poids": 0.5}, {"code": "Autre", "nom": "Autre", "poids": 0.5}],
            "Autre": [{"code": "XX", "nom": "—", "poids": 1}],
        },
        "villes_exemples": {
            "QC": ["Montréal", "Québec", "Laval", "Gatineau"],
            "ON": ["Toronto", "Ottawa", "Mississauga"],
            "NY": ["New York", "Buffalo", "Rochester"],
            "FR": ["Paris", "Lyon", "Marseille"],
        },
    }


def sauver_config(config):
    with open(FICHIER_SORTIE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    return FICHIER_SORTIE


def main():
    st.set_page_config(
        page_title="Config tarification dynamique",
        page_icon="🏨",
        layout="wide",
    )
    st.title("🏨 Config tarification dynamique – Art de Vivre")
    st.caption("Modifiez les valeurs puis exportez vers config_tarification_dynamique.json. Relancez ensuite run_pipeline_evolution.py pour régénérer les données.")

    if "config" not in st.session_state:
        st.session_state.config = charger_config()
    config = st.session_state.config

    # --- Types de chambre ---
    st.header("1. Types de chambre")
    types = config.get("types_chambre", [])
    cols = st.columns(min(3, len(types) + 1))
    new_types = []
    for i, t in enumerate(types):
        with cols[i % 3]:
            with st.expander(t.get("nom", f"Type {i+1}"), expanded=True):
                nom = st.text_input("Nom", value=t.get("nom", ""), key=f"type_nom_{i}")
                nb = st.number_input("Nb chambres", min_value=1, max_value=500, value=int(t.get("nb_chambres", 50)), key=f"type_nb_{i}")
                prix = st.number_input("Prix base ($/nuit)", min_value=0.0, value=float(t.get("prix_base", 200)), step=10.0, key=f"type_prix_{i}")
                new_types.append({"nom": nom or f"Type{i+1}", "nb_chambres": nb, "prix_base": prix})
    if st.button("+ Ajouter un type de chambre"):
        st.session_state.config["types_chambre"] = new_types + [{"nom": "Nouveau", "nb_chambres": 20, "prix_base": 200}]
        st.rerun()
    config["types_chambre"] = new_types

    # --- 12 taux d'occupation ---
    st.header("2. Taux d'occupation par mois (%)")
    taux = config.get("taux_occupation_mois", [0.72] * 12)
    new_taux = []
    c1, c2, c3, c4 = st.columns(4)
    for i in range(12):
        col = [c1, c2, c3, c4][i % 4]
        with col:
            v = st.slider(MOIS_NOMS[i], 0.0, 1.0, float(taux[i]) if i < len(taux) else 0.72, 0.01, key=f"taux_{i}")
            new_taux.append(round(v, 2))
    config["taux_occupation_mois"] = new_taux

    # --- Répartition sexe ---
    st.header("3. Répartition sexe (proportions, somme = 1)")
    rsex = config.get("repartition_sexe", {"M": 0.48, "F": 0.5, "Autre": 0.02})
    col1, col2, col3 = st.columns(3)
    with col1:
        m = st.number_input("Homme (M)", 0.0, 1.0, float(rsex.get("M", 0.48)), 0.01, key="sex_m")
    with col2:
        f = st.number_input("Femme (F)", 0.0, 1.0, float(rsex.get("F", 0.5)), 0.01, key="sex_f")
    with col3:
        a = st.number_input("Autre", 0.0, 1.0, float(rsex.get("Autre", 0.02)), 0.01, key="sex_a")
    total = m + f + a
    if abs(total - 1.0) > 0.001:
        st.warning(f"La somme vaut {total:.2f}. Ajustez pour que la somme = 1.")
    config["repartition_sexe"] = {"M": round(m, 2), "F": round(f, 2), "Autre": round(a, 2)}

    # --- Plages de revenus ---
    st.header("4. Plages de revenus (annuels)")
    plages = config.get("plages_revenus", [])
    new_plages = []
    for i, p in enumerate(plages):
        with st.expander(p.get("libelle", f"Plage {i+1}")):
            lib = st.text_input("Libellé", value=p.get("libelle", ""), key=f"rev_lib_{i}")
            mn = st.number_input("Min ($)", 0, 1000000, int(p.get("min", 0)), key=f"rev_min_{i}")
            mx = st.number_input("Max ($)", 0, 1000000, int(p.get("max", 50000)), key=f"rev_max_{i}")
            new_plages.append({"libelle": lib or f"Plage{i+1}", "min": mn, "max": mx})
    config["plages_revenus"] = new_plages

    # --- Pays (code, nom, poids) ---
    st.header("5. Pays (code, nom, poids)")
    pays = config.get("pays", [])
    new_pays = []
    for i, p in enumerate(pays):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            code = st.text_input("Code", value=p.get("code", ""), key=f"pays_code_{i}")
        with c2:
            nom = st.text_input("Nom", value=p.get("nom", ""), key=f"pays_nom_{i}")
        with c3:
            poids = st.number_input("Poids", 0.0, 1.0, float(p.get("poids", 0.25)), 0.05, key=f"pays_poids_{i}")
        new_pays.append({"code": code or f"P{i}", "nom": nom or code, "poids": round(poids, 2)})
    config["pays"] = new_pays
    if st.button("+ Ajouter un pays"):
        config["pays"].append({"code": "XX", "nom": "Nouveau", "poids": 0.05})
        st.rerun()

    st.session_state.config = config

    # --- Export ---
    st.divider()
    st.subheader("Exporter la configuration")
    if st.button("Enregistrer config_tarification_dynamique.json", type="primary"):
        path = sauver_config(config)
        st.success(f"Fichier enregistré : {path}")
        st.info("Relancez run_pipeline_evolution.py pour régénérer le CSV avec ces valeurs.")

    with st.expander("Aperçu JSON"):
        st.code(json.dumps(config, ensure_ascii=False, indent=2), language="json")


if __name__ == "__main__":
    main()
