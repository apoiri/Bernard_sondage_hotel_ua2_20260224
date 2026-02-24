# Rapport détaillé – Validation des analyses et appui à la prise de décision

**Projet :** L'Hôtel Boutique Art de Vivre – Données de sondage pour la formation  
**Public :** Professeurs, client, experts  
**Objectif :** Démontrer que les données fournies sont **valides**, que les techniques statistiques appliquées sont **cohérentes**, et que chaque analyse fournit des **indications utiles pour la prise de décision en entreprise** et pour la **formation des étudiants**.

---

## 1. Contexte et validité des données

- Le fichier **sondage_hotel_data.csv** contient environ **10 500 réservations** simulées sur une année (variables : segment, canal, annulation, nuits, revenus chambre/resto/spa, forfait, satisfaction NPS, etc.).
- **Taux d'occupation cible :** le taux de génération est **industrie ± 1 %** (moyenne des 12 taux mensuels de la config étendue + écart). La valeur (ex. 72 %, 74 %) figure dans **config.json** (`TAUX_OCCUPATION_POURCENT`). C'est un **paramètre de la simulation** pour fixer le volume de réservations. Le taux **calculable à partir du CSV** (somme des Nuits vendues, ex. Interne + non annulée, divisée par la capacité 100×365) peut différer (effet des annulations, des Externes, du périmètre). Les étudiants ne sont pas censés « prouver » ce taux à partir du fichier ; c’est un élément de contexte pédagogique.
- Les analyses ci‑dessous ont été réalisées avec les **mêmes données** que celles livrées aux étudiants. Les résultats constatés sont **reproductibles** à partir du CSV (script `verif_calculs_stats.py` et module m10).
- **Validation des chiffres :** les valeurs de ce rapport (proportions, Khi², Pearson, ANOVA, régression, taux d'annulation, anomalies) ont été **recalculées sur le fichier sondage_hotel_data.csv** et correspondent aux sorties de `verif_calculs_stats.py` et du module m10. Chaque résultat est aligné sur l'analyse du fichier sondage livré (pas une simple reprise de modèle).
- Ce rapport détaille, pour **chaque technique** : les **résultats constatés**, une **interprétation**, les **leçons à retenir** et l’**information à tenir pour la prise de décision**. Il permet aux professeurs et au client de **valider la qualité et l’usage pédagogique** des données.

---

## 2. Proportions et intervalles de confiance (IC 95 %)

### Ce que la technique permet de déceler
Estimer la **part d’une catégorie** dans la population (ex. % d’annulations, % de clients avec dépenses spa, % forfait gastronomique) et la **précision** de cette estimation (IC 95 %).

### Formule utilisée
\( p \pm 1{,}96 \sqrt{p(1-p)/n} \) (approximation normale pour une proportion).

### Résultats constatés
- **% Annulées :** 18,7 % — IC 95 % : [18,0 % ; 19,5 %]
- **% Rev_Spa > 0 :** 52,3 % — IC 95 % : [51,4 % ; 53,3 %]
- **% Forfait Gastronomique :** 42,1 % — IC 95 % : [41,1 % ; 43,0 %]

### Interprétation
Les proportions observées sont cohérentes avec les hypothèses de la simulation (taux d’annulation global ~18 %, part direct/intermédiaire, répartition forfaits). Les IC sont resserrés grâce à la taille d’échantillon (n ≈ 10 500), ce qui donne une estimation stable.

### Leçons à retenir
- Un **grand échantillon** réduit la marge d’incertitude (IC étroit).
- Suivre les **proportions clés** (annulations, pénétration spa, forfaits) permet de piloter l’activité et de détecter les dérives.

### Information pour la prise de décision (gestionnaire)
**Fixer des objectifs réalistes** (taux d’annulation, pénétration spa, part des forfaits) et **suivre les écarts** par rapport aux objectifs. Les IC donnent une fourchette crédible pour le pilotage opérationnel et la rentabilité (ex. objectif « annulations < 20 % »).

---

## 3. Test du Khi-deux (indépendance)

### Ce que la technique permet de déceler
Déceler une **liaison** entre deux variables catégorielles : ici **Segment** et **Type de forfait**. Les segments ont-ils des comportements différents selon le forfait choisi ?

### Formule utilisée
\( \chi^2 = \sum (O - E)^2 / E \), avec O = effectifs observés, E = effectifs attendus sous l’hypothèse d’indépendance. ddl = (lignes − 1)(colonnes − 1).

### Résultats constatés
- **Khi² = 2841,56** — ddl = 4 — **p-value ≈ 0,000**

### Interprétation
La liaison est **très significative** : le type de forfait (Gastronomique vs Chambre seule) est fortement associé au segment client (ex. Loisirs_Couple → plus de Forfait Gastronomique ; Congressiste → plus Chambre seule). Les données sont donc **adaptées** pour un exercice sur l’indépendance et le ciblage.

### Leçons à retenir
- Un **Khi-deux significatif** indique que les deux variables ne sont pas indépendantes : le profil client (segment) **influence** le choix du forfait.
- On peut ensuite analyser les **effectifs par case** pour voir quels segments adhèrent le plus à quel forfait.

### Information pour la prise de décision (gestionnaire)
**Cibler l’offre (forfaits) par segment** pour maximiser l’adhésion et les revenus. **Personnaliser** la communication et les tarifs selon le profil client (ex. mettre en avant le forfait gastronomique pour les Loisirs, offres chambre seule pour les Affaires/Congressiste).

---

## 4. Corrélation de Pearson (Rev_Spa × Satisfaction_NPS)

### Ce que la technique permet de déceler
Mesurer la **relation linéaire** entre deux variables numériques : ici **revenus Spa** et **satisfaction NPS**. Les clients qui dépensent plus au spa sont-ils plus satisfaits ?

### Formule utilisée
\( r = \text{Cov}(X,Y) / (s_X \cdot s_Y) \). Calcul sur les réservations non annulées et sans valeur manquante (n ≈ 8 121).

### Résultats constatés
- **r ≈ 0,45** (données brutes) — **p-value ≈ 0,000** — n = 8 121. **Après nettoyage** (suppression doublons, NPS=99 → manquant, correction cohérente des annulées) : **r ≈ 0,76**, conforme à l'intention pédagogique.

### Interprétation
**Corrélation positive significative** : plus les revenus Spa sont élevés, plus la satisfaction NPS tend à être élevée. En **données brutes**, r ≈ 0,45 ; **après nettoyage**, r remonte à environ 0,76. La formulation pédagogique doit indiquer « r ≈ 0,75 **après nettoyage** », et non « avant anomalies ».

### Leçons à retenir
- Une corrélation **positive et significative** suggère un **lien** entre dépense spa et satisfaction, sans prouver la causalité.
- r modéré (0,45) : d’autres facteurs influencent aussi la satisfaction ; utile pour discuter avec les étudiants (corrélation ≠ causalité).

### Information pour la prise de décision (gestionnaire)
**Identifier les leviers de satisfaction** (ex. Spa) pour la **fidélisation** et la **rentabilité**. **Investir** dans les services qui améliorent à la fois la satisfaction et le panier moyen (ex. offres spa ciblées, packages).

---

## 5. ANOVA à un facteur (Rev_Resto par Segment)

### Ce que la technique permet de déceler
Déceler des **différences de moyennes** d’une variable quantitative (**Rev_Resto**) entre plusieurs groupes (**segments**). Les segments dépensent-ils différemment au restaurant ?

### Formule utilisée
F = (variance inter-groupes / ddl₁) / (variance intra-groupes / ddl₂). Test F de Fisher (ANOVA).

### Résultats constatés
- **F = 10 362,84** — **p-value ≈ 0,000**

### Interprétation
Les **dépenses restaurant** diffèrent **très significativement** selon le segment. Les étudiants peuvent interpréter **quels segments** dépensent le plus au restaurant (ex. Local_Gourmet, Loisirs) et lesquels moins (ex. Affaires_Solo, Congressiste).

### Leçons à retenir
- Une **ANOVA significative** indique qu’au moins deux segments ont des moyennes différentes ; des **comparaisons multiples** (ou les moyennes par segment) permettent d’affiner.
- Segment × revenus = base pour le **ciblage** des offres (menus, promotions).

### Information pour la prise de décision (gestionnaire)
**Allouer les ressources** (restaurant, menus, promotions) selon les **segments qui dépensent le plus**. **Optimiser la rentabilité** par centre de profit et par cible (ex. menus « gourmet » pour Local_Gourmet et Loisirs).

---

## 6. Régression linéaire multiple (Total_Facture ~ toutes sources de revenus)

### Ce que la technique permet de déceler
Expliquer la **facture totale** à partir de **toutes les sources de revenus** (Chambre, Banquet si présent, Resto, Spa) et **vérifier la cohérence** du modèle (coefficients théoriques 1 pour Chambre/Banquet ; 1,1 Resto ; 1,3 Spa).

### Formule utilisée
Modèle : Total_Facture = β₀ + β₁·Rev_Chambre + β₂·Rev_Banquet + β₃·Rev_Resto + β₄·Rev_Spa + ε (Rev_Banquet inclus lorsque disponible). MCO. R² = 1 − (SCR / SCT).

### Résultats constatés
- **Constante ≈ 2,59** — **Rev_Chambre ≈ 1,00** — **Rev_Banquet ≈ 1,00** — **Rev_Resto ≈ 1,08** — **Rev_Spa ≈ 1,29** — **R² ≈ 0,9998** — n ≈ 9 500 (pipeline évolution avec Rev_Banquet).

### Interprétation
Les **coefficients** sont très proches du **modèle théorique** (1 ; 1,1 ; 1,3). La facture totale est **quasi parfaitement** expliquée par la somme pondérée des revenus, ce qui **valide la structure des données** pour l’exercice de régression et la cohérence du modèle économique simulé.

### Leçons à retenir
- Un **R² proche de 1** indique que le modèle linéaire décrit très bien la facture ; en situation réelle, R² serait en général plus faible (bruit, autres postes).
- Les **coefficients** renseignent sur le **poids** de chaque poste dans le total (chambre, resto, spa).

### Information pour la prise de décision (gestionnaire)
**Piloter la structure des revenus** (chambre, resto, spa) et **détecter les dérives** de tarification ou de coûts. **Assurer la cohérence** du modèle économique et de la **rentabilité globale** (ex. si les coefficients s’écartent fortement, enquêter sur les prix ou les coûts).

---

## 7. Taux d’annulation par canal (Direct vs Intermédiaire)

### Ce que la technique permet de déceler
Comparer le **risque d’annulation** entre **réservations directes** (site, courriel, téléphone) et **intermédiaires** (OTA : Booking, Expedia, etc.).

### Formule utilisée
Taux = (nombre d’annulées dans le groupe) / (nombre total dans le groupe).

### Résultats constatés
- **Taux Direct : 6,8 %** (attendu simulation ~7 %)
- **Taux Intermédiaire : 30,5 %** (attendu simulation ~29 %)

### Interprétation
Les taux observés sont **proches des paramètres** de la simulation. Les **intermédiaires** affichent un **taux d’annulation nettement plus élevé** que le direct, ce qui est **réaliste** et fournit une base claire pour un débat décisionnel (canal, politique tarifaire, commissions).

### Leçons à retenir
- **Comparer des taux** entre groupes (direct vs OTA) permet de **quantifier le risque** par canal.
- Un taux d’annulation plus élevé sur les OTA a un impact sur l’occupation réelle, les surréservations et la rentabilité.

### Information pour la prise de décision (gestionnaire)
**Choisir les canaux** (développement du direct vs OTA), **négocier les commissions** et **gérer le risque de no-show**. **Réduire les annulations** (ex. politique de prépaiement, communication) améliore la **prévisibilité** et la **rentabilité** (taux d’occupation réel, surréservations).

---

## 8. Contrôle qualité (anomalies pédagogiques)

### Ce que la technique permet de déceler
Vérifier la **présence des anomalies** volontairement injectées pour les **exercices de nettoyage** : incohérences (Externes avec Nuits > 0), valeurs aberrantes (NPS = 99), valeurs manquantes (Rev_Spa, Rev_Resto), doublons.

### Formule utilisée
Comptages : Externes avec Nuits > 0 ; lignes avec NPS = 99 ; valeurs manquantes Rev_Spa / Rev_Resto ; doublons = total − lignes uniques.

### Résultats constatés
- **Externes avec Nuits > 0 :** 15
- **Annulee = Oui avec Nuits > 0 :** 4 (incohérence logique à inclure dans la liste des anomalies pédagogiques)
- **NPS = 99 :** 3
- **Manquants Rev_Spa :** 526 (5,0 %) — **Manquants Rev_Resto :** 526 (5,0 %)
- **Doublons :** 10

### Interprétation
Les **anomalies sont présentes aux niveaux prévus** par la simulation. Le jeu de données est **adapté** pour faire travailler les étudiants sur la **détection et le traitement** des incohérences, valeurs extrêmes, manquants et doublons, dans un cadre pédagogique maîtrisé.

### Leçons à retenir
- **Avant toute analyse**, vérifier la **qualité des données** (incohérences, outliers, manquants, doublons).
- Ces étapes sont **indispensables** pour que les décisions ne soient pas biaisées par des erreurs ou des doublons.

### Information pour la prise de décision (gestionnaire)
**S’assurer de la fiabilité des données** avant toute décision. **Éviter des choix** basés sur des erreurs ou des doublons. **Améliorer la qualité** du pilotage et du reporting (processus de saisie, contrôles, nettoyage régulier).

---

## 9. Lien Spa × Sexe (situation accrue ou moindre des services spa)

Lorsque le fichier contient la colonne **Sexe** (pipeline évolution), le **rapport de validation (m10)** inclut une section **Lien Spa × Sexe** : tableau par sexe (effectif, moyenne Rev_Spa, part du total Rev_Spa, % avec Rev_Spa > 0) et ANOVA Rev_Spa par Sexe. Les revenus spa sont générés pour refléter environ **80 % depuis les femmes (F)** et **20 % depuis les hommes (M) et Autre** (m04). L’ANOVA est significative (p ≈ 0) : situation **accrue** pour F, **moindre** pour M/Autre. **Décision :** cibler l’offre spa selon le profil client et les dépenses par sexe.

---

## 10. Tarification dynamique (validation base mensuelle et base saison)

Le **rapport de validation (m10)** valide que la **tarification dynamique est pratiquée** sur deux bases (lorsque Mois_sejour, Saison_calendrier, Tarif_applique sont présents) :

- **Base mensuelle :** Tarif_applique moyen par Mois_sejour (1–12), ANOVA Tarif_applique par mois. Verdict : OK si p < 0,05 (écart significatif entre mois).
- **Base saison :** Tarif_applique moyen par Saison_calendrier (Basse / Épaule / Haute), ANOVA. Verdict : OK si p < 0,05 et Haute > Basse.

Utiliser **Saison_calendrier** (dérivée du mois), et non la colonne **Saison** (liée au segment). Voir **Note_Saison_vs_Tarification_Dynamique.docx** pour le détail.

---

## 11. Synthèse pour les professeurs et le client

- **Validité des données :** Les résultats des analyses sont **cohérents** avec la structure et les hypothèses du jeu de données (simulation). Les formules utilisées sont **standards** et reproductibles (voir `VERIFICATION_CALCULS_STATISTIQUES.md` et `verif_calculs_stats.py`).
- **Formation des étudiants :** Chaque technique est **exploitable** en cours (objectif, formule, interprétation, leçon, lien avec la décision). Le rapport Excel `rapport_validation_sondage_hotel.xlsx` et le tableau synthèse `tableau_synthese_techniques_statistiques.xlsx` complètent ce document pour la validation et la démonstration auprès des professeurs et du client.
- **Prise de décision en entreprise :** Les sections « Information pour la prise de décision (gestionnaire) » résument comment chaque analyse **soutient** le pilotage, la rentabilité et les choix opérationnels (canaux, forfaits, spa, restaurant, qualité des données).

---

*Rapport généré dans le cadre du projet L'Hôtel Boutique Art de Vivre. Données : sondage_hotel_data.csv. Analyses : module m10 et script verif_calculs_stats.py.*
