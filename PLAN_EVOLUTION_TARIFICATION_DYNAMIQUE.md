# Plan d’évolution – Tarification dynamique, types de chambre et nouvelles variables

**Objectif** : Avant toute modification du code, ce document décrit le plan de développement pour introduire les types de chambre, une tarification dynamique (haute/basse saison), l’attribution réaliste des réservations aux chambres, et de nouvelles variables (sexe, niveau de revenus, provenance pays/province/ville), le tout piloté par une **interface utilisateur**.

---

## 1. Synthèse des objectifs

| Besoin | Description |
|--------|-------------|
| **Types de chambre** | Définir des catégories (ex. Standard, Supérieure, Luxe) avec un **prix de base** par type, saisi dans une interface. |
| **Tarification dynamique** | Ajuster les prix selon la saison : **basse saison** = prix plus bas pour attirer la clientèle ; **haute saison** = prix plus élevés (forte demande). Les **taux d’occupation moyens par mois** (saisis par l’utilisateur) pilotent la définition des périodes et l’amplitude des prix. |
| **Allocation réaliste** | Attribuer chaque réservation à un **type de chambre** (et idéalement à une chambre précise) de sorte que **toutes les chambres soient réservées au moins une fois dans l’année**. Contrôle à prévoir pour garantir ce réalisme. |
| **Nouvelles variables** | **Sexe** du client, **niveau de revenus** (plage fournie par l’utilisateur via l’interface), **provenance** : **pays**, **province**, **ville** (en s’appuyant sur les hypothèses déjà présentes ou à ajouter dans les modules). |
| **Interface utilisateur** | Une ou plusieurs interfaces pour saisir : types de chambre + prix de base, taux d’occupation par mois, plages de revenus, options de provenance (pays, provinces, villes). |

---

## 2. Périmètre fonctionnel détaillé

### 2.1 Types de chambre et prix de base

- **Interface** : L’utilisateur définit une liste de **types de chambre** (ex. Standard, Supérieure, Luxe, Suite) et un **prix de base** (ou fourchette) par type.
- **Données** : Chaque type est associé à un **nombre de chambres** (ex. 50 Standard, 30 Supérieure, 20 Luxe) et à un **tarif de base** ($/nuit). Le total des chambres peut rester 100 (projet actuel) ou être paramétrable.
- **Sortie** : Fichier de config ou table (ex. JSON/Excel) lisible par les modules de génération.

### 2.2 Taux d’occupation par mois et tarification dynamique

- **Interface** : L’utilisateur saisit un **taux d’occupation moyen pour chaque mois** (12 valeurs, ex. janvier 55 %, juillet 88 %, etc.). Ces taux servent à :
  - Définir les **périodes** haute / basse saison (ex. mois au-dessus d’un seuil = haute saison).
  - Piloter l’**amplitude** de la tarification dynamique : plus l’occupation mensuelle est élevée, plus le prix appliqué peut être élevé par rapport au prix de base ; en basse saison, on diminue pour attirer les clients.
- **Règle métier** : Pour chaque réservation, on connaît (ou on simule) un **mois** de séjour. Le **prix de la chambre** = prix de base du type de chambre × **coefficient dynamique** (dérivé du taux d’occupation du mois). Ex. : occupation 90 % → coefficient 1,2 ; occupation 50 % → coefficient 0,85.
- **Sortie** : Paramètres (seuils, coefficients min/max) stockés en config ; le module de calcul des revenus chambre (évolution de m03 ou nouveau module) applique la formule.

### 2.3 Attribution des réservations aux chambres (allocation réaliste)

- **Principe** : Chaque réservation est affectée à un **type de chambre** (et éventuellement à un **numéro de chambre** dans ce type). Un **contrôle** garantit que **toutes les chambres** (tous les numéros) sont **réservées au moins une fois** sur l’année.
- **Méthode possible** :
  - Générer un **calendrier annuel** (ou des créneaux par mois) avec un nombre de « nuits vendues » par type cohérent avec les taux d’occupation par mois et le nombre de chambres par type.
  - Attribuer les **réservations** (déjà générées avec date de séjour simulée) à des chambres en évitant les chevauchements (une chambre = une réservation à la fois pour des dates données).
  - En fin de processus, **vérifier** que chaque chambre a au moins une réservation sur l’année ; sinon, ajuster (réattribuer ou générer des réservations complémentaires).
- **Sortie** : Colonnes **Type_chambre**, éventuellement **Numero_chambre**, et **Date_arrivee** / **Date_depart** (ou mois) dans le jeu de données.

### 2.4 Nouvelles variables : sexe, niveau de revenus, provenance

- **Sexe** : Variable catégorielle (ex. M, F, Autre) à ajouter au début de la chaîne (m02 ou module dédié). Répartition saisie par l’utilisateur (ex. 50 % / 50 %) ou tirée aléatoirement.
- **Niveau de revenus** : Plages définies par l’utilisateur dans l’interface (ex. Faible &lt; 40 k$, Moyen 40–80 k$, Élevé &gt; 80 k$). Chaque client se voit attribuer une catégorie (éventuellement en lien avec le segment ou le canal).
- **Provenance** : **Pays**, **Province/État**, **Ville**. Réutiliser ou étendre les hypothèses déjà présentes dans les modules (segments, canaux). L’interface permet de définir une liste de pays, de provinces par pays, de villes par province, et des poids (répartition) pour tirer la provenance de chaque client.

### 2.5 Interface utilisateur (résumé)

- **Écran 1 – Types de chambre** : Saisie des types, nombre de chambres par type, prix de base par type.
- **Écran 2 – Occupation et saison** : Saisie des 12 taux d’occupation mensuels ; optionnellement seuils haute/basse saison et coefficients min/max pour la tarification dynamique.
- **Écran 3 – Nouvelles variables** : Répartition sexe ; plages de revenus (bornes) ; liste pays / provinces / villes avec poids.
- **Sortie interface** : Fichier(s) de configuration (JSON, Excel ou CSV) alimentant la génération sans modifier les modules validés en direct (lecture de la config par un module « config étendue » ou par m01 si déblocage).

---

## 3. Architecture proposée (modules et flux)

### 3.1 Contraintes

- Les **modules m01 à m11** sont **validés** (liste validated_modules.txt). On évite de les modifier directement ; on privilégie des **nouveaux fichiers** ou une **couche de config étendue** lue par de nouveaux modules.
- **m01** reste la référence pour les paramètres existants. Les **nouveaux paramètres** (types de chambre, taux par mois, revenus, provenance) peuvent être dans un **fichier séparé** (ex. `config_tarification_dynamique.json`) généré par l’interface et lu par un **nouveau module** en amont ou en parallèle de m02/m03.

### 3.2 Nouveaux composants proposés

| Composant | Rôle |
|-----------|------|
| **Interface utilisateur** | Web (Flask/Streamlit) ou desktop (Tkinter) ou formulaire → JSON/Excel. Saisie : types de chambre + prix, 12 taux d’occupation, sexe/revenus/provenance. Export vers `config_tarification_dynamique.json` (et éventuellement mise à jour partielle de m01 si déblocage). |
| **Module config étendue** (ex. **m00_config_etendue.py**) | Charge la config de base (m01) + le fichier généré par l’interface. Expose une fonction `get_config_etendue()` utilisée par les modules d’évolution. Ne modifie pas m01. |
| **Module types de chambre et calendrier** (ex. **m02b_types_chambre_calendrier.py**) | À partir de la config étendue : définit les types de chambre, le nombre de chambres par type, et un **calendrier annuel** (mois par mois) avec taux d’occupation et coefficients de prix. Produit une table « disponibilités » ou « créneaux » par type. |
| **Évolution génération réservations** (ex. **m02c_reservations_avec_dates.py**) | Génère les réservations (comme m02) en ajoutant : **mois de séjour** (ou date d’arrivée), **sexe**, **niveau de revenus**, **pays**, **province**, **ville**. Utilise les répartitions et listes fournies par l’interface. Peut s’appuyer sur les segments/canaux existants. |
| **Module allocation chambres** (ex. **m02d_allocation_chambres.py**) | Prend les réservations (avec mois ou dates) et les **attribue à un type de chambre** puis à un **numéro de chambre** concret, en respectant les capacités par type et en évitant les chevauchements. **Contrôle final** : vérifier que toute chambre a au moins une réservation sur l’année ; sinon, ajuster ou signaler. |
| **Module tarification dynamique et Rev_Chambre** (ex. **m03b_revenus_chambre_dynamique.py**) | Pour chaque réservation : type de chambre + mois (ou saison) → **coefficient dynamique** (dérivé des taux d’occupation mensuels) → **prix appliqué** = prix de base du type × coefficient. Calcule **Rev_Chambre** et peut écrire **Tarif_applique**, **Type_chambre**, etc. Remplace ou complète m03 pour le revenu chambre. |
| **Chaîne existante** | À partir de m04 (Rev_Resto, Rev_Spa, etc.), la chaîne actuelle (m04 → m09) reste utilisée ; les nouveaux champs (sexe, revenus, provenance, type chambre, tarif dynamique) sont déjà dans le DataFrame. m09 exporte toutes les colonnes. |

### 3.3 Flux de données (schéma)

```
[Interface utilisateur]
    → config_tarification_dynamique.json (types chambre, prix base, 12 taux, sexe/revenus/provenance)
           ↓
[m00_config_etendue]  ← m01 (config actuelle)
    → get_config_etendue()
           ↓
[m02b_types_chambre_calendrier]  → calendrier / coefficients par mois
           ↓
[m02 ou m02c]  → réservations + mois + sexe + revenus + pays + province + ville
           ↓
[m02d_allocation_chambres]  → Type_chambre, Numero_chambre, contrôle « toutes chambres réservées »
           ↓
[m03b_revenus_chambre_dynamique]  → Rev_Chambre (tarification dynamique), Tarif_applique
           ↓
[m04 … m09]  → reste de la chaîne, export CSV avec toutes les colonnes
```

---

## 4. Contrôle « allocation réaliste »

- **Objectif** : Chaque chambre (chaque numéro) doit être réservée **au moins une fois** sur l’année.
- **Méthode** :
  1. Après attribution des réservations aux chambres (m02d), lister toutes les chambres (par type puis numéro).
  2. Pour chaque chambre, compter le nombre de réservations qui la concernent (sur l’année).
  3. Si une chambre a 0 réservation : **alerte** et soit (a) réattribuer une réservation existante vers cette chambre (en modifiant Type_chambre / Numero_chambre), soit (b) générer une réservation supplémentaire pour cette chambre. Répéter jusqu’à ce que toutes les chambres aient au moins 1 réservation.
  4. Optionnel : rapport (Excel ou log) listant les chambres et le nombre de réservations par chambre pour validation par l’utilisateur.

---

## 5. Réutilisation des hypothèses existantes (provenance, segments)

- **Segments** (m01/m02) : Les segments (Affaires_Solo, Congressiste, Loisirs_Couple, etc.) peuvent rester ; on ajoute **provenance** (pays, province, ville) et **sexe** / **niveau de revenus** en complément. La provenance peut être corrélée aux segments (ex. Loisirs plus souvent de certaines régions) si on le souhaite.
- **Canaux** : Inchangés ; les canaux de réservation restent utilisés pour les réservations.
- **Saison** : Actuellement chaque réservation a un attribut **Saison** (Basse/Haute). On le fait dériver du **mois** de séjour et des **taux d’occupation par mois** : les mois avec occupation au-dessus d’un seuil = Haute, les autres = Basse. Ainsi la « saison » reste cohérente avec la tarification dynamique.

---

## 6. Phases d’implémentation suggérées

| Phase | Contenu | Livrable |
|-------|---------|----------|
| **1** | Spécification détaillée de l’interface (écrans, champs, format JSON/Excel de sortie) et du schéma de **config_tarification_dynamique.json**. | Document spec interface + exemple de fichier JSON. |
| **2** | **m00_config_etendue** : lecture m01 + lecture du fichier interface ; exposition `get_config_etendue()`. | Module testé, config étendue disponible. |
| **3** | **m02b** : types de chambre, calendrier mensuel, coefficients de prix par mois. | Module + tests unitaires. |
| **4** | **m02c** (ou extension m02) : génération des réservations avec **mois**, **sexe**, **niveau de revenus**, **pays**, **province**, **ville**. | Données enrichies. |
| **5** | **m02d** : allocation des réservations aux types de chambre et aux numéros de chambre ; **contrôle** « toutes chambres réservées ». | Module + rapport de contrôle. |
| **6** | **m03b** : calcul **Rev_Chambre** par tarification dynamique (prix base × coefficient mois). | Rev_Chambre réaliste par type et saison. |
| **7** | **Interface utilisateur** (Streamlit ou autre) : saisie types de chambre, 12 taux, sexe/revenus/provenance ; export config. | Application utilisable. |
| **8** | Intégration dans le **pipeline** (run_pipeline ou nouveau script) : m00 → m02b → m02c → m02d → m03b → m04 … m09. Documentation et vérification des livrables. | Pipeline complet et documenté. |

---

## 7. Points d’attention

- **Compatibilité** : Les modules m04 à m11 attendent un DataFrame avec un certain nombre de colonnes. Les **nouvelles colonnes** (Type_chambre, Sexe, Revenus, Pays, Province, Ville, Tarif_applique, etc.) sont **ajoutées** ; les colonnes existantes sont conservées pour ne pas casser m04–m11.
- **Performance** : L’allocation réaliste (éviter chevauchements, garantir une réservation par chambre) peut nécessiter un algorithme de type « assignation » ou itératif ; à dimensionner selon le volume (10 500 réservations, 100 chambres).
- **Validation** : Conserver la possibilité de lancer l’ancien pipeline (sans tarification dynamique) pour comparer ou pour livraisons pédagogiques « simple » ; par ex. un flag ou un fichier config vide pour désactiver les nouveaux modules.

---

## 8. Résumé

- **Interface** : Saisie types de chambre + prix de base, **taux d’occupation par mois**, plages de revenus, sexe, provenance (pays, province, ville).
- **Tarification dynamique** : Prix = prix de base (par type de chambre) × coefficient dérivé du taux d’occupation du mois (basse saison = baisse de prix, haute saison = hausse).
- **Allocation** : Chaque réservation est affectée à un type de chambre et à un numéro de chambre ; **contrôle** pour que toutes les chambres soient réservées au moins une fois dans l’année.
- **Nouvelles variables** : Sexe, niveau de revenus, pays, province, ville (provenance), en s’appuyant sur les hypothèses des modules existants.
- **Modules** : Nouveaux fichiers (m00, m02b, m02c, m02d, m03b) et interface ; pas de modification des modules validés m01–m11 tant qu’aucun déblocage n’est décidé.

Ce plan peut servir de base pour détailler chaque phase (user stories, maquettes d’écran, schémas JSON) avant de commencer les modifications de script.
