# Archive – Projet « L'Hôtel Boutique Art de Vivre » (Sondage – Marketing)

**Date d'archivage** : 2025-02-17  
**Objectif** : Conserver une trace de la discussion, des décisions et du développement pour permettre des modifications ou améliorations ultérieures.

---

## 1. Contexte et objectifs du projet

- **Commande** : Préparer un jeu de données de réservations hôtelières (simulation) pour des **étudiants en marketing-sondage**, afin qu’ils pratiquent les **techniques statistiques d’analyse de sondage** et produisent des **informations pour la prise de décision**.
- **Public** : Professeur et étudiants ; le professeur doit pouvoir s’assurer que **tous les éléments d’apprentissage** prévus sont réalisables avec le fichier.
- **Livrables** :  
  - Fichier de données **sondage_hotel_data.csv** (environ 10 500+ lignes).  
  - Rapport de validation **Excel** (statistiques, tests, verdicts).  
  - **Synthèse Word** à l’intention du professeur (éléments d’apprentissage, checklist).  
  - Option : détail « information fine » (nourriture, spa) et format multi-onglets Excel (évoqué en début de projet ; non implémenté dans la première version, le cœur étant la génération CSV + validation + synthèse prof).

---

## 2. Décisions prises pendant la discussion

| Décision | Détail |
|----------|--------|
| **Nombre de chambres** | **100 chambres** (fixe, non modifiable). |
| **Taux d’occupation** | **72 %** en moyenne sur l’année. |
| **Nombre de réservations** | Une année complète : **N = ceil(100 × 365 × 0,72 / 2,5) = 10 512** réservations. |
| **Annulations** | Taux annuel **18 %** ; **7 %** pour réservations directes, **29 %** pour intermédiaires ; **50 %** direct / **50 %** intermédiaires. |
| **Canaux de réservation** | Direct : Site Web, Courriel, Téléphone. Intermédiaires : Booking.com, Expedia, Hotels.com, Trivago, Trip.com, TripAdvisor, Google, Airbnb, Autre OTA. |
| **Format de sortie** | **CSV** principal ; rapport de validation en **Excel** ; synthèse pédagogique en **Word**. |
| **Structure modulaire** | **11 modules** (config → génération → export → rapport → synthèse Word) ; chaque module = un fichier Python ; **blocage** possible par module pour éviter les modifications non voulues. |
| **Hypothèses modifiables** | En **tête de chaque script** : bloc d’hypothèses (paramètres) que l’opérateur peut modifier sans toucher au reste du code. |
| **Rapport de validation** | En **fin de traitement** : affichage **terminal** + fichier **Excel** avec descriptif, proportions/IC, Khi-deux, Pearson, ANOVA, régression, annulations par canal, contrôle qualité (anomalies). |
| **Anomalies pédagogiques** | Incohérences (Externes avec Nuits > 0), outliers (NPS = 99), valeurs manquantes (Rev_Spa, Rev_Resto), doublons — pour exercice de **data cleaning**. |

---

## 3. Fichiers du développement (emplacement et rôle)

**Répertoire principal** : `Bernard_sondage_hotel_ua2_20260224/` (ou chemin indiqué dans le plan).

| Fichier | Rôle | Statut |
|---------|------|--------|
| **PLAN_DEVELOPPEMENT_SONDAGE_HOTEL_MODULES.md** | Plan officiel du projet (spec, modules, verrouillage). Référence pour toute évolution. | Document maître |
| **m01_config.py** | Configuration : 100 chambres, 72 %, segments, annulations, canaux, formules, anomalies. Sortie : `get_config()`, `config.json`. | Bloqué |
| **m02_segments.py** | Génération ID_Client, Segment, Type_Client, Saison, Canal_reservation, Type_canal, Annulee. | Bloqué |
| **m03_nuits_chambre.py** | Nuits (Poisson si Interne non annulé), Rev_Chambre. | Bloqué |
| **m04_revenus_centres_profit.py** | Rev_Banquet, Rev_Resto, Rev_Spa (par segment ; ANOVA sur Rev_Resto). | Bloqué |
| **m05_type_forfait.py** | Type_Forfait (Forfait Gastronomique / Chambre Seule) pour Khi-deux. | Bloqué |
| **m06_satisfaction_nps.py** | Satisfaction_NPS (formule + corrélation avec Rev_Spa) ; NaN si Annulee = Oui. | Bloqué |
| **m07_total_facture.py** | Total_Facture = Rev_Chambre + 1,1×Rev_Resto + 1,3×Rev_Spa + ε. | Bloqué |
| **m08_anomalies_pedagogiques.py** | Anomalies : 15 Externes Nuits>0, 3 NPS=99, 5 % manquants, 10 doublons. | Bloqué |
| **m09_export_csv.py** | Types de données, export **sondage_hotel_data.csv**. | Bloqué |
| **m10_rapport_validation.py** | Analyses statistiques complètes ; sortie **terminal** + **rapport_validation_sondage_hotel.xlsx**. | Bloqué |
| **m11_synthese_word_prof.py** | Synthèse **Word** pour le professeur : éléments d’apprentissage, variables, anomalies, checklist. Sortie : **synthese_elements_apprentissage_prof.docx**. | En cours |
| **config.json** | Config exportée (générée par m01_config.py). | Dépend de m01 |
| **sondage_hotel_data.csv** | Fichier de travail pour les étudiants (généré par m09). | Produit par pipeline |
| **rapport_validation_sondage_hotel.xlsx** | Rapport de validation (généré par m10). | Produit par pipeline |
| **synthese_elements_apprentissage_prof.docx** | Document Word pour le professeur (généré par m11). | Produit par m11 |

**Documents connexes** (racine Cursor ou dossier projet) :  
- **PROJET_DONNEES_HOTEL_MARKETING_SONDAGE.md** : objectifs initiaux, structure données, options A/B.  
- **ANALYSE_FICHIER_HOTEL_ET_FORMAT_SORTIE.md** : analyse du fichier Excel existant « Hotel de la Promenade », format multi-onglets / CSV, gestion du détail (nourriture, spa).

---

## 4. Enchaînement des modules et exécution

- **Ordre logique** : 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11.  
- **Exécution manuelle** : lancer chaque script depuis le répertoire du projet (ex. `python3 m01_config.py`, puis `m02_segments.py`, etc.) ; les modules 2–11 lisent la config (m01) ou la sortie du module précédent.  
- **Orchestrateur** : prévu **run_pipeline.py** (Module 0) pour enchaîner 1 à 11 en une seule commande ; non implémenté dans cette version — à ajouter si besoin.

---

## 5. Règles de blocage et évolution

- Un module **bloqué** ne doit **pas être modifié** sans demande explicite de déblocage.  
- Toute évolution qui toucherait à un module bloqué se fait soit par **déblocage**, soit dans un **nouveau fichier** (ex. m04b_ajustement.py) qui s’enchaîne après le module concerné.  
- Les **hypothèses** (paramètres) sont regroupées en **tête de chaque script** pour que l’opérateur puisse les modifier sans toucher à la logique.

---

## 6. Pistes d’amélioration ou de modification

- **Orchestrateur** : créer `run_pipeline.py` pour exécuter d’un coup m01 → m11 et produire CSV + Excel + Word.  
- **Détail « information fine »** : si besoin, ajouter des modules ou scripts qui génèrent des tables **détail_nourriture** et **détail_spa** (lignes de facture) à partir des montants Rev_Resto et Rev_Spa, avec sortie Excel multi-onglets ou CSV séparés.  
- **Volume** : le nombre de réservations (10 512) est fixé par la config (m01) ; modifier **DUREE_MOYENNE_SEJOUR** ou **NB_CHAMBRES** (si déblocage) pour changer le volume.  
- **Synthèse Word** : le contenu du document (éléments d’apprentissage, tableau, checklist) est dans **m11_synthese_word_prof.py** ; modifier ce script pour adapter le texte ou les sections (après déblocage si le module est bloqué).

---

## 7. Dépendances techniques

- **Python 3** avec **pandas**, **numpy**, **scipy** (pour ANOVA, Khi-deux, Pearson, régression).  
- **openpyxl** pour l’export Excel (m10).  
- **python-docx** pour l’export Word (m11) : `pip install python-docx`.

---

*Archive créée le 2025-02-17. Pour toute modification ou amélioration, s’appuyer sur ce document et sur **PLAN_DEVELOPPEMENT_SONDAGE_HOTEL_MODULES.md**.*
