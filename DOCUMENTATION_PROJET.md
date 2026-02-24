# Documentation du projet – L'Hôtel Boutique Art de Vivre

**Dernière mise à jour :** 24 février 2026  
**Objet :** Simulation de données de sondage pour la formation (analyse statistique, prise de décision). Ce document décrit l'état du projet, le blocage des modules, les pipelines et les livrables.

---

## 1. Blocage des modules

Les modules suivants contiennent la **RÈGLE DE BLOCAGE** en fin de fichier. Aucune modification n'est acceptée sans l'autorisation du maître d'ouvrage.

| Module | Rôle |
|--------|------|
| m01_config.py | Configuration (config.json, hypothèses simulation) |
| m02_segments.py | Base réservations (segment, canal, annulation) |
| m02c_reservations_avec_dates.py | Dates, Mois_sejour, type chambre (pipeline évolution) |
| m02e_saison_calendrier.py | Saison_calendrier (Basse/Épaule/Haute) dérivée du mois |
| m02d_allocation_chambres.py | Allocation chambres, numéro (pipeline évolution) |
| m03_nuits_chambre.py | Nuits, Rev_Chambre (pipeline classique) |
| m03b_revenus_chambre_dynamique.py | Rev_Chambre, Tarif_applique (tarification dynamique) |
| m04_revenus_centres_profit.py | Rev_Banquet, Rev_Resto, Rev_Spa |
| m05_type_forfait.py | Type_Forfait |
| m06_satisfaction_nps.py | Satisfaction_NPS |
| m07_total_facture.py | Total_Facture |
| m08_anomalies_pedagogiques.py | Anomalies (doublons, NPS=99, manquants, incohérences) |
| m09_export_csv.py | Export sondage_hotel_data.csv |
| m10_rapport_validation.py | Rapport Excel de validation |
| m11_synthese_word_prof.py | Synthèse Word professeur (éléments d'apprentissage) |

**Total : 15 modules** avec RÈGLE DE BLOCAGE.  
**Sans blocage (par convention) :** m00_config_etendue.py, m02b_types_chambre_calendrier.py.

**Vérification :** `run_pipeline.py` exécute une vérification du nombre de modules contenant « RÈGLE DE BLOCAGE » (attendu : 15).

---

## 2. Pipelines

### Pipeline classique (`run_pipeline.py`)
- **Séquence :** m01 → m09 (m09 enchaîne m02 → m03 → … → m08 en interne) → m10 → m11.
- **Sorties :** config.json, sondage_hotel_data.csv, rapport_validation_sondage_hotel.xlsx, synthese_elements_apprentissage_prof.docx.

### Pipeline évolution – tarification dynamique (`run_pipeline_evolution.py`)
- **Séquence :** m01 → m02c → m02e → m02d → m03b → m04 → … → m09 → m10 → m11.
- **Spécificités :** types de chambre, Mois_sejour, coefficients par mois, Rev_Chambre/Tarif_applique dynamiques, colonne Saison_calendrier.
- **Sorties :** mêmes fichiers que le pipeline classique (écrasés).

**Lancer depuis le répertoire du projet** (Terminal) pour que les fichiers soient bien écrits au bon endroit.

---

## 3. Livrables principaux (client / professeur)

| Fichier | Description |
|---------|-------------|
| **sondage_hotel_data.csv** | Données principales (~10 500 lignes, 25 variables). |
| **rapport_validation_sondage_hotel.xlsx** | Validation statistique (proportions, Khi-deux, Pearson, ANOVA, régression, anomalies). |
| **synthese_elements_apprentissage_prof.docx** | Éléments d'apprentissage, anomalies, synthèse du rapport de validation, checklist prof. |
| **RAPPORT_DETAILLE_VALIDATION_ANALYSES.md** | Rapport détaillé par technique (résultats, interprétation, décision). |
| **Note_Saison_vs_Tarification_Dynamique.docx** | Saison vs Saison_calendrier, tarification active (pour le client). |

Voir **SYNTHESE_LIVRABLES_CLIENT.md** pour la liste complète et l'ordre de remise.

---

## 4. Documentation du dossier (référence)

| Document | Contenu |
|----------|---------|
| **DOCUMENTATION_PROJET.md** | Ce fichier : blocage, pipelines, livrables, état du projet. |
| **CHAINAGE_MODULES_m01_a_m09.md** | Détail du traitement de chaque module (m01 à m09 + évolution). |
| **VERIFICATION_LIVRABLES.md** | Vérifications à effectuer après exécution des pipelines. |
| **RAPPORT_DETAILLE_VALIDATION_ANALYSES.md** | Validation des analyses et appui à la prise de décision. |
| **NOTE_SAISON_VS_TARIFICATION_DYNAMIQUE.md** | Différence Saison / Saison_calendrier, usage pour la tarification active. |
| **SYNTHESE_LIVRABLES_CLIENT.md** | Liste des livrables à remettre au client. |
| **COMPTE_RENDU_DERNIERS_CHANGEMENTS.md** | Compte rendu des derniers changements (Saison_calendrier, m02e, etc.). |

---

## 5. Modules validés

La liste des modules validés est dans **validated_modules.txt** (m00, m01, m02, m02b, m02c, m02e, m02d, m03, m03b, m04–m11, interfaces, run_pipeline_evolution).

---

*Projet : Bernard_sondage_hotel_ua2_20260224 – Simulation L'Hôtel Boutique Art de Vivre.*
