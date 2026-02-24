# Mode de fonctionnement – Modifier des valeurs sans repartir à zéro

Ce document décrit **comment voir le processus de création du fichier** et **où modifier des valeurs (ou en ajouter)** en ne touchant qu’**un seul endroit** autant que possible.

---

## Principe : un seul fichier pour toutes les valeurs

**Pour modifier des valeurs existantes (tarifs, taux, segments, canaux, etc.)**, vous n’avez à éditer **qu’un seul fichier** : **m01_config.py**.

Tous les modules m02 à m09 (et m10) lisent la configuration via `get_config()` qui s’appuie sur les constantes définies dans m01. Donc :

- Vous changez une valeur dans **m01_config.py**.
- Vous relancez le pipeline : `python3 run_pipeline.py`.
- Les fichiers (CSV, rapport Excel, Word) sont régénérés avec les nouvelles valeurs.

**Vous ne modifiez aucun autre module** (m02 à m11). Un seul fichier = un seul point de modification pour les paramètres.

---

## Voir le processus de création

1. **Chaînage des modules** : le fichier **CHAINAGE_MODULES_m01_a_m09.md** décrit, module par module, ce qui est fait (m01 → m02 → … → m09) pour aboutir à `sondage_hotel_data.csv`.
2. **Exécution** : en lançant `python3 run_pipeline.py`, vous voyez dans le terminal les étapes (m01, m09, m10, m11) et les messages des modules (hypothèses, export, etc.).
3. **Config exportée** : après exécution, **config.json** contient un résumé de toute la config utilisée (lecture possible pour vérifier les valeurs effectives).

---

## Où modifier quoi (tout est dans m01_config.py)

Tableau de repérage : **variable dans m01** → **effet sur les données / le rapport**.

| Vous voulez… | Variable(s) dans m01_config.py (section « HYPOTHÈSES ») |
|--------------|--------------------------------------------------------|
| Changer le nombre de réservations (volume) | `TAUX_OCCUPATION`, `DUREE_MOYENNE_SEJOUR` (N est calculé à partir de ça) |
| Changer les segments ou leur répartition | `SEGMENTS_NOMS`, `SEGMENTS_POURCENTAGES` |
| Changer les canaux (direct / intermédiaire) | `CANAUX_DIRECT`, `CANAUX_DIRECT_POIDS`, `CANAUX_INTERMEDIAIRES`, `CANAUX_INTERMEDIAIRES_POIDS`, `PART_RESERVATIONS_DIRECT` |
| Changer les taux d’annulation | `TAUX_ANNULATION_DIRECT`, `TAUX_ANNULATION_INTERMEDIAIRE` |
| Changer la saison (Basse/Haute) par segment | `PROBA_SAISON_BASSE_PAR_SEGMENT` |
| Changer les nuits (durée de séjour) | `LAMBDA_POISSON_NUITS`, `MIN_NUITS`, `MAX_NUITS` |
| Changer les tarifs chambre | `TARIF_CHAMBRE_BASSE`, `TARIF_CHAMBRE_HAUTE` |
| Changer les revenus restaurant / spa par segment | `MOYENNES_REV_RESTO_PAR_SEGMENT`, `MOYENNES_REV_SPA_PAR_SEGMENT` |
| Changer le forfait (Khi-deux) par segment | `PROBA_FORFAIT_GASTRONOMIQUE_PAR_SEGMENT` |
| Changer la satisfaction NPS (niveau, corrélation Spa) | `NPS_CONSTANTE`, `NPS_EFFET_HAUTE_SAISON`, `NPS_EFFET_REV_SPA_SUP_100`, `NPS_CORRELATION_REV_SPA` |
| Changer la formule Total_Facture | `COEFF_REV_RESTO`, `COEFF_REV_SPA`, `ECART_TYPE_BRUIT_TOTAL` |
| Changer les anomalies pédagogiques | `N_INCOHERENCES_EXTERNES_NUITS`, `N_OUTLIERS_NPS`, `PCT_MANQUANTS`, `N_DOUBLONS` |
| Changer le nom du fichier CSV de sortie | `FICHIER_CSV_SORTIE` |

Tant que vous ne faites qu’**ajuster ces valeurs** (nombres, listes, probabilités), **m01_config.py est le seul fichier à modifier**. Aucun autre module n’a besoin d’être touché.

---

## Workflow recommandé

1. Ouvrir **m01_config.py** et modifier les constantes dans la section « HYPOTHÈSES DU SCRIPT ».
2. Sauvegarder.
3. Lancer : `python3 run_pipeline.py`.
4. Vérifier **sondage_hotel_data.csv** et **rapport_validation_sondage_hotel.xlsx**.

Répéter ces étapes pour toute nouvelle série de valeurs. Vous ne repartez pas à zéro : vous ne changez que des paramètres dans un seul fichier.

---

## Pourquoi certaines modifications demandent plusieurs modules

Votre condition est : éviter de modifier plusieurs modules. C’est respecté pour **toutes les modifications de valeurs listées ci-dessus** (un seul fichier : m01).

En revanche, si vous voulez **ajouter une nouvelle grandeur** (une **nouvelle colonne** dans les données, ou une **nouvelle analyse** dans le rapport), alors **par construction du pipeline** plusieurs modules sont concernés. Voici pourquoi.

- **Une nouvelle colonne** doit être **créée** quelque part : un module (m02 à m08) doit calculer cette colonne et l’ajouter au DataFrame. Il n’existe pas de “module générique” qui invente des colonnes à la demande sans code.
- Si cette grandeur dépend de **paramètres**, ils doivent être définis (souvent dans m01) et éventuellement exposés dans `get_config()`.
- Si vous voulez que cette grandeur apparaisse dans le **rapport de validation** (Excel), le module qui produit ce rapport (m10) doit être adapté pour la calculer et l’afficher.

Donc :

- **Changer des valeurs ou des listes existantes** → **un seul fichier** : m01_config.py.
- **Ajouter une nouvelle variable / une nouvelle analyse** → **plusieurs modules** : au moins un module qui génère la donnée, éventuellement m01 pour les paramètres, et éventuellement m10 pour le rapport. Ce n’est pas une limite de conception évitable : c’est la structure même du flux (génération → export → rapport).

En résumé : **modifications de valeurs = uniquement m01**. **Nouvelles colonnes ou nouvelles analyses = plusieurs modules par nécessité de structure.**

---

## Récapitulatif

| Type de modification | Fichier(s) à modifier | Remarque |
|----------------------|------------------------|----------|
| Valeurs existantes (tarifs, taux, segments, canaux, NPS, anomalies, etc.) | **m01_config.py** uniquement | Un seul fichier ; puis relancer le pipeline. |
| Voir le processus de création | **CHAINAGE_MODULES_m01_a_m09.md** + exécution du pipeline | Aucune modification de code. |
| Ajouter une nouvelle colonne ou une nouvelle analyse | m01 (paramètres) + un module de génération (m02–m08) + éventuellement m10 | Plusieurs modules nécessaires par la structure du pipeline. |

Si vous restez sur des **changements de valeurs ou de listes déjà présentes dans m01**, vous ne modifiez **qu’un seul module** (m01) et vous évitez de repartir à zéro sur l’ensemble du projet.
