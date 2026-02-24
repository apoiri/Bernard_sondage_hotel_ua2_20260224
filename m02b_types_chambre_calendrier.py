# -*- coding: utf-8 -*-
"""
Module 02b – Types de chambre et calendrier (coefficients de tarification par mois)
Simulation « L'Hôtel Boutique Art de Vivre »

Lit la config étendue (m00), extrait les types de chambre et les 12 taux d'occupation,
calcule un coefficient de tarification par mois (forte occupation → coefficient > 1).
Expose get_types_chambre() et get_coefficient_mois(mois).
"""

from pathlib import Path

REP_PROJET = Path(__file__).resolve().parent

# Bornes et facteur pour le coefficient dynamique (occupation haute → prix plus élevé)
COEFF_MIN = 0.7
COEFF_MAX = 1.3
FACTEUR_SENSIBILITE = 2.0   # amplitude de la variation autour de 1


def get_config_etendue():
    import sys
    sys.path.insert(0, str(REP_PROJET))
    from m00_config_etendue import get_config_etendue as _get
    return _get()


def get_types_chambre():
    """
    Retourne la liste des types de chambre (nom, nb_chambres, prix_base).
    Si la config étendue n'a pas 'types_chambre', retourne un type unique par défaut.
    """
    c = get_config_etendue()
    if "types_chambre" in c and len(c["types_chambre"]) >= 1:
        return list(c["types_chambre"])
    return [{"nom": "Standard", "nb_chambres": 100, "prix_base": 250}]


def get_taux_occupation_mois():
    """Retourne les 12 taux d'occupation (janvier à décembre)."""
    c = get_config_etendue()
    if "taux_occupation_mois" in c and len(c["taux_occupation_mois"]) == 12:
        return list(c["taux_occupation_mois"])
    return [0.72] * 12


def get_coefficient_mois(mois):
    """
    Retourne le coefficient de tarification pour un mois (1 = janvier, 12 = décembre).
    Forte occupation → coefficient > 1 ; faible occupation → coefficient < 1.
    """
    taux_list = get_taux_occupation_mois()
    if not (1 <= mois <= 12):
        return 1.0
    taux = taux_list[mois - 1]
    moyen = sum(taux_list) / 12
    # Écart par rapport à la moyenne : au-dessus → coeff > 1
    coeff = 1.0 + (taux - moyen) * FACTEUR_SENSIBILITE
    return max(COEFF_MIN, min(COEFF_MAX, coeff))


def get_coefficients_annee():
    """Retourne la liste des 12 coefficients (mois 1 à 12)."""
    return [get_coefficient_mois(m) for m in range(1, 13)]
