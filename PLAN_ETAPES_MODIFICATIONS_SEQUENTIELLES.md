# Plan étape par étape – Modifications séquentielles (un module à la fois)

**Règles impératives :**
1. **Un seul module est modifié ou créé par étape.**
2. On s’en tient **uniquement aux modifications requises** pour cette étape (pas d’ajustements sur d’autres fichiers).
3. Chaque étape comprend : **modification** → **test** → **validation du fonctionnement** → **blocage du module** (on n’y revient plus).
4. Une fois un module bloqué, il est ajouté à **validated_modules.txt** (ou à une liste dédiée « modules évolution ») et n’est plus modifié.

**Référence fonctionnelle :** PLAN_EVOLUTION_TARIFICATION_DYNAMIQUE.md

---

## Ordre des étapes (séquence à respecter)

| Étape | Module / composant | Statut (à mettre à jour) |
|-------|--------------------|---------------------------|
| 1 | m00_config_etendue.py | **Validé et bloqué** |
| 2 | Fichier config minimal (JSON) + schéma | **Validé** |
| 3 | m02b_types_chambre_calendrier.py | **Validé et bloqué** |
| 4 | m02c_reservations_avec_dates.py | **Validé et bloqué** |
| 5 | m02d_allocation_chambres.py | **Validé et bloqué** |
| 6 | m03b_revenus_chambre_dynamique.py | **Validé et bloqué** |
| 7 | Interface utilisateur (génération JSON) | **Validé** |
| 8 | Intégration pipeline (script d’enchaînement) | **Validé** |

---

## Modèle de déroulement pour chaque étape

Pour **chaque** étape, suivre strictement :

1. **Faire** : uniquement les modifications prévues pour ce module (fichiers listés dans la section de l’étape).
2. **Tester** : exécuter le test décrit (commande ou script).
3. **Valider** : vérifier que les critères de validation sont remplis.
4. **Bloquer** : ajouter le(s) fichier(s) du module à la liste des modules bloqués (validated_modules.txt ou liste « évolution »), puis marquer l’étape comme **Validé et bloqué** dans ce document.

---

## Étape 1 – Module m00_config_etendue.py

**Objectif :** Créer un module qui charge la config de base (m01) et, si présent, le fichier `config_tarification_dynamique.json`, puis expose une fonction `get_config_etendue()`.

**Modifications (uniquement) :**
- Créer le fichier **m00_config_etendue.py** à la racine du projet.
- Contenu minimal : import de `get_config` depuis m01 ; lecture optionnelle de `config_tarification_dynamique.json` (si le fichier n’existe pas, retourner uniquement la config m01) ; fonction `get_config_etendue()` qui retourne un dictionnaire fusionné (config m01 + clés du JSON si présentes).
- Aucune modification des autres fichiers.

**Test :**
```bash
cd "/Users/alainpoirier/Desktop/Bernard_sondage_hotel_ua2_20260224"
python3 -c "
from m00_config_etendue import get_config_etendue
c = get_config_etendue()
assert 'N_RESERVATIONS' in c or 'NB_CHAMBRES' in c
print('OK:', list(c.keys())[:5])
"
```

**Critères de validation :**
- Le script ci-dessus s’exécute sans erreur.
- `get_config_etendue()` retourne au minimum les clés de la config m01 (ex. N_RESERVATIONS, NB_CHAMBRES).
- Si `config_tarification_dynamique.json` existe, les clés de ce fichier sont présentes dans le dictionnaire retourné.

**Blocage :**
- Ajouter **m00_config_etendue.py** à **validated_modules.txt** (ou à une liste **modules_evolution_valides.txt** si vous préférez séparer les modules « évolution » des modules de base).
- Marquer l’étape 1 comme **Validé et bloqué** dans le tableau ci-dessus.

---

## Étape 2 – Fichier config minimal et schéma (JSON)

**Objectif :** Définir la structure du fichier produit par l’interface (types de chambre, prix de base, 12 taux d’occupation, etc.) et fournir un fichier JSON minimal pour les tests des modules suivants.

**Modifications (uniquement) :**
- Créer **config_tarification_dynamique_exemple.json** (ou **config_tarification_dynamique.json** avec des valeurs de test) contenant au minimum : types de chambre (noms, nombre de chambres, prix de base), 12 taux d’occupation par mois, optionnellement répartition sexe, plages de revenus, liste pays/provinces/villes.
- Optionnel : créer **SCHEMA_CONFIG_TARIFICATION.md** (ou .json) décrivant les clés attendues.
- Aucune modification des modules Python.

**Test :**
- Vérifier que le JSON est valide : `python3 -c "import json; json.load(open('config_tarification_dynamique_exemple.json'))"`.
- Vérifier que m00 charge ce fichier si présent : placer le fichier à la racine, relancer le test de l’étape 1 et vérifier que les nouvelles clés apparaissent dans `get_config_etendue()`.

**Critères de validation :**
- Le fichier JSON est valide et contient au moins : types de chambre (avec prix de base), 12 taux d’occupation.
- m00_config_etendue (déjà bloqué) retourne bien ces données lorsque le fichier est présent.

**Blocage :**
- Pas de « blocage » au sens fichier Python ; considérer l’étape comme **validée** une fois les critères remplis. La structure du JSON est figée pour les étapes suivantes (ne pas changer le schéma sans mise à jour du plan).

---

## Étape 3 – Module m02b_types_chambre_calendrier.py

**Objectif :** À partir de la config étendue, produire une structure « types de chambre » et un calendrier (coefficients de prix par mois dérivés des taux d’occupation).

**Modifications (uniquement) :**
- Créer **m02b_types_chambre_calendrier.py**.
- Le module lit `get_config_etendue()`, extrait les types de chambre et les 12 taux d’occupation, calcule un coefficient de tarification par mois (ex. occupation haute → coefficient > 1, basse → < 1), et expose une fonction (ex. `get_types_chambre()`, `get_coefficient_mois(mois)`) ou une table utilisable par m02c/m03b.
- Aucune modification de m00, m01, m02, etc.

**Test :**
```bash
python3 -c "
from m02b_types_chambre_calendrier import get_types_chambre, get_coefficient_mois  # adapter aux noms réels
types = get_types_chambre()
assert len(types) >= 1
c = get_coefficient_mois(1)
assert c > 0
print('OK')
"
```

**Critères de validation :**
- Les fonctions s’exécutent sans erreur avec le fichier config exemple en place.
- Les types de chambre et les coefficients par mois sont cohérents (ex. mois à forte occupation → coefficient plus élevé).

**Blocage :**
- Ajouter **m02b_types_chambre_calendrier.py** à la liste des modules validés (validated_modules.txt ou modules_evolution_valides.txt).
- Marquer l’étape 3 comme **Validé et bloqué**.

---

## Étape 4 – Module m02c_reservations_avec_dates.py

**Objectif :** Générer ou enrichir les réservations avec : mois de séjour (ou date), sexe, niveau de revenus, pays, province, ville. S’appuyer sur m02 existant (ne pas le modifier) : appeler m02.run() puis enrichir le DataFrame avec les nouvelles colonnes à partir de la config étendue.

**Modifications (uniquement) :**
- Créer **m02c_reservations_avec_dates.py** qui importe m02, exécute `m02.run()`, puis ajoute les colonnes **Mois_sejour** (ou Date_arrivee), **Sexe**, **Niveau_revenus**, **Pays**, **Province**, **Ville** en utilisant les listes et répartitions de la config étendue.
- Aucune modification de m02 ni des autres modules.

**Test :**
```bash
python3 -c "
import m02c_reservations_avec_dates
df = m02c_reservations_avec_dates.run()  # ou run(df) selon design
for col in ['Sexe', 'Mois_sejour', 'Pays']:  # adapter aux noms réels
    assert col in df.columns
print('OK')
"
```

**Critères de validation :**
- Le DataFrame retourné contient les colonnes existantes de m02 plus les nouvelles (Sexe, Mois_sejour, Niveau_revenus, Pays, Province, Ville).
- Aucune erreur à l’exécution ; les valeurs sont cohérentes (ex. répartition sexe respectée).

**Blocage :**
- Ajouter **m02c_reservations_avec_dates.py** à la liste des modules validés.
- Marquer l’étape 4 comme **Validé et bloqué**.

---

## Étape 5 – Module m02d_allocation_chambres.py

**Objectif :** Attribuer à chaque réservation un type de chambre et un numéro de chambre ; vérifier que toutes les chambres sont réservées au moins une fois dans l’année.

**Modifications (uniquement) :**
- Créer **m02d_allocation_chambres.py** qui reçoit le DataFrame (sortie m02c) et les infos types de chambre (m02b ou config), attribue Type_chambre et Numero_chambre à chaque ligne, puis exécute le **contrôle** : toutes les chambres ont au moins 1 réservation ; sinon, ajustement ou alerte.
- Aucune modification des modules déjà bloqués.

**Test :**
```bash
python3 -c "
import m02c_reservations_avec_dates
import m02d_allocation_chambres
df = m02c_reservations_avec_dates.run()
df = m02d_allocation_chambres.run(df)
assert 'Type_chambre' in df.columns and 'Numero_chambre' in df.columns
# Vérifier contrôle : toutes chambres réservées au moins 1 fois
ok = m02d_allocation_chambres.verifier_toutes_chambres_reservees(df)
assert ok
print('OK')
"
```

**Critères de validation :**
- Colonnes Type_chambre et Numero_chambre présentes.
- Le contrôle « toutes chambres réservées au moins une fois » est satisfait (ou une alerte claire est émise si impossible sans ajustement).

**Blocage :**
- Ajouter **m02d_allocation_chambres.py** à la liste des modules validés.
- Marquer l’étape 5 comme **Validé et bloqué**.

---

## Étape 6 – Module m03b_revenus_chambre_dynamique.py

**Objectif :** Calculer Rev_Chambre (et éventuellement Tarif_applique) à partir du type de chambre, du mois et des coefficients de tarification dynamique (prix de base × coefficient du mois).

**Modifications (uniquement) :**
- Créer **m03b_revenus_chambre_dynamique.py** qui reçoit le DataFrame (sortie m02d), utilise le type de chambre et le mois pour obtenir le coefficient (m02b) et le prix de base (config), calcule Rev_Chambre = Nuits × prix_base × coefficient (0 si Externe ou Annulée), et ajoute éventuellement la colonne Tarif_applique.
- Ne pas modifier m03.

**Test :**
```bash
python3 -c "
import m02_segments
import m02c_reservations_avec_dates
import m02d_allocation_chambres
import m03b_revenus_chambre_dynamique
# Chaîne minimale pour tester m03b (adapter si m02c dépend de m02 seulement)
df = m02_segments.run()
# ... enrichir avec m02c, m02d si nécessaire pour avoir Type_chambre, Mois
# Puis :
# df = m03b_revenus_chambre_dynamique.run(df)
# assert 'Rev_Chambre' in df.columns
# print('OK')
"
```
(À adapter selon la chaîne réelle : m02c peut appeler m02 en interne, donc le test pourra être simplifié.)

**Critères de validation :**
- Rev_Chambre est cohérent avec le type de chambre, le mois et la règle de tarification dynamique (ex. haute occupation → prix plus élevé).
- Les réservations Externes ou Annulées ont Rev_Chambre = 0.

**Blocage :**
- Ajouter **m03b_revenus_chambre_dynamique.py** à la liste des modules validés.
- Marquer l’étape 6 comme **Validé et bloqué**.

---

## Étape 7 – Interface utilisateur (génération du JSON)

**Objectif :** Fournir une interface (script en ligne de commande, Streamlit, ou formulaire) permettant de saisir types de chambre + prix de base, 12 taux d’occupation, sexe/revenus/provenance, et d’exporter **config_tarification_dynamique.json**.

**Modifications (uniquement) :**
- Créer le script ou l’application (ex. **interface_config_tarification.py** ou dossier **interface/** avec une app Streamlit).
- L’interface ne modifie aucun des modules m00, m02b, m02c, m02d, m03b ; elle ne fait qu’écrire le fichier JSON.

**Test :**
- Lancer l’interface, remplir les champs (ou utiliser des valeurs par défaut), exporter le JSON.
- Vérifier que le fichier généré est valide et que m00 le charge correctement (relancer le test de l’étape 1 avec ce fichier).

**Critères de validation :**
- Le fichier JSON produit est valide et conforme au schéma attendu par m00/m02b.
- Aucun module déjà bloqué n’a été modifié.

**Blocage :**
- Ajouter le(s) fichier(s) de l’interface à la liste des livrables validés (ou à une liste dédiée). Considérer l’étape 7 comme **Validée**.

---

## Étape 8 – Intégration pipeline

**Objectif :** Enchaîner m00 → m02b → m02c → m02d → m03b puis m04 … m09 dans un script (ex. **run_pipeline_evolution.py** ou option dans run_pipeline.py) et vérifier que le CSV final contient toutes les colonnes attendues.

**Modifications (uniquement) :**
- Créer ou adapter **un seul** script d’enchaînement qui appelle dans l’ordre : m00 (chargement config), m02b (calendrier), m02 (run), m02c (enrichissement), m02d (allocation), m03b (Rev_Chambre dynamique), puis m04 à m09.
- Ne pas modifier m04 à m11.

**Test :**
```bash
python3 run_pipeline_evolution.py
# Puis vérifier :
# - sondage_hotel_data.csv existe et contient Type_chambre, Sexe, Rev_Chambre, etc.
# - Aucune erreur pendant l’exécution
```

**Critères de validation :**
- Le pipeline s’exécute sans erreur de bout en bout.
- Le CSV contient les colonnes existantes plus les nouvelles (Type_chambre, Numero_chambre, Sexe, Niveau_revenus, Pays, Province, Ville, Rev_Chambre cohérent avec la tarification dynamique).

**Blocage :**
- Considérer le script de pipeline d’évolution comme **validé**. Ne pas modifier les modules déjà bloqués.

---

## Liste des modules à bloquer (à mettre à jour après chaque étape)

Après validation de chaque étape, ajouter le fichier concerné à la liste ci-dessous (et à **validated_modules.txt** ou **modules_evolution_valides.txt** selon votre choix).

| Fichier | Ajouté après étape |
|---------|--------------------|
| m00_config_etendue.py | 1 |
| m02b_types_chambre_calendrier.py | 3 |
| m02c_reservations_avec_dates.py | 4 |
| m02d_allocation_chambres.py | 5 |
| m03b_revenus_chambre_dynamique.py | 6 |
| interface (fichier(s)) | 7 |
| run_pipeline_evolution.py | 8 |

---

## Récapitulatif des règles

- **Un module à la fois** : seule l’étape en cours touche à des fichiers.
- **Uniquement les modifications requises** : pas de refactor ou d’amélioration hors périmètre de l’étape.
- **Test puis validation** : chaque étape est validée par le test et les critères avant blocage.
- **Blocage = ne plus modifier** : une fois le module ajouté à la liste validée, on n’y revient pas (sauf déblocage formel décidé par le maître d’ouvrage).

Ce plan peut être suivi tel quel pour réaliser les évolutions dans l’ordre, avec validation et blocage à chaque étape.
