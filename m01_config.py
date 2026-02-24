# -*- coding: utf-8 -*-
"""
Module 1 – Configuration et constantes
Simulation « L'Hôtel Boutique Art de Vivre »
Les modules 2 à 10 lisent cette config (get_config() ou config.json).
"""

import math
import json
from pathlib import Path

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
# Modifier les valeurs ci-dessous pour ajuster la génération.
# Les modules suivants importeront ce fichier ou liront config.json.

# --- Hôtel et volume ---
NB_CHAMBRES = 100                    # Fixe (projet) – ne pas modifier
# Taux industrie = moyenne des 12 taux mensuels (config_tarification_dynamique.json) ; si absent, défaut 0.73
# Écart vs industrie : +0.01 = hôtel 1 % au-dessus, -0.01 = 1 % en dessous
ECART_OCCUPATION_VS_INDUSTRIE = 0.01  # +1 % (performance plus élevée) ; mettre -0.01 pour plus bas
DUREE_MOYENNE_SEJOUR = 2.5          # Nuits (aligné sur λ Poisson du Module 3)

# --- Segments (personas) : noms et répartition en % ---
SEGMENTS_NOMS = [
    "Affaires_Solo",      # 25 %
    "Congressiste",       # 20 %
    "Loisirs_Couple",     # 25 %
    "Local_Gourmet",       # 20 %
    "Local_Spa",          # 10 %
]
SEGMENTS_POURCENTAGES = [25.0, 20.0, 25.0, 20.0, 10.0]  # même ordre que SEGMENTS_NOMS

# --- Annulations et canal ---
TAUX_ANNULATION_ANNUEL = 0.18       # 18 % global
TAUX_ANNULATION_DIRECT = 0.07       # 7 % pour réservations directes
TAUX_ANNULATION_INTERMEDIAIRE = 0.29  # 29 % pour intermédiaires (OTA)
PART_RESERVATIONS_DIRECT = 0.5      # 50 % direct, 50 % intermédiaires

# Canaux direct (répartition dans les 50 % direct)
CANAUX_DIRECT = [
    "Site Web de l'hôtel",
    "Courriel à l'hôtel",
    "Téléphone à l'hôtel",
]
CANAUX_DIRECT_POIDS = [0.40, 0.30, 0.30]  # 40 % / 30 % / 30 %

# Canaux intermédiaires (répartition dans les 50 % intermédiaires)
CANAUX_INTERMEDIAIRES = [
    "Booking.com",
    "Expedia",
    "Hotels.com",
    "Trivago",
    "Trip.com",
    "TripAdvisor",
    "Google",
    "Airbnb",
    "Autre OTA",
]
# Poids (part de marché approximative : Booking et Expedia plus élevés)
CANAUX_INTERMEDIAIRES_POIDS = [0.35, 0.20, 0.08, 0.06, 0.06, 0.05, 0.05, 0.05, 0.10]

# --- Saison par segment (probabilité Basse) : Congressiste surtout Basse, Loisirs surtout Haute ---
# Ordre : Affaires_Solo, Congressiste, Loisirs_Couple, Local_Gourmet, Local_Spa
PROBA_SAISON_BASSE_PAR_SEGMENT = [0.5, 0.8, 0.2, 0.5, 0.5]  # Congressiste 80 % Basse, Loisirs 20 % Basse (= 80 % Haute)

# --- Module 3 : Nuits et Rev_Chambre ---
LAMBDA_POISSON_NUITS = 2.5
MIN_NUITS = 1
MAX_NUITS = 14
TARIF_CHAMBRE_BASSE = 200           # $/nuit
TARIF_CHAMBRE_HAUTE = 350           # $/nuit

# --- Module 4 : Rev_Banquet, Rev_Resto, Rev_Spa ---
GAMMA_BANQUET_K = 2
GAMMA_BANQUET_THETA = 200
# Moyennes Rev_Resto par segment (Affaires_Solo, Congressiste, Loisirs_Couple, Local_Gourmet, Local_Spa)
MOYENNES_REV_RESTO_PAR_SEGMENT = [60, 45, 80, 150, 20]
# Moyennes Rev_Spa par segment (Local_Spa et Loisirs élevés, autres 0 ou faible)
MOYENNES_REV_SPA_PAR_SEGMENT = [0, 0, 180, 0, 120]

# --- Module 5 : Type_Forfait (Khi-deux) ---
# Probabilité "Forfait Gastronomique" par segment (sinon "Chambre Seule" ou "Autre")
PROBA_FORFAIT_GASTRONOMIQUE_PAR_SEGMENT = [0.3, 0.1, 0.8, 0.5, 0.2]  # Loisirs 80 %, Congressiste 10 %

# --- Module 6 : Satisfaction NPS ---
NPS_CONSTANTE = 8.0
NPS_EFFET_HAUTE_SAISON = -1.5
NPS_EFFET_REV_SPA_SUP_100 = 1.0
NPS_ECART_TYPE_BRUIT = 0.5
NPS_CORRELATION_REV_SPA = 0.75      # cible r ≈ 0,75

# --- Module 7 : Total_Facture ---
COEFF_REV_RESTO = 1.1
COEFF_REV_SPA = 1.3
ECART_TYPE_BRUIT_TOTAL = 10.0

# --- Module 8 : Anomalies pédagogiques ---
N_INCOHERENCES_EXTERNES_NUITS = 15  # Externes avec Nuits > 0
N_OUTLIERS_NPS = 3                  # Satisfaction_NPS = 99 (erreur de saisie)
PCT_MANQUANTS = 0.05                # 5 % de cellules vides Rev_Spa et Rev_Resto
N_DOUBLONS = 10                     # Lignes dupliquées

# --- Module 9 : Export ---
FICHIER_CSV_SORTIE = "sondage_hotel_data.csv"
ENCODAGE_CSV = "utf-8-sig"
SEPARATEUR_CSV = ";"

# --- Module 10 : Rapport de validation ---
FICHIER_RAPPORT_EXCEL = "rapport_validation_sondage_hotel.xlsx"

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

FICHIER_CONFIG_ETENDUE = Path(__file__).resolve().parent / "config_tarification_dynamique.json"


def _get_taux_industrie():
    """Taux d'occupation moyen industrie = moyenne des 12 taux mensuels (config étendue)."""
    if not FICHIER_CONFIG_ETENDUE.exists():
        return 0.73
    try:
        with open(FICHIER_CONFIG_ETENDUE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        taux_mois = cfg.get("taux_occupation_mois")
        if isinstance(taux_mois, list) and len(taux_mois) == 12:
            return round(sum(taux_mois) / 12, 4)
    except (json.JSONDecodeError, IOError, TypeError):
        pass
    return 0.73


def _get_taux_occupation():
    """Taux d'occupation cible de l'hôtel = industrie + ECART_OCCUPATION_VS_INDUSTRIE (± 1 %)."""
    return round(_get_taux_industrie() + ECART_OCCUPATION_VS_INDUSTRIE, 4)


def _calcul_n_reservations():
    """Calcule le nombre de réservations pour une année (taux = industrie ± 1 %)."""
    taux = _get_taux_occupation()
    nuits_an = NB_CHAMBRES * 365 * taux
    return int(math.ceil(nuits_an / DUREE_MOYENNE_SEJOUR))


def get_config():
    """
    Retourne un dictionnaire contenant toute la configuration.
    Les autres modules peuvent faire : from m01_config import get_config; config = get_config()
    """
    n_reservations = _calcul_n_reservations()
    taux_occ = _get_taux_occupation()
    taux_ind = _get_taux_industrie()
    return {
        "NB_CHAMBRES": NB_CHAMBRES,
        "TAUX_OCCUPATION": taux_occ,
        "TAUX_OCCUPATION_POURCENT": round(taux_occ * 100, 1),
        "TAUX_INDUSTRIE": taux_ind,
        "TAUX_INDUSTRIE_POURCENT": round(taux_ind * 100, 1),
        "DUREE_MOYENNE_SEJOUR": DUREE_MOYENNE_SEJOUR,
        "N_RESERVATIONS": n_reservations,
        "SEGMENTS_NOMS": list(SEGMENTS_NOMS),
        "SEGMENTS_POURCENTAGES": list(SEGMENTS_POURCENTAGES),
        "TAUX_ANNULATION_ANNUEL": TAUX_ANNULATION_ANNUEL,
        "TAUX_ANNULATION_DIRECT": TAUX_ANNULATION_DIRECT,
        "TAUX_ANNULATION_INTERMEDIAIRE": TAUX_ANNULATION_INTERMEDIAIRE,
        "PART_RESERVATIONS_DIRECT": PART_RESERVATIONS_DIRECT,
        "CANAUX_DIRECT": list(CANAUX_DIRECT),
        "CANAUX_DIRECT_POIDS": list(CANAUX_DIRECT_POIDS),
        "CANAUX_INTERMEDIAIRES": list(CANAUX_INTERMEDIAIRES),
        "CANAUX_INTERMEDIAIRES_POIDS": list(CANAUX_INTERMEDIAIRES_POIDS),
        "PROBA_SAISON_BASSE_PAR_SEGMENT": list(PROBA_SAISON_BASSE_PAR_SEGMENT),
        "LAMBDA_POISSON_NUITS": LAMBDA_POISSON_NUITS,
        "MIN_NUITS": MIN_NUITS,
        "MAX_NUITS": MAX_NUITS,
        "TARIF_CHAMBRE_BASSE": TARIF_CHAMBRE_BASSE,
        "TARIF_CHAMBRE_HAUTE": TARIF_CHAMBRE_HAUTE,
        "GAMMA_BANQUET_K": GAMMA_BANQUET_K,
        "GAMMA_BANQUET_THETA": GAMMA_BANQUET_THETA,
        "MOYENNES_REV_RESTO_PAR_SEGMENT": list(MOYENNES_REV_RESTO_PAR_SEGMENT),
        "MOYENNES_REV_SPA_PAR_SEGMENT": list(MOYENNES_REV_SPA_PAR_SEGMENT),
        "PROBA_FORFAIT_GASTRONOMIQUE_PAR_SEGMENT": list(PROBA_FORFAIT_GASTRONOMIQUE_PAR_SEGMENT),
        "NPS_CONSTANTE": NPS_CONSTANTE,
        "NPS_EFFET_HAUTE_SAISON": NPS_EFFET_HAUTE_SAISON,
        "NPS_EFFET_REV_SPA_SUP_100": NPS_EFFET_REV_SPA_SUP_100,
        "NPS_ECART_TYPE_BRUIT": NPS_ECART_TYPE_BRUIT,
        "NPS_CORRELATION_REV_SPA": NPS_CORRELATION_REV_SPA,
        "COEFF_REV_RESTO": COEFF_REV_RESTO,
        "COEFF_REV_SPA": COEFF_REV_SPA,
        "ECART_TYPE_BRUIT_TOTAL": ECART_TYPE_BRUIT_TOTAL,
        "N_INCOHERENCES_EXTERNES_NUITS": N_INCOHERENCES_EXTERNES_NUITS,
        "N_OUTLIERS_NPS": N_OUTLIERS_NPS,
        "PCT_MANQUANTS": PCT_MANQUANTS,
        "N_DOUBLONS": N_DOUBLONS,
        "FICHIER_CSV_SORTIE": FICHIER_CSV_SORTIE,
        "ENCODAGE_CSV": ENCODAGE_CSV,
        "SEPARATEUR_CSV": SEPARATEUR_CSV,
        "FICHIER_RAPPORT_EXCEL": FICHIER_RAPPORT_EXCEL,
    }


def save_config_json(filepath=None):
    """Sauvegarde la config dans un fichier JSON (optionnel)."""
    if filepath is None:
        filepath = Path(__file__).parent / "config.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(get_config(), f, ensure_ascii=False, indent=2)
    return filepath


def print_hypotheses():
    """Affiche les hypothèses en tête de traitement (pour l'opérateur)."""
    c = get_config()
    print("=" * 60)
    print("HYPOTHÈSES DU MODULE 1 (config)")
    print("=" * 60)
    print(f"  NB_CHAMBRES           = {c['NB_CHAMBRES']}")
    print(f"  TAUX_OCCUPATION       = {c['TAUX_OCCUPATION']} ({c['TAUX_OCCUPATION_POURCENT']} %, industrie {c['TAUX_INDUSTRIE_POURCENT']} % ± 1 %)")
    print(f"  DUREE_MOYENNE_SEJOUR  = {c['DUREE_MOYENNE_SEJOUR']} nuits")
    print(f"  N_RESERVATIONS        = {c['N_RESERVATIONS']} (calculé)")
    print(f"  Segments              = {c['SEGMENTS_NOMS']}")
    print(f"  Répartition %         = {c['SEGMENTS_POURCENTAGES']}")
    print(f"  Annulation direct     = {c['TAUX_ANNULATION_DIRECT']} ; intermédiaire = {c['TAUX_ANNULATION_INTERMEDIAIRE']}")
    print(f"  Part direct           = {c['PART_RESERVATIONS_DIRECT']}")
    print(f"  Canaux direct         = {c['CANAUX_DIRECT']}")
    print(f"  Canaux intermédiaires = {c['CANAUX_INTERMEDIAIRES'][:3]}... ({len(c['CANAUX_INTERMEDIAIRES'])} au total)")
    print(f"  Anomalies : incohérences={c['N_INCOHERENCES_EXTERNES_NUITS']}, NPS=99={c['N_OUTLIERS_NPS']}, manquants={c['PCT_MANQUANTS']*100}%, doublons={c['N_DOUBLONS']}")
    print("=" * 60)


if __name__ == "__main__":
    # Exécution directe : afficher les hypothèses et sauvegarder config.json
    print_hypotheses()
    out_path = save_config_json()
    print(f"Config sauvegardée dans : {out_path}")

# ========== RÈGLE DE BLOCAGE ==========
# Aucune modification de ce module n'est acceptée sans l'autorisation du maître d'ouvrage du projet.
