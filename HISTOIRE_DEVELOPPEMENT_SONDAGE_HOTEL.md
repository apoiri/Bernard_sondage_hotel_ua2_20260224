# Histoire du développement – Projet « L'Hôtel Boutique Art de Vivre » (Sondage – Marketing)

**Objectif de ce document** : Reconstituer l’historique de ce qui a été développé, module par module, pour ne pas repartir à zéro et pour donner le contexte à un assistant (ex. Cursor) qui n’a pas la mémoire des discussions.

---

## Contexte initial du projet

- **Commande** : Créer un jeu de données de réservations hôtelières **simulées** pour des **étudiants en marketing-sondage**, afin qu’ils pratiquent les techniques d’analyse de sondage (proportions, IC, Khi-deux, Pearson, ANOVA, régression) et produisent des informations pour la prise de décision.
- **Public** : Professeur et étudiants. Le professeur doit pouvoir s’assurer que tous les éléments d’apprentissage prévus sont réalisables avec le fichier.
- **Livrables visés** :
  1. Fichier CSV **sondage_hotel_data.csv** (~10 500+ lignes).
  2. Rapport de validation **Excel** (statistiques, tests, verdicts).
  3. Synthèse **Word** pour le professeur (éléments d’apprentissage, checklist).

Les décisions de conception (100 chambres, 72 % occupation, 18 % annulations, 50 % direct / 50 % intermédiaires, canaux, segments, etc.) sont consignées dans **ARCHIVE_PROJET_SONDAGE_HOTEL.md**.

---

## Ordre logique du développement (ce qui a été fait)

Le projet a été structuré en **11 modules Python** enchaînés. Chaque module correspond à un fichier `mXX_*.py`, avec des hypothèses modifiables en tête de script et une fonction `run()` qui prend le DataFrame du module précédent (sauf m01) et retourne le DataFrame enrichi.

---

### Module 1 – Configuration (**m01_config.py**)

- **Rôle** : Centraliser toutes les constantes et paramètres du projet (100 chambres, 72 % occupation, segments, canaux, taux d’annulation, formules NPS, anomalies pédagogiques, noms des fichiers de sortie, etc.).
- **Sorties** : `get_config()` (dictionnaire) et fichier **config.json** (sauvegardé à l’exécution).
- **Calcul** : Nombre de réservations pour une année = `ceil(100 × 365 × 0,72 / 2,5)` = **10 512**.
- **Développement** : Premier module écrit ; tous les autres s’appuient sur lui (import de `get_config()` ou lecture de `config.json`).

---

### Module 2 – Segments, canal, annulation (**m02_segments.py**)

- **Rôle** : Générer le squelette du jeu de données : une ligne par réservation, avec **ID_Client** (AB-00001 … AB-10512), **Segment** (Affaires_Solo, Congressiste, Loisirs_Couple, Local_Gourmet, Local_Spa) selon les pourcentages, **Type_Client** (Interne / Externe : Local_Gourmet et Local_Spa = Externe), **Saison** (Haute/Basse selon probabilité par segment), **Canal_reservation** et **Type_canal** (Direct / Intermediaire), **Annulee** (Oui/Non avec 7 % direct, 29 % intermédiaire).
- **Entrée** : Config (m01).
- **Sortie** : DataFrame avec ces colonnes ; pas de fichier intermédiaire par défaut (option `etape2_segments.csv`).
- **Développement** : Deuxième module ; définit la structure de base sur laquelle tous les modules suivants s’appuient.

---

### Module 3 – Nuits et Rev_Chambre (**m03_nuits_chambre.py**)

- **Rôle** : Ajouter **Nuits** et **Rev_Chambre**. Règles : Nuits = 0 si Externe ou Annulée ; sinon tirage **Poisson(λ=2,5)** borné [1, 14]. Rev_Chambre = 0 si Externe ou Annulée ; sinon Nuits × tarif (saison Basse 200 $/nuit, Haute 350 $/nuit).
- **Entrée** : DataFrame sortie m02.
- **Développement** : Troisième module ; introduit les premières variables numériques « métier » et la logique Interne/Externe/Annulé.

---

### Module 4 – Revenus centres profit (**m04_revenus_centres_profit.py**)

- **Rôle** : Ajouter **Rev_Banquet**, **Rev_Resto**, **Rev_Spa**. Si Annulée = Oui : les trois = 0. Sinon : Rev_Banquet = Gamma(k, θ) pour le segment Congressiste, 0 pour les autres ; Rev_Resto et Rev_Spa = moyenne par segment + bruit normal (avec écarts-types fixés pour que l’ANOVA sur Rev_Resto soit significative, p < 0,05).
- **Entrée** : DataFrame sortie m03.
- **Développement** : Quatrième module ; permet les analyses ANOVA (Rev_Resto par segment) et la corrélation Rev_Spa–NPS plus tard.

---

### Module 5 – Type_Forfait (**m05_type_forfait.py**)

- **Rôle** : Ajouter **Type_Forfait** : « Forfait Gastronomique » ou « Chambre Seule » selon une probabilité par segment (ex. Loisirs 80 % Forfait, Congressiste 10 %), pour permettre un **test du Khi-deux** (Segment × Type_Forfait).
- **Entrée** : DataFrame sortie m04.
- **Développement** : Cinquième module ; variable catégorielle pensée pour l’exercice Khi-deux en cours.

---

### Module 6 – Satisfaction NPS (**m06_satisfaction_nps.py**)

- **Rôle** : Ajouter **Satisfaction_NPS**. Si Annulée = Oui : NPS = NaN. Sinon : formule de base (constante + effet Haute saison + effet Rev_Spa>100 + bruit) + une **composante corrélée à Rev_Spa** pour atteindre une corrélation Pearson cible d’environ **0,75** entre Rev_Spa et NPS.
- **Entrée** : DataFrame sortie m05.
- **Développement** : Sixième module ; conçu pour que les étudiants retrouvent une corrélation forte Rev_Spa–NPS (avant introduction des anomalies).

---

### Module 7 – Total_Facture (**m07_total_facture.py**)

- **Rôle** : Ajouter **Total_Facture** = Rev_Chambre + 1,1×Rev_Resto + 1,3×Rev_Spa + ε (bruit petit). Modèle de **régression linéaire multiple** que les étudiants peuvent retrouver (coefficients proches de 1 ; 1,1 ; 1,3).
- **Entrée** : DataFrame sortie m06.
- **Développement** : Septième module ; boucle la partie « génération de données propres » avant les anomalies.

---

### Module 8 – Anomalies pédagogiques (**m08_anomalies_pedagogiques.py**)

- **Rôle** : Introduire volontairement des **anomalies** pour l’exercice de **data cleaning** : (1) 15 Externes avec Nuits > 0 (incohérence logique), (2) 3 lignes avec Satisfaction_NPS = 99 (outlier de saisie), (3) 5 % de valeurs manquantes dans Rev_Spa et Rev_Resto, (4) 10 lignes dupliquées (le fichier final a donc N_RESERVATIONS + 10 lignes).
- **Entrée** : DataFrame sortie m07.
- **Sortie** : Même DataFrame modifié + lignes dupliquées.
- **Développement** : Huitième module ; les étudiants doivent détecter et traiter ces anomalies avant ou pendant les analyses.

---

### Module 9 – Export CSV (**m09_export_csv.py**)

- **Rôle** : Forcer les types des colonnes (catégorielles, entiers, flottants), puis exporter le DataFrame vers **sondage_hotel_data.csv** (encodage UTF-8-sig, séparateur `;`).
- **Entrée** : DataFrame sortie m08.
- **Sortie** : Fichier **sondage_hotel_data.csv** (livrable principal pour les étudiants).
- **Développement** : Neuvième module ; produit le CSV final utilisé par m10 et par le professeur/étudiants.

---

### Module 10 – Rapport de validation (**m10_rapport_validation.py**)

- **Rôle** : Lire **sondage_hotel_data.csv**, exécuter toutes les analyses prévues pour les étudiants (descriptif, proportions + IC 95 %, Khi-deux Segment×Type_Forfait, Pearson Rev_Spa–NPS, ANOVA Rev_Resto par segment, régression Total_Facture ~ Rev_Chambre + Rev_Resto + Rev_Spa, annulations par canal, contrôle qualité des anomalies), afficher un **sommaire dans le terminal** et écrire un fichier **rapport_validation_sondage_hotel.xlsx** (plusieurs onglets : Descriptif, Effectifs, Proportions_IC, Khi2, Pearson, ANOVA, Régression, Annulations, Qualité).
- **Entrée** : Fichier CSV (produit par m09).
- **Sortie** : Rapport terminal + **rapport_validation_sondage_hotel.xlsx** (livrable de validation).
- **Développement** : Dixième module ; vérifie que le jeu de données permet bien toutes les analyses pédagogiques prévues.

---

### Module 11 – Synthèse Word professeur (**m11_synthese_word_prof.py**)

- **Rôle** : Générer un document **Word** (**synthese_elements_apprentissage_prof.docx**) à l’intention du professeur : présentation du jeu de données, liste des variables, **tableau des éléments d’apprentissage** (technique, variables, objectif, case à cocher), description des **anomalies pédagogiques**, et **checklist** pour s’assurer que tous les objectifs sont couverts en cours/TD.
- **Entrée** : Aucune (script autonome ; peut s’appuyer sur la présence du CSV pour rappeler le nom du fichier).
- **Sortie** : **synthese_elements_apprentissage_prof.docx** (livrable professeur).
- **Développement** : Onzième module ; statut « En cours » dans l’archive (contenu déjà riche, possiblement à affiner selon retours).

---

## Fichiers de support et documentation

- **config.json** : Généré par m01 ; contient toute la config en JSON (utilisable par d’autres outils si besoin).
- **ARCHIVE_PROJET_SONDAGE_HOTEL.md** : Contexte, décisions, reprise, checklist, liste des fichiers, règles de blocage, pistes d’amélioration, garanties pour ne pas repartir à zéro.
- **COMMENT_UTILISER_GIT.txt** : Guide Git en 4 étapes (add, commit, push) + section « Quand tu reviens sur le projet ».
- **PREMIERE_EXPORTATION_GITHUB.txt** : Instructions pour la première connexion du projet à GitHub.
- **.gitignore** : Exclut .DS_Store, __pycache__, environnements virtuels.

---

## Ce qui n’a pas été développé (pistes connues)

- **run_pipeline.py** (Module 0) : Script orchestrateur pour enchaîner m01 → m11 en une seule commande ; prévu mais non implémenté.
- **PLAN_DEVELOPPEMENT_SONDAGE_HOTEL_MODULES.md** : Référencé dans l’archive comme « plan officiel » ; absent du dépôt (possiblement dans un autre dossier ou à recréer).
- **Détail « information fine »** (nourriture, spa en lignes de facture) et format Excel multi-onglets : évoqué en début de projet, non implémenté dans cette version.

---

## Enchaînement technique (résumé)

1. **m01_config.py** → config + `get_config()`  
2. **m02_segments.run()** → DataFrame (ID_Client, Segment, Type_Client, Saison, Canal, Type_canal, Annulee)  
3. **m03_nuits_chambre.run(df)** → + Nuits, Rev_Chambre  
4. **m04_revenus_centres_profit.run(df)** → + Rev_Banquet, Rev_Resto, Rev_Spa  
5. **m05_type_forfait.run(df)** → + Type_Forfait  
6. **m06_satisfaction_nps.run(df)** → + Satisfaction_NPS  
7. **m07_total_facture.run(df)** → + Total_Facture  
8. **m08_anomalies_pedagogiques.run(df)** → anomalies + doublons  
9. **m09_export_csv.run(df)** → sondage_hotel_data.csv  
10. **m10_rapport_validation.run()** → lit le CSV → rapport terminal + rapport_validation_sondage_hotel.xlsx  
11. **m11_synthese_word_prof.run()** → synthese_elements_apprentissage_prof.docx  

Chaque module peut être exécuté seul (section `if __name__ == "__main__"` qui enchaîne les modules précédents puis affiche un aperçu) ou appelé par un futur orchestrateur.

---

*Document créé pour reconstituer l’historique du développement à partir des fichiers du projet. À mettre à jour si de nouveaux modules ou livrables sont ajoutés.*
