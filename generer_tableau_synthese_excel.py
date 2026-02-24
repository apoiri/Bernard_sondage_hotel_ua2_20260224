# -*- coding: utf-8 -*-
"""
Génère un fichier Excel contenant le tableau synthèse des techniques statistiques
à l'intention des professeurs et experts (clients).

Usage : python3 generer_tableau_synthese_excel.py
        Sortie : tableau_synthese_techniques_statistiques.xlsx (dans le dossier du script)
"""

from pathlib import Path
import pandas as pd

REP = Path(__file__).resolve().parent
FICHIER_SORTIE = REP / "tableau_synthese_techniques_statistiques.xlsx"

# Ordre des colonnes (la dernière met en avant l'impact pour le gestionnaire)
COLONNES = [
    "Technique",
    "Ce que la technique permet de déceler",
    "Formule(s) utilisée(s)",
    "Résultats obtenus",
    "Explication sommaire",
    "Impact sur la prise de décision (gestionnaire)",
]

# Données du tableau (une ligne par technique)
LIGNES = [
    {
        "Technique": "Proportions et intervalle de confiance 95 %",
        "Ce que la technique permet de déceler": "Estimer la part d'une catégorie dans la population (ex. % d'annulations) et la précision de cette estimation (IC 95 %).",
        "Formule(s) utilisée(s)": "p ± 1,96 × √(p(1−p)/n) (approximation normale pour une proportion).",
        "Résultats obtenus": "% Annulées : 18,7 % [18,0 % ; 19,5 %]. % Rev_Spa > 0 : 52,3 % [51,4 % ; 53,3 %]. % Forfait Gastronomique : 42,1 % [41,1 % ; 43,0 %].",
        "Explication sommaire": "Les proportions observées sont cohérentes avec les hypothèses de la simulation. Les IC confirment une estimation stable grâce à un grand échantillon.",
        "Impact sur la prise de décision (gestionnaire)": "Fixer des objectifs réalistes (taux d'annulation, pénétration spa, forfaits) et suivre les écarts ; base pour le pilotage opérationnel et la rentabilité.",
    },
    {
        "Technique": "Test du Khi-deux (indépendance)",
        "Ce que la technique permet de déceler": "Déceler une liaison entre deux variables catégorielles (Segment et Type de forfait) : les segments ont-ils des comportements différents selon le forfait ?",
        "Formule(s) utilisée(s)": "χ² = Σ (O − E)² / E ; O = effectifs observés, E = attendus sous indépendance. ddl = (lignes − 1)(colonnes − 1).",
        "Résultats obtenus": "Khi² = 2841,56 ; ddl = 4 ; p-value ≈ 0,000.",
        "Explication sommaire": "Liaison très significative : le type de forfait est fortement associé au segment (ex. Loisirs → plus Forfait Gastronomique, Congressiste → plus Chambre seule).",
        "Impact sur la prise de décision (gestionnaire)": "Cibler l'offre (forfaits) par segment pour maximiser l'adhésion et les revenus ; personnaliser la communication et les tarifs selon le profil client.",
    },
    {
        "Technique": "Corrélation de Pearson",
        "Ce que la technique permet de déceler": "Mesurer la relation linéaire entre deux variables numériques (revenus Spa et satisfaction NPS).",
        "Formule(s) utilisée(s)": "r = Cov(X,Y) / (s_X × s_Y). Calcul sur réservations non annulées, sans NaN.",
        "Résultats obtenus": "r = 0,45 ; p-value ≈ 0,000 ; n = 8121.",
        "Explication sommaire": "Corrélation positive significative : plus les revenus Spa sont élevés, plus la satisfaction NPS tend à être élevée. r < 0,75 reflète le bruit volontaire dans la simulation.",
        "Impact sur la prise de décision (gestionnaire)": "Identifier les leviers satisfaction (ex. Spa) pour la fidélisation et la rentabilité ; investir dans les services qui améliorent la satisfaction et le panier moyen.",
    },
    {
        "Technique": "ANOVA à un facteur",
        "Ce que la technique permet de déceler": "Déceler des différences de moyennes d'une variable quantitative (Rev_Resto) entre plusieurs groupes (segments).",
        "Formule(s) utilisée(s)": "F = (variance inter-groupes / ddl₁) / (variance intra-groupes / ddl₂). Test F de Fisher.",
        "Résultats obtenus": "F = 10 362,84 ; p-value ≈ 0,000.",
        "Explication sommaire": "Les dépenses restaurant diffèrent significativement selon le segment. Les étudiants peuvent interpréter quels segments dépensent le plus au restaurant.",
        "Impact sur la prise de décision (gestionnaire)": "Allouer les ressources (restaurant, menus, promotions) selon les segments qui dépensent le plus ; optimiser la rentabilité par centre de profit et par cible.",
    },
    {
        "Technique": "Régression linéaire multiple",
        "Ce que la technique permet de déceler": "Expliquer la facture totale à partir des revenus par poste (Chambre, Resto, Spa) et vérifier la cohérence du modèle de tarification.",
        "Formule(s) utilisée(s)": "Total_Facture = β₀ + β₁·Rev_Chambre + β₂·Rev_Resto + β₃·Rev_Spa + ε. MCO. R² = 1 − (SCR / SCT).",
        "Résultats obtenus": "Constante ≈ 2,35 ; Rev_Chambre ≈ 1,00 ; Rev_Resto ≈ 1,08 ; Rev_Spa ≈ 1,30 ; R² ≈ 0,9997 ; n = 9499.",
        "Explication sommaire": "Les coefficients sont proches du modèle théorique (1 ; 1,1 ; 1,3). La facture totale est quasi parfaitement expliquée par les revenus, ce qui valide la structure pour l'exercice de régression.",
        "Impact sur la prise de décision (gestionnaire)": "Piloter la structure des revenus (chambre, resto, spa) et détecter les dérives de tarification ou de coûts ; assurer la cohérence du modèle économique et la rentabilité globale.",
    },
    {
        "Technique": "Taux d'annulation par canal",
        "Ce que la technique permet de déceler": "Comparer le risque d'annulation entre réservations directes et intermédiaires (OTA).",
        "Formule(s) utilisée(s)": "Taux = (nombre d'annulées dans le groupe) / (nombre total dans le groupe).",
        "Résultats obtenus": "Taux Direct : 6,8 % ; Taux Intermédiaire : 30,5 %. (Attendus simulation : ~7 % et ~29 %.)",
        "Explication sommaire": "Les taux observés sont proches des paramètres de la simulation. Les intermédiaires affichent un taux d'annulation nettement plus élevé que le direct.",
        "Impact sur la prise de décision (gestionnaire)": "Choisir les canaux (direct vs OTA), négocier les commissions et gérer le risque de no-show ; impact direct sur le taux d'occupation réel et la rentabilité (réduction des annulations = meilleure prévisibilité).",
    },
    {
        "Technique": "Contrôle qualité (anomalies pédagogiques)",
        "Ce que la technique permet de déceler": "Vérifier la présence des anomalies volontairement injectées pour les exercices de nettoyage (incohérences, outliers, manquants, doublons).",
        "Formule(s) utilisée(s)": "Comptages : Externes avec Nuits > 0 ; NPS = 99 ; valeurs manquantes Rev_Spa / Rev_Resto ; doublons = total − lignes uniques.",
        "Résultats obtenus": "Externes Nuits>0 : 15 ; NPS = 99 : 3 ; Manquants Rev_Spa : 526 (5,0 %) ; Rev_Resto : 526 (5,0 %) ; Doublons : 10.",
        "Explication sommaire": "Les anomalies sont présentes aux niveaux prévus. Le jeu est adapté pour faire travailler les étudiants sur la détection et le traitement des incohérences, manquants et doublons.",
        "Impact sur la prise de décision (gestionnaire)": "S'assurer de la fiabilité des données avant toute décision ; éviter des choix basés sur des erreurs ou des doublons, et améliorer la qualité du pilotage et du reporting.",
    },
]


def main():
    df = pd.DataFrame(LIGNES)[COLONNES]
    df.to_excel(FICHIER_SORTIE, sheet_name="Synthese_techniques", index=False, engine="openpyxl")
    print(f"Fichier généré : {FICHIER_SORTIE}")
    return FICHIER_SORTIE


if __name__ == "__main__":
    main()
