# Vérification des calculs statistiques du rapport de validation

Ce document décrit les calculs réalisés dans le module 10 (rapport de validation) et **comment vérifier** qu’ils sont adéquats. Les formules sont standards ; les implémentations utilisent **NumPy**, **Pandas** et **SciPy**, des bibliothèques de référence.

---

## 1. Méthodes utilisées dans le rapport

| Section | Méthode | Implémentation (m10) | Référence |
|--------|---------|----------------------|-----------|
| Proportions + IC 95 % | Approximation normale | `z * sqrt(p(1-p)/n)` avec z=1.96 | IC pour une proportion, n grand |
| Khi-deux | Test d’indépendance | `scipy.stats.chi2_contingency` | Tableau de contingence Segment × Type_Forfait |
| Pearson | Corrélation linéaire | `scipy.stats.pearsonr` | Rev_Spa vs Satisfaction_NPS |
| ANOVA | Comparaison de moyennes (1 facteur) | `scipy.stats.f_oneway` | Rev_Resto par Segment |
| Régression | MCO (moindres carrés ordinaires) | `np.linalg.lstsq` (modèle avec constante) | Total_Facture ~ Rev_Chambre + Rev_Resto + Rev_Spa |
| Annulations | Proportions par groupe | Comptages puis ratio | Taux Direct / Intermédiaire |
| Qualité | Comptages | Masques booléens + `drop_duplicates` | Anomalies pédagogiques |

Aucune modification n’est apportée aux modules validés ; la vérification se fait **en parallèle** (script indépendant ou comparaison manuelle).

---

## 2. Détail des formules (pour contrôle manuel ou autre logiciel)

### 2.1 IC 95 % pour une proportion

- **Formule** : \( p \pm 1{,}96 \sqrt{\dfrac{p(1-p)}{n}} \)
- **Condition** : \( n \cdot p \geq 5 \) et \( n(1-p) \geq 5 \) (approximation normale).
- Dans le code : `_ic_proportion(p, n)` avec z = 1.96.

### 2.2 Khi-deux d’indépendance

- **Tableau** : effectifs croisés Segment (lignes) × Type_Forfait (colonnes).
- **Statistique** : \( \chi^2 = \sum \dfrac{(O - E)^2}{E} \) (O = observé, E = attendu sous indépendance).
- **ddl** : (nombre de lignes − 1) × (nombre de colonnes − 1).
- Le rapport utilise `scipy.stats.chi2_contingency`, qui fait exactement ce calcul.

### 2.3 Corrélation de Pearson

- **Formule** : \( r = \dfrac{\text{Cov}(X,Y)}{s_X \cdot s_Y} \), avec covariance et écarts-types sur les paires (sans NaN).
- Le rapport utilise `scipy.stats.pearsonr` (même définition).

### 2.4 ANOVA à un facteur (Rev_Resto par Segment)

- Comparaison des moyennes de Rev_Resto entre les segments.
- **F** : rapport (variance inter-groupes / ddl1) / (variance intra-groupes / ddl2).
- Le rapport utilise `scipy.stats.f_oneway(group1, group2, ...)`.

### 2.5 Régression linéaire multiple

- **Modèle** : Total_Facture = β₀ + β₁·Rev_Chambre + β₂·Rev_Resto + β₃·Rev_Spa + ε.
- **Estimation** : MCO via `np.linalg.lstsq` sur la matrice [1, Rev_Chambre, Rev_Resto, Rev_Spa].
- **R²** : \( R^2 = 1 - \dfrac{\sum(y - \hat{y})^2}{\sum(y - \bar{y})^2} \).

---

## 3. Comment s’assurer que les calculs sont adéquats

### Option A – Script de recalcul indépendant (recommandé)

Un script **hors** des modules validés recalcule les mêmes indicateurs à partir du CSV et affiche les résultats :

```bash
python3 verif_calculs_stats.py
```

Vous comparez la sortie du script avec :
- le rapport affiché dans le terminal par `m10_rapport_validation.py`, ou  
- les onglets du fichier `rapport_validation_sondage_hotel.xlsx`.

Si les chiffres coïncident (à l’arrondi près), les calculs du module 10 sont cohérents avec des formules explicites / SciPy.

### Option B – Vérification manuelle sur un sous-ensemble

1. **Proportions** : Dans Excel, sur le CSV, calculez par exemple `=NB.SI(Annulee;"Oui")/NB(Annulee)` et comparez au % Annulées du rapport.
2. **Pearson** : Dans Excel, `=COEFFICIENT.CORRELATION(Rev_Spa; Satisfaction_NPS)` sur les lignes non annulées et sans NaN → à comparer à l’onglet Pearson du rapport.
3. **Régression** : Utilisez la fonction DROITEREG (ou l’outil Analyse → Régression) sur Total_Facture en Y et Rev_Chambre, Rev_Resto, Rev_Spa en X ; comparez constante et coefficients à l’onglet Regression.

### Option C – Comparaison avec un autre logiciel

- **R** : `cor()`, `chisq.test()`, `aov()`, `lm()` donnent les mêmes statistiques pour les mêmes données.
- **Excel** : Fonctions KHI2, COEFFICIENT.CORRELATION, DROITEREG, etc., pour des contrôles ciblés.

### Option D – Vérifier les prérequis des tests

- **Khi-deux** : effectifs théoriques ≥ 5 (sinon regroupement ou test exact). Avec ~10k lignes et 5 segments × 2 forfaits, les effectifs sont largement suffisants.
- **ANOVA** : hypothèse de normalité des résidus par groupe (approximation acceptable pour grands échantillons).
- **Régression** : linéarité, homoscédasticité (le rapport ne fait pas de tests de diagnostic ; les coefficients attendus ~1 ; 1,1 ; 1,3 servent de garde-fou).

---

## 4. Résumé

| Vérification | Action |
|--------------|--------|
| **Cohérence interne** | Lancer `python3 verif_calculs_stats.py` et comparer à la sortie de m10 ou au fichier Excel. |
| **Formules** | Ce document + code du module 10 (lecture seule) : formules standards (IC proportion, χ², Pearson, F, MCO, R²). |
| **Prérequis** | Effectifs suffisants pour le Khi-deux ; échantillons grands pour ANOVA et régression. |

En pratique : exécuter **verif_calculs_stats.py** après chaque génération du CSV donne une assurance rapide que les calculs statistiques du rapport sont adéquats et reproductibles.
