# -*- coding: utf-8 -*-
"""
Pipeline de validation – Orchestrateur m01 → m09 → m10 → m11
Simulation « L'Hôtel Boutique Art de Vivre »

Enchaîne l'exécution des modules pour produire :
  - config.json (m01)
  - sondage_hotel_data.csv (m09, qui enchaîne m02–m08)
  - rapport_validation_sondage_hotel.xlsx (m10)
  - synthese_elements_apprentissage_prof.docx (m11)

Puis exécute les vérifications des livrables (RÈGLE DE BLOCAGE, présence des sorties).
Usage : python run_pipeline.py
"""

import subprocess
import sys
from pathlib import Path

# Répertoire du projet (où se trouvent les m*.py)
REP_PROJET = Path(__file__).resolve().parent

MODULES_PIPELINE = [
    "m01_config.py",
    "m09_export_csv.py",
    "m10_rapport_validation.py",
    "m11_synthese_word_prof.py",
]

FICHIERS_SORTIE_ATTENDUS = [
    "config.json",
    "sondage_hotel_data.csv",
    "rapport_validation_sondage_hotel.xlsx",
    "synthese_elements_apprentissage_prof.docx",
]

NOMBRE_MODULES_AVEC_REGLE_BLOCAGE = 14  # m01..m11 + m02b, m02c, m02d, m03b


def run_module(script: str) -> int:
    """Exécute un module Python ; retourne le code de sortie."""
    p = subprocess.run(
        [sys.executable, script],
        cwd=REP_PROJET,
        capture_output=False,
    )
    return p.returncode


def verifier_regle_blocage() -> bool:
    """Vérifie que les modules m*.py contiennent la RÈGLE DE BLOCAGE."""
    import glob
    pattern = str(REP_PROJET / "m*.py")
    fichiers = sorted(glob.glob(pattern))
    count = 0
    for f in fichiers:
        if "RÈGLE DE BLOCAGE" in Path(f).read_text(encoding="utf-8"):
            count += 1
    return count == NOMBRE_MODULES_AVEC_REGLE_BLOCAGE


def verifier_fichiers_sortie() -> bool:
    """Vérifie que tous les fichiers de sortie attendus existent."""
    for nom in FICHIERS_SORTIE_ATTENDUS:
        if not (REP_PROJET / nom).exists():
            return False
    return True


def main() -> int:
    print("=" * 60)
    print("PIPELINE DE VALIDATION – Sondage Hôtel")
    print("=" * 60)

    for script in MODULES_PIPELINE:
        print(f"\n>>> Exécution : {script}")
        code = run_module(script)
        if code != 0:
            print(f"\n[ÉCHEC] {script} a retourné le code {code}. Arrêt du pipeline.")
            return code

    print("\n" + "=" * 60)
    print("VÉRIFICATIONS DES LIVRABLES")
    print("=" * 60)

    ok_blocage = verifier_regle_blocage()
    print(f"  RÈGLE DE BLOCAGE dans m*.py (attendu {NOMBRE_MODULES_AVEC_REGLE_BLOCAGE}) : {'OK' if ok_blocage else 'ÉCHEC'}")

    ok_sortie = verifier_fichiers_sortie()
    print(f"  Fichiers de sortie présents : {'OK' if ok_sortie else 'ÉCHEC'}")
    if not ok_sortie:
        for nom in FICHIERS_SORTIE_ATTENDUS:
            present = (REP_PROJET / nom).exists()
            print(f"    - {nom} : {'oui' if present else 'NON TROUVÉ'}")

    if not ok_blocage or not ok_sortie:
        print("\n[ÉCHEC] Une ou plusieurs vérifications ont échoué.")
        return 1

    # Preuve : chemin et date du CSV généré
    import os
    from datetime import datetime
    chemin_csv = REP_PROJET / "sondage_hotel_data.csv"
    if chemin_csv.exists():
        mtime = os.path.getmtime(chemin_csv)
        date_modif = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        print("\n--- Fichier CSV généré ---")
        print(f"  Chemin : {chemin_csv.resolve()}")
        print(f"  Dernière modification : {date_modif}")

    print("\n[OK] Pipeline terminé avec succès. Toutes les vérifications sont passées.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
