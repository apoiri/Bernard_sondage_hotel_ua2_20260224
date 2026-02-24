# Archive – Projet « L'Hôtel Boutique Art de Vivre » (Sondage – Marketing)

**Date d'archivage** : 2025-02-17  
**Objectif** : Conserver une trace de la discussion, des décisions et du développement pour permettre des modifications ou améliorations ultérieures.

---

## 1. Contexte, reprise et checklist (ne jamais repartir à zéro)

### Pourquoi cette section

Cursor ne retient pas les discussions entre les sessions. Si tu changes de répertoire, d’ordinateur ou que tu réactives une station de travail, **tout le contexte semble perdu**. Ce document et Git/GitHub sont ta mémoire de projet : en suivant la checklist ci-dessous, tu ne repartiras plus à zéro.

### Quand tu réactives une station de travail (Cursor)

1. **Ouvre le bon dossier dans Cursor**  
   Fichier → Ouvrir le dossier → `Bernard_sondage_hotel_ua2_20260224`  
   (ou le chemin actuel du projet sur cette machine).

2. **Récupère la dernière version depuis GitHub** (si le projet est déjà cloné ou déplacé) :
   ```bash
   cd "/Users/alainpoirier/Desktop/Bernard_sondage_hotel_ua2_20260224"
   git pull origin main
   ```

3. **Donne le contexte à Cursor en ouvrant ce fichier**  
   Ouvre **ARCHIVE_PROJET_SONDAGE_HOTEL.md** (ce fichier) et, si besoin, **PLAN_DEVELOPPEMENT_SONDAGE_HOTEL_MODULES.md**. Tu peux dire à l’assistant : *« J’ai rouvert le projet sondage hôtel. Voici l’archive du projet [coller ou @ARCHIVE_PROJET_SONDAGE_HOTEL.md]. Je veux reprendre à [X]. »*

4. **Vérifie où tu en es**  
   Regarde la section **3. Fichiers du développement** pour le statut des modules (bloqué / en cours). Les livrables (CSV, Excel, Word) sont listés à la fin du tableau.

### Où trouver quoi (référence rapide)

| Besoin | Fichier ou ressource |
|--------|----------------------|
| Contexte global, décisions, reprise | **ARCHIVE_PROJET_SONDAGE_HOTEL.md** (ce fichier) |
| Dernière session (24 fév. 2026) – discussion, pipeline, livrables | **HISTORIQUE_SESSION_2026-02-24.md** |
| Histoire de ce qui a été développé (modules 1–11) | **HISTOIRE_DEVELOPPEMENT_SONDAGE_HOTEL.md** |
| Chaînage m01→m09, qui génère le CSV | **CHAINAGE_MODULES_m01_a_m09.md** |
| Modifier des valeurs (un seul fichier : m01) | **MODE_FONCTIONNEMENT_MODIFICATIONS.md** |
| Évolution tarification dynamique (m00, m02b, étapes suivantes) | **PLAN_ETAPES_MODIFICATIONS_SEQUENTIELLES.md**, **PLAN_EVOLUTION_TARIFICATION_DYNAMIQUE.md** |
| Modifier la config tarification (interface graphique) | **INTERFACE_UTILISATEUR.md** ; lancer `streamlit run interface_streamlit_config.py` |
| Livrables à remettre au client | **SYNTHESE_LIVRABLES_CLIENT.md** |
| Spec détaillée, modules, verrouillage | **PLAN_DEVELOPPEMENT_SONDAGE_HOTEL_MODULES.md** |
| Commandes Git et push (sauvegarde) | **COMMENT_UTILISER_GIT.txt** |
| Vérifier qu’un livrable a bien été fait (preuve) | **VERIFICATION_LIVRABLES.md** |
| Code et historique complet | Dépôt GitHub (lien en bas de COMMENT_UTILISER_GIT.txt) |
| Objectifs initiaux, structure des données | **PROJET_DONNEES_HOTEL_MARKETING_SONDAGE.md** |

### Checklist « Je reprends le projet » (à cocher mentalement)

- [ ] Cursor ouvert sur le dossier **Bernard_sondage_hotel_ua2_20260224**
- [ ] `git pull origin main` fait (pour avoir la dernière version)
- [ ] **ARCHIVE_PROJET_SONDAGE_HOTEL.md** lu ou ouvert pour l’assistant
- [ ] Objectif de la session clair (ex. : finir m11, corriger le rapport, etc.)

Après une session de travail : **add → commit → push** (voir COMMENT_UTILISER_GIT.txt).

---

## 2. Contexte et objectifs du projet

- **Commande** : Préparer un jeu de données de réservations hôtelières (simulation) pour des **étudiants en marketing-sondage**, afin qu’ils pratiquent les **techniques statistiques d’analyse de sondage** et produisent des **informations pour la prise de décision**.
- **Public** : Professeur et étudiants ; le professeur doit pouvoir s’assurer que **tous les éléments d’apprentissage** prévus sont réalisables avec le fichier.
- **Livrables** :  
  - Fichier de données **sondage_hotel_data.csv** (environ 10 500+ lignes).  
  - Rapport de validation **Excel** (statistiques, tests, verdicts).  
  - **Synthèse Word** à l’intention du professeur (éléments d’apprentissage, checklist).  
  - Option : détail « information fine » (nourriture, spa) et format multi-onglets Excel (évoqué en début de projet ; non implémenté dans la première version, le cœur étant la génération CSV + validation + synthèse prof).

---

## 3. Décisions prises pendant la discussion

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

## 4. Fichiers du développement (emplacement et rôle)

**Répertoire principal** : `Bernard_sondage_hotel_ua2_20260224/` (ou chemin indiqué dans le plan).

| Fichier | Rôle | Statut |
|---------|------|--------|
| **PLAN_DEVELOPPEMENT_SONDAGE_HOTEL_MODULES.md** | Plan officiel du projet (spec, modules, verrouillage). Référence pour toute évolution. | Document maître |
| **PLAN_ETAPES_MODIFICATIONS_SEQUENTIELLES.md** | Plan étape par étape pour l’évolution « tarification dynamique » (m00, m02b, m02c, m02d, m03b, interface, pipeline). | Référence évolution |
| **m00_config_etendue.py** | Config étendue : charge m01 + config_tarification_dynamique.json ; expose `get_config_etendue()`. | Bloqué |
| **m01_config.py** | Configuration : 100 chambres, 72 %, segments, annulations, canaux, formules, anomalies. Sortie : `get_config()`, `config.json`. | Bloqué |
| **m02_segments.py** | Génération ID_Client, Segment, Type_Client, Saison, Canal_reservation, Type_canal, Annulee. | Bloqué |
| **m02b_types_chambre_calendrier.py** | Types de chambre et coefficients de tarification par mois (à partir de la config étendue). Expose `get_types_chambre()`, `get_coefficient_mois(mois)`. | Bloqué |
| **m02c_reservations_avec_dates.py** | Enrichit les réservations (m02) avec Mois_sejour, Sexe, Niveau_revenus, Pays, Province, Ville (config étendue). | Bloqué |
| **m02d_allocation_chambres.py** | Attribue Type_chambre et Numero_chambre à chaque réservation ; contrôle « toutes chambres réservées au moins 1 fois ». | Bloqué |
| **m03_nuits_chambre.py** | Nuits (Poisson si Interne non annulé), Rev_Chambre. | Bloqué |
| **m03b_revenus_chambre_dynamique.py** | Rev_Chambre (tarification dynamique : prix_base × coefficient mois) ; Tarif_applique ; 0 si Externe/Annulée. | Bloqué |
| **interface_config_tarification.py** | Interface CLI pour générer config_tarification_dynamique.json ; option --interactif. | Bloqué |
| **interface_streamlit_config.py** | Interface utilisateur (Streamlit) : formulaires pour modifier types chambre, 12 taux, sexe, revenus, pays, puis export JSON. Voir **INTERFACE_UTILISATEUR.md**. | Bloqué |
| **run_pipeline_evolution.py** | Pipeline évolution : m01 → m02c→m02d→m03b→m04…m09 → m10 → m11 ; CSV avec colonnes tarification dynamique. | Bloqué |
| **m04_revenus_centres_profit.py** | Rev_Banquet, Rev_Resto, Rev_Spa (par segment ; ANOVA sur Rev_Resto). | Bloqué |
| **m05_type_forfait.py** | Type_Forfait (Forfait Gastronomique / Chambre Seule) pour Khi-deux. | Bloqué |
| **m06_satisfaction_nps.py** | Satisfaction_NPS (formule + corrélation avec Rev_Spa) ; NaN si Annulee = Oui. | Bloqué |
| **m07_total_facture.py** | Total_Facture = Rev_Chambre + 1,1×Rev_Resto + 1,3×Rev_Spa + ε. | Bloqué |
| **m08_anomalies_pedagogiques.py** | Anomalies : 15 Externes Nuits>0, 3 NPS=99, 5 % manquants, 10 doublons. | Bloqué |
| **m09_export_csv.py** | Types de données, export **sondage_hotel_data.csv**. | Bloqué |
| **m10_rapport_validation.py** | Analyses statistiques complètes ; sortie **terminal** + **rapport_validation_sondage_hotel.xlsx**. | Bloqué |
| **m11_synthese_word_prof.py** | Synthèse **Word** pour le professeur : éléments d’apprentissage, variables, anomalies, checklist. Sortie : **synthese_elements_apprentissage_prof.docx**. | Bloqué |
| **config.json** | Config exportée (générée par m01_config.py). | Dépend de m01 |
| **sondage_hotel_data.csv** | Fichier de travail pour les étudiants (généré par m09). | Produit par pipeline |
| **rapport_validation_sondage_hotel.xlsx** | Rapport de validation (généré par m10). | Produit par pipeline |
| **synthese_elements_apprentissage_prof.docx** | Document Word pour le professeur (généré par m11). | Produit par m11 |

**Documents connexes** (racine Cursor ou dossier projet) :  
- **PROJET_DONNEES_HOTEL_MARKETING_SONDAGE.md** : objectifs initiaux, structure données, options A/B.  
- **ANALYSE_FICHIER_HOTEL_ET_FORMAT_SORTIE.md** : analyse du fichier Excel existant « Hotel de la Promenade », format multi-onglets / CSV, gestion du détail (nourriture, spa).

---

## 5. Enchaînement des modules et exécution

- **Ordre logique** : 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11.  
- **Exécution manuelle** : lancer chaque script depuis le répertoire du projet (ex. `python3 m01_config.py`, puis `m02_segments.py`, etc.) ; les modules 2–11 lisent la config (m01) ou la sortie du module précédent.  
- **Orchestrateur** : **run_pipeline.py** enchaîne m01 → m09 → m10 → m11 en une seule commande et vérifie la règle de blocage + présence des 4 fichiers de sortie. Commande : `python3 run_pipeline.py`. Détail : **HISTORIQUE_SESSION_2026-02-24.md** et **VERIFICATION_LIVRABLES.md** (section Pipeline).

---

## 6. Règles de blocage et évolution

- Un module **bloqué** ne doit **pas être modifié** sans demande explicite de déblocage.  
- Toute évolution qui toucherait à un module bloqué se fait soit par **déblocage**, soit dans un **nouveau fichier** (ex. m04b_ajustement.py) qui s’enchaîne après le module concerné.  
- Les **hypothèses** (paramètres) sont regroupées en **tête de chaque script** pour que l’opérateur puisse les modifier sans toucher à la logique.

---

## 7. Pistes d’amélioration ou de modification

- **Orchestrateur** : créer `run_pipeline.py` pour exécuter d’un coup m01 → m11 et produire CSV + Excel + Word.  
- **Détail « information fine »** : si besoin, ajouter des modules ou scripts qui génèrent des tables **détail_nourriture** et **détail_spa** (lignes de facture) à partir des montants Rev_Resto et Rev_Spa, avec sortie Excel multi-onglets ou CSV séparés.  
- **Volume** : le nombre de réservations (10 512) est fixé par la config (m01) ; modifier **DUREE_MOYENNE_SEJOUR** ou **NB_CHAMBRES** (si déblocage) pour changer le volume.  
- **Synthèse Word** : le contenu du document (éléments d’apprentissage, tableau, checklist) est dans **m11_synthese_word_prof.py** ; modifier ce script pour adapter le texte ou les sections (après déblocage si le module est bloqué).

---

## 8. Dépendances techniques

- **Python 3** avec **pandas**, **numpy**, **scipy** (pour ANOVA, Khi-deux, Pearson, régression).  
- **openpyxl** pour l’export Excel (m10).  
- **python-docx** pour l’export Word (m11) : `pip install python-docx`.

---

## 9. Garanties pour ne jamais repartir à zéro

- **En début de session** : ouvrir ce dossier dans Cursor → `git pull` → lire la section 1 (Contexte, reprise et checklist) et ouvrir ce fichier pour l'assistant.
- **En fin de session** : `git add .` → `git commit -m "…"` → `git push origin main` (voir COMMENT_UTILISER_GIT.txt).
- **Si tu changes de machine ou de répertoire** : cloner le dépôt GitHub (ou copier le dossier), ouvrir le projet dans Cursor, puis suivre la checklist reprise (section 1).
- **L'assistant Cursor n'a pas la mémoire** : lui donner **ARCHIVE_PROJET_SONDAGE_HOTEL.md** (et éventuellement PLAN_DEVELOPPEMENT_SONDAGE_HOTEL_MODULES.md) pour qu'il retrouve le contexte. Tu n'as pas à tout réexpliquer.

---

*Archive créée le 2025-02-17. Pour toute modification ou amélioration, s'appuyer sur ce document et sur **PLAN_DEVELOPPEMENT_SONDAGE_HOTEL_MODULES.md**.*

