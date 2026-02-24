# Chaînage des modules m01 → m09 : de la config au fichier sondage_hotel_data.csv

Ce document décrit **l’essentiel du traitement** effectué à chaque module pour aboutir au fichier **sondage_hotel_data.csv** (généré au module 9).

**Point important :** Dans la version actuelle, les données **ne partent pas d’un fichier Excel ou CSV fourni au départ**. Elles sont **générées de zéro** à partir de la configuration (module 1) et des modules 2 à 8. Le module 9 ne fait qu’écrire le tableau final en CSV. Si, en début de projet, un fichier de base avait été utilisé, il a été remplacé par cette chaîne de **simulation**.

---

## Vue d’ensemble du flux

**Pipeline classique** (run_pipeline.py) :
```
m01 (config)  →  m02  →  m03  →  m04  →  m05  →  m06  →  m07  →  m08  →  m09 (export CSV)
     │            │       │       │       │       │       │       │            │
  paramètres   base    nuits   revenus  forfait  NPS   facture  anomalies   sondage_hotel_data.csv
               table   chambre  resto/spa          total
```
**Pipeline évolution** (run_pipeline_evolution.py) : m02c → m02d → m03b puis m04…m09 (types chambre, mois, sexe, pays, tarif dynamique). Voir section *Pipeline évolution* en fin de document.

---

## Module 1 – Configuration (m01_config.py)

**Entrée :** Aucune (fichier de paramètres).  
**Sortie :** `config.json` (et un dictionnaire `get_config()` lu par tous les modules).

**Traitement :**
- Définition de toutes les **hypothèses** de la simulation : nombre de chambres (100), taux d’occupation (72 %), durée moyenne de séjour (2,5 nuits).
- Calcul du **nombre de réservations** pour l’année : N ≈ 10 512 (à partir des nuits annuelles et de la durée moyenne).
- Définition des **segments** (noms et répartition en %) : Affaires_Solo, Congressiste, Loisirs_Couple, Local_Gourmet, Local_Spa.
- **Canaux** de réservation (direct / intermédiaire), **taux d’annulation** (7 % direct, 29 % intermédiaire), **saison** (Basse/Haute) par segment.
- Paramètres pour les modules suivants : tarifs chambre, moyennes Rev_Resto/Rev_Spa par segment, probabilités Type_Forfait, formule NPS, coefficients Total_Facture, **anomalies pédagogiques** (nombre d’incohérences, NPS=99, % manquants, doublons).

**Rôle :** C’est la **référence unique** : aucun fichier de données en entrée ; tout part de cette config.

---

## Module 2 – Génération de la base (m02_segments.py)

**Entrée :** Config (m01).  
**Sortie :** Un **DataFrame** (en mémoire) : une ligne par réservation, sans fichier CSV en entrée.

**Traitement :**
- **ID_Client** : AB-00001 à AB-10512 (ou N selon la config).
- **Segment** : répartition selon les % de la config (25 % Affaires_Solo, 20 % Congressiste, etc.), puis mélange aléatoire.
- **Type_Client** : Interne ou Externe (Externe pour Local_Gourmet et Local_Spa).
- **Saison** : Haute ou Basse selon une probabilité par segment (ex. Congressiste 80 % Basse, Loisirs 80 % Haute).
- **Canal_reservation** : Site web, Courriel, Téléphone (direct) ou Booking, Expedia, etc. (intermédiaire), avec 50 % direct / 50 % intermédiaire.
- **Type_canal** : Direct ou Intermediaire.
- **Annulee** : Oui/Non selon le taux d’annulation par type de canal (graine aléatoire 42 pour reproductibilité).

**Rôle :** Création de la **table de base** : qui est le client, comment il a réservé, s’il a annulé. Aucune lecture de fichier Excel/CSV.

---

## Module 3 – Nuits et revenus chambre (m03_nuits_chambre.py)

**Entrée :** DataFrame sortie du module 2.  
**Sortie :** Même DataFrame + colonnes **Nuits**, **Rev_Chambre**.

**Traitement :**
- **Nuits** : 0 si Externe ou Annulée ; sinon tirage **Poisson(λ=2,5)** borné entre 1 et 14.
- **Rev_Chambre** : 0 si Externe ou Annulée ; sinon Nuits × tarif (200 $ en Basse, 350 $ en Haute).

**Rôle :** Ajout du **séjour** (nombre de nuits) et du **revenu chambre** par réservation.

---

## Module 4 – Revenus centres de profit (m04_revenus_centres_profit.py)

**Entrée :** DataFrame sortie du module 3.  
**Sortie :** Même DataFrame + **Rev_Banquet**, **Rev_Resto**, **Rev_Spa**.

**Traitement :**
- Si **Annulée = Oui** : Rev_Banquet, Rev_Resto, Rev_Spa = 0.
- **Rev_Banquet** : loi Gamma(k, θ) pour le segment Congressiste, 0 pour les autres.
- **Rev_Resto** : moyenne par segment + bruit normal (moyennes config : 60, 45, 80, 150, 20 par segment).
- **Rev_Spa** : moyenne par segment + bruit (Loisirs et Local_Spa plus élevés, autres 0 ou faible).

**Rôle :** Revenus **restaurant, spa, banquet** pour permettre les analyses par centre de profit et l’ANOVA (Rev_Resto par segment).

---

## Module 5 – Type de forfait (m05_type_forfait.py)

**Entrée :** DataFrame sortie du module 4.  
**Sortie :** Même DataFrame + **Type_Forfait**.

**Traitement :**
- **Type_Forfait** : « Forfait Gastronomique » ou « Chambre Seule » selon une **probabilité par segment** (ex. Loisirs 80 % Forfait, Congressiste 10 % Forfait).

**Rôle :** Variable catégorielle pour le **test du Khi-deux** (liaison Segment × Type_Forfait).

---

## Module 6 – Satisfaction NPS (m06_satisfaction_nps.py)

**Entrée :** DataFrame sortie du module 5.  
**Sortie :** Même DataFrame + **Satisfaction_NPS**.

**Traitement :**
- Si **Annulée = Oui** : NPS = NaN (pas de sondage).
- Sinon : formule de base (constante + effet Haute saison + effet Rev_Spa>100 + bruit) puis **composante corrélée à Rev_Spa** pour viser une corrélation Pearson d’environ 0,75. NPS borné entre 0 et 10.

**Rôle :** Satisfaction pour les analyses **Pearson** (Rev_Spa × NPS) et pour les exercices sur la satisfaction client.

---

## Module 7 – Total facture (m07_total_facture.py)

**Entrée :** DataFrame sortie du module 6.  
**Sortie :** Même DataFrame + **Total_Facture**.

**Traitement :**
- **Total_Facture** = Rev_Chambre + 1,1×Rev_Resto + 1,3×Rev_Spa + ε (ε petit bruit normal).

**Rôle :** Variable cible pour la **régression linéaire multiple** (les étudiants retrouvent des coefficients proches de 1 ; 1,1 ; 1,3).

---

## Module 8 – Anomalies pédagogiques (m08_anomalies_pedagogiques.py)

**Entrée :** DataFrame sortie du module 7.  
**Sortie :** Même DataFrame **modifié** + **10 lignes dupliquées** (donc plus de lignes au total).

**Traitement :**
1. **Incohérence logique** : 15 clients Externes se voient attribuer Nuits > 0 (alors qu’un Externe ne logeur pas à l’hôtel).
2. **Outliers** : 3 lignes avec Satisfaction_NPS = 99 (erreur de saisie simulée).
3. **Valeurs manquantes** : 5 % de cellules mises à NaN dans Rev_Spa et 5 % dans Rev_Resto (indépendamment).
4. **Doublons** : 10 lignes dupliquées ajoutées à la fin du tableau.

**Rôle :** Introduire des **anomalies volontaires** pour les exercices de **nettoyage de données** (détection et traitement).

---

## Module 9 – Export CSV (m09_export_csv.py)

**Entrée :** DataFrame sortie du module 8 (en mémoire).  
**Sortie :** Fichier **sondage_hotel_data.csv** sur disque.

**Traitement :**
- **Forcer les types** : colonnes catégorielles (Segment, Type_Client, Saison, etc.), Nuits en entier, revenus et NPS en flottant.
- **Export** : `to_csv` avec encodage UTF-8-sig, séparateur « ; », décimal « . ».

**Rôle :** Écrire le **fichier final** livré aux étudiants et utilisé par le module 10 (rapport de validation). C’est le **seul** module qui écrit `sondage_hotel_data.csv`.

---

## Résumé en tableau

| Module | Entrée | Sortie | Essentiel du traitement |
|--------|--------|--------|--------------------------|
| **m01** | — | config.json | Paramètres (volume, segments, canaux, taux, tarifs, anomalies). |
| **m02** | Config | DataFrame base | Génération des réservations : ID, Segment, Type_Client, Saison, Canal, Annulee. |
| **m03** | df m02 | df + Nuits, Rev_Chambre | Nuits (Poisson) et revenu chambre (Nuits × tarif). |
| **m04** | df m03 | df + Rev_Banquet, Rev_Resto, Rev_Spa | Revenus par centre de profit (Banquet Congressiste, Resto/Spa par segment). |
| **m05** | df m04 | df + Type_Forfait | Forfait Gastronomique / Chambre Seule selon le segment. |
| **m06** | df m05 | df + Satisfaction_NPS | NPS avec corrélation à Rev_Spa (cible r ≈ 0,75). |
| **m07** | df m06 | df + Total_Facture | Total = Rev_Chambre + 1,1×Rev_Resto + 1,3×Rev_Spa + bruit. |
| **m08** | df m07 | df modifié + 10 doublons | Incohérences (Externes Nuits>0), NPS=99, manquants 5 %, doublons. |
| **m09** | df m08 | **sondage_hotel_data.csv** | Typage des colonnes et export CSV. |

---

## Fichier de base initial

Dans le code actuel, **aucun fichier Excel ou CSV n’est lu** pour construire les données. La « base » est :

1. **m01** : la configuration (constantes + `config.json`).
2. **m02** : la **génération aléatoire** du tableau de réservations à partir de cette config.

Si, au tout début du projet, un fichier Excel/CSV avait été fourni, il a été remplacé par cette chaîne de simulation (m01 → m09). Pour obtenir un nouveau `sondage_hotel_data.csv`, il suffit de lancer le pipeline (ou m09 après m01) : le fichier est alors **régénéré** entièrement à partir de la config et des modules 2 à 8.

---

## Pipeline évolution (tarification dynamique)

Une **deuxième chaîne** permet d’obtenir un CSV enrichi avec **types de chambre**, **mois de séjour**, **sexe**, **revenus**, **pays/province/ville** et **tarification dynamique** (prix selon le type de chambre et le mois). Script : **run_pipeline_evolution.py**.

**Flux :**
```
m01  →  m00 (config étendue)  →  m02b (calendrier)  →  m02c  →  m02d  →  m03b  →  m04 … m08  →  m09
       config_tarification_dynamique.json    types + coeffs   enrichi   allocation  Rev_Chambre dynamique
```

**Modules supplémentaires :**
- **m00** : charge m01 + `config_tarification_dynamique.json` (types chambre, 12 taux, sexe, revenus, pays).
- **m02b** : types de chambre et coefficient de prix par mois (forte occupation → coefficient > 1).
- **m02c** : appelle m02 puis ajoute **Mois_sejour**, **Sexe**, **Niveau_revenus**, **Pays**, **Province**, **Ville**.
- **m02d** : ajoute **Type_chambre** et **Numero_chambre** (chaque chambre au moins 1 réservation).
- **m03b** : **Rev_Chambre** = Nuits × prix_base(type) × coefficient(mois), 0 si Externe/Annulée ; **Tarif_applique**.

**Colonnes supplémentaires dans le CSV :** Mois_sejour, Sexe, Niveau_revenus, Pays, Province, Ville, Type_chambre, Numero_chambre, Tarif_applique (Rev_Chambre est recalculé par m03b).

**Interface :** Pour modifier les valeurs (types de chambre, taux, sexe, pays, etc.) : **interface_streamlit_config.py** (`streamlit run interface_streamlit_config.py` ou `./lancer_interface_chrome.sh`). Enregistrement vers `config_tarification_dynamique.json`, puis `python3 run_pipeline_evolution.py` pour régénérer le CSV.
