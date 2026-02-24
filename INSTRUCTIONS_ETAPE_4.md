# Instructions – Étape 4 (m02c_reservations_avec_dates)

## Ce qui a été fait

- **Fichier créé** : `m02c_reservations_avec_dates.py`
  - Appelle `m02.run()` pour obtenir le DataFrame segments.
  - Lit la config étendue via m00 (`get_config_etendue()`).
  - Ajoute les colonnes : **Mois_sejour** (1–12, pondéré par taux d’occupation), **Sexe**, **Niveau_revenus**, **Pays**, **Province**, **Ville** (tirées des listes et répartitions de la config).
  - Si la config étendue n’a pas ces clés, des valeurs par défaut sont utilisées (ex. Pays = Canada, Sexe 50/50 M-F).

---

## Instructions à réaliser (vous)

### 1. Tester le module

Dans le terminal (depuis le dossier du projet) :

```bash
cd "/Users/alainpoirier/Desktop/Bernard_sondage_hotel_ua2_20260224"
python3 -c "
import m02c_reservations_avec_dates
df = m02c_reservations_avec_dates.run()
for col in ['Sexe', 'Mois_sejour', 'Pays', 'Niveau_revenus', 'Province', 'Ville']:
    assert col in df.columns
print('OK')
"
```

**Résultat attendu** : affichage de `OK` (sans erreur).

### 2. (Optionnel) Vérifier les valeurs

```bash
python3 m02c_reservations_avec_dates.py
```

Vous devez voir un aperçu des colonnes et quelques lignes avec Mois_sejour, Sexe, Niveau_revenus, Pays, Province, Ville.

### 3. Bloquer le module — **déjà fait**

- **validated_modules.txt** : `m02c_reservations_avec_dates.py` a été ajouté.
- **PLAN_ETAPES_MODIFICATIONS_SEQUENTIELLES.md** : étape 4 marquée **Validé et bloqué**.
- **HISTORIQUE_SESSION_2026-02-24.md** et **ARCHIVE_PROJET_SONDAGE_HOTEL.md** : m02c documenté.

---

## Résumé

| Action | Fichier / endroit |
|--------|--------------------|
| Tester | `python3 -c "import m02c_reservations_avec_dates; ..."` |
| Bloquer | **validated_modules.txt** : ajouter `m02c_reservations_avec_dates.py` |
| Marquer étape | **PLAN_ETAPES_MODIFICATIONS_SEQUENTIELLES.md** : étape 4 = Validé et bloqué |
| Documenter | **HISTORIQUE_SESSION_2026-02-24.md**, **ARCHIVE_PROJET_SONDAGE_HOTEL.md** (optionnel) |

Une fois ces points faits, l’étape 4 est terminée. Prochaine étape : **5 – m02d_allocation_chambres.py**.
