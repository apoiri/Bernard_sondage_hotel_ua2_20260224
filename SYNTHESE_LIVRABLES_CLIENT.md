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

---

### 4. **synthese_elements_apprentissage_prof.docx**
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
| **synthese_elements_apprentissage_prof.docx** | Pédagogie | Liste des objectifs d’apprentissage et couverture (pour le professeur). |

---

## Ordre suggéré pour une livraison type

1. **sondage_hotel_data.csv** – les données.
2. **rapport_validation_sondage_hotel.xlsx** – preuve que les calculs et la structure sont validés.
3. **tableau_synthese_techniques_statistiques.xlsx** – synthèse lisible avec impact gestionnaire.
4. **synthese_elements_apprentissage_prof.docx** – guide pédagogique pour le professeur.

Vous pouvez remettre les quatre fichiers ensemble ou adapter selon le besoin du client (données seules, données + rapport, ou package complet avec synthèse et document professeur).
