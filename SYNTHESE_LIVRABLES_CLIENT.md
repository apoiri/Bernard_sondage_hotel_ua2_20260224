# Synthèse des livrables – À remettre au client (professeurs / experts)

Ce document décrit les **fichiers que vous pouvez utiliser et donner à votre client**, avec un court descriptif de chaque livrable.

---

## Fichiers à remettre au client

### 1. **sondage_hotel_data.csv**
- **Quoi :** Fichier de données principal (environ 10 500 réservations simulées).
- **Contenu :** Une ligne par réservation : ID_Client, Segment, Type_Client, Saison, Canal_reservation, Type_canal, Annulee, Nuits, revenus (Chambre, Banquet, Resto, Spa), Type_Forfait, Satisfaction_NPS, Total_Facture. Encodage UTF-8, séparateur point-virgule.
- **Usage client :** Les étudiants l’utilisent pour faire les exercices d’analyse (proportions, Khi-deux, Pearson, ANOVA, régression, nettoyage des anomalies). Le professeur peut l’ouvrir dans Excel ou l’importer dans R/Python pour vérifier ou démontrer.
- **À donner si :** Vous livrez le jeu de données pour les travaux pratiques.

---

### 2. **rapport_validation_sondage_hotel.xlsx**
- **Quoi :** Rapport Excel de validation des calculs et de la structure des données.
- **Contenu :** Plusieurs onglets : statistiques descriptives, effectifs par segment/annulation, proportions et IC 95 %, tableau et résultat Khi-deux, Pearson, ANOVA, régression, annulations par canal, contrôle qualité (anomalies). Chaque onglet contient les chiffres et résultats des tests.
- **Usage client :** Le professeur ou l’expert vérifie que les analyses sont cohérentes (liaison segment/forfait, coefficients de régression, taux d’annulation, anomalies pédagogiques). Référence pour valider les réponses des étudiants ou pour une relecture critique.
- **À donner si :** Le client doit pouvoir contrôler la qualité statistique et la cohérence des données.

---

### 3. **tableau_synthese_techniques_statistiques.xlsx**
- **Quoi :** Tableau synthèse (une ligne par technique statistique).
- **Contenu :** Colonnes : Technique | Ce que la technique permet de déceler | Formule(s) utilisée(s) | Résultats obtenus | Explication sommaire | **Impact sur la prise de décision (gestionnaire)**. Couvre les 7 techniques du rapport (proportions/IC, Khi-deux, Pearson, ANOVA, régression, taux d’annulation, contrôle qualité).
- **Usage client :** Vue d’ensemble pour le professeur ou l’expert : objectif de chaque technique, formules, résultats et interprétation, **plus la valeur pour le gestionnaire** (pilotage, rentabilité, qualité des décisions). Idéal pour une présentation ou un document d’accompagnement.
- **À donner si :** Vous voulez mettre en avant l’utilité des analyses pour la prise de décision et la rentabilité de l’hôtel.
- **Génération :** `python3 generer_tableau_synthese_excel.py` (à lancer depuis le dossier du projet).

---

### 4. **RAPPORT_DETAILLE_VALIDATION_ANALYSES.md** (rapport détaillé pour validation)
- **Quoi :** Rapport détaillé par technique : résultats constatés, interprétation, **leçons à retenir**, **information pour la prise de décision (gestionnaire)**.
- **Contenu :** Pour chaque technique (proportions/IC, Khi-deux, Pearson, ANOVA, régression, annulations par canal, contrôle qualité) : objectif, formule, résultats, interprétation, leçons retenues, appui à la décision. Introduction sur la validité des données et synthèse pour professeurs et client.
- **Usage client :** Démontrer aux **professeurs et au client** que les données sont **valides**, que les analyses sont **cohérentes**, et que chaque technique fournit des **indications pour la formation des étudiants** et pour la **prise de décision en entreprise**. Document de référence pour la reddition et la validation pédagogique.
- **À donner si :** Vous devez **prouver la qualité et l’usage pédagogique** des données et soutenir la formation des étudiants. Peut être exporté en PDF ou Word pour remise officielle.

---

### 5. **synthese_elements_apprentissage_prof.docx**
- **Quoi :** Document Word à l’intention du professeur (synthèse pédagogique).
- **Contenu :** Description du jeu de données, variables principales, et un tableau listant les **éléments d’apprentissage** : chaque technique ou objectif pédagogique, les variables à utiliser, le type de sortie attendu, avec des cases à cocher. Permet de s’assurer que tous les objectifs (proportions, IC, Khi-deux, Pearson, ANOVA, régression, décision, nettoyage) sont couverts.
- **Usage client :** Le professeur s’en sert pour construire ou vérifier les exercices et pour s’assurer que le fichier de données permet bien de couvrir le programme.
- **À donner si :** Vous livrez un support pédagogique pour concevoir les séances et les évaluations.

---

## Récapitulatif rapide

| Fichier | Type | Rôle principal |
|---------|------|----------------|
| **sondage_hotel_data.csv** | Données | Jeu de données pour les étudiants (travaux pratiques). |
| **rapport_validation_sondage_hotel.xlsx** | Rapport | Validation statistique et qualité des données (pour contrôle expert). |
| **tableau_synthese_techniques_statistiques.xlsx** | Synthèse | Résumé des techniques + impact décisionnel (pour présentation / accompagnement). |
| **RAPPORT_DETAILLE_VALIDATION_ANALYSES.md** | Rapport détaillé | Résultats, leçons retenues, prise de décision ; validation professeurs et client. |
| **synthese_elements_apprentissage_prof.docx** | Pédagogie | Liste des objectifs d’apprentissage et couverture (pour le professeur). |

---

## Ordre suggéré pour une livraison type

1. **sondage_hotel_data.csv** – les données.
2. **rapport_validation_sondage_hotel.xlsx** – preuve que les calculs et la structure sont validés.
3. **tableau_synthese_techniques_statistiques.xlsx** – synthèse lisible avec impact gestionnaire (générer avec `python3 generer_tableau_synthese_excel.py`).
4. **RAPPORT_DETAILLE_VALIDATION_ANALYSES.md** – rapport détaillé (résultats, leçons retenues, prise de décision) pour validation professeurs et client ; exportable en PDF/Word.
5. **synthese_elements_apprentissage_prof.docx** – guide pédagogique pour le professeur.

Vous pouvez remettre les cinq documents ensemble ou adapter selon le besoin du client (données seules, données + rapport, ou package complet avec synthèse et document professeur).
