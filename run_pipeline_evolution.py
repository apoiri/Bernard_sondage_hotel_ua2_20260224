# -*- coding: utf-8 -*-
"""
Pipeline évolution – m00 → m02b → m02c → m02d → m03b → m04 … m09 → m10 → m11
Simulation « L'Hôtel Boutique Art de Vivre »

Enchaîne la génération des données avec tarification dynamique (types de chambre,
coefficients par mois, Rev_Chambre dynamique) puis export CSV, rapport Excel et synthèse Word.
Produit les mêmes livrables que run_pipeline.py avec les colonnes supplémentaires :
Type_chambre, Numero_chambre, Mois_sejour, Sexe, Niveau_revenus, Pays, Province, Ville, Tarif_applique.

Usage : python3 run_pipeline_evolution.py
"""

import os
import subprocess
import sys
from pathlib import Path

REP_PROJET = Path(__file__).resolve().parent


def run_script(script: str) -> int:
    """Exécute un script Python ; retourne le code de sortie."""
    p = subprocess.run(
        [sys.executable, script],
        cwd=REP_PROJET,
        capture_output=False,
    )
    return p.returncode


def main() -> int:
    os.chdir(REP_PROJET)
    print("=" * 60)
    print("PIPELINE ÉVOLUTION – Tarification dynamique")
    print("=" * 60)
    print(f"Répertoire d'écriture : {REP_PROJET.resolve()}")
    print("(Les 4 fichiers seront créés dans ce dossier.)\n")

    # 1. Config de base (m01 → config.json)
    print("\n>>> m01_config.py")
    code = run_script("m01_config.py")
    if code != 0:
        print(f"[ÉCHEC] m01_config.py a retourné {code}.")
        return code

    # 2. Chaîne m02c → m02d → m03b → m04 → m05 → m06 → m07 → m08 → m09 (en processus)
    print("\n>>> Chaîne m02c → m02e → m02d → m03b → m04 … m09")
    sys.path.insert(0, str(REP_PROJET))
    from m00_config_etendue import get_config_etendue
    from m02b_types_chambre_calendrier import get_types_chambre, get_coefficient_mois
    import m02c_reservations_avec_dates
    import m02e_saison_calendrier
    import m02d_allocation_chambres
    import m03b_revenus_chambre_dynamique
    import m04_revenus_centres_profit
    import m05_type_forfait
    import m06_satisfaction_nps
    import m07_total_facture
    import m08_anomalies_pedagogiques
    import m09_export_csv

    get_config_etendue()
    get_types_chambre()
    get_coefficient_mois(1)

    df = m02c_reservations_avec_dates.run()
    df = m02e_saison_calendrier.run(df)
    df = m02d_allocation_chambres.run(df)
    df = m03b_revenus_chambre_dynamique.run(df)
    df = m04_revenus_centres_profit.run(df)
    df = m05_type_forfait.run(df)
    df = m06_satisfaction_nps.run(df)
    df = m07_total_facture.run(df)
    df = m08_anomalies_pedagogiques.run(df)
    df, chemin_csv = m09_export_csv.run(df)
    print(f"  CSV exporté : {chemin_csv} ({len(df)} lignes)")

    colonnes_attendues = ["Type_chambre", "Numero_chambre", "Sexe", "Niveau_revenus", "Pays", "Province", "Ville", "Rev_Chambre", "Saison_calendrier"]
    manquantes = [c for c in colonnes_attendues if c not in df.columns]
    if manquantes:
        print(f"  [ATTENTION] Colonnes absentes du CSV : {manquantes}")
    else:
        print("  Colonnes évolution présentes : OK")

    # 3. Rapport de validation (m10 lit le CSV)
    print("\n>>> m10_rapport_validation.py")
    code = run_script("m10_rapport_validation.py")
    if code != 0:
        print(f"[ÉCHEC] m10 a retourné {code}.")
        return code

    # 4. Synthèse Word (m11)
    print("\n>>> m11_synthese_word_prof.py")
    code = run_script("m11_synthese_word_prof.py")
    if code != 0:
        print(f"[ÉCHEC] m11 a retourné {code}.")
        return code

    print("\n" + "=" * 60)
    print("Pipeline évolution terminé avec succès.")
    print("=" * 60)
    rep = REP_PROJET.resolve()
    for nom in ["config.json", "sondage_hotel_data.csv", "rapport_validation_sondage_hotel.xlsx", "synthese_elements_apprentissage_prof.docx"]:
        chemin = rep / nom
        existe = " (créé)" if chemin.exists() else " [ABSENT]"
        print(f"  {nom}  →  {chemin}{existe}")
    print("=" * 60)
    print("Pour les ouvrir dans le Finder : ouvrir → Aller au dossier → coller le chemin ci‑dessus.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
