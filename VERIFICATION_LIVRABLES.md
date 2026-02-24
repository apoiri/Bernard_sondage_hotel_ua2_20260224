# Vérification des livrables – Ne pas se fier à la seule parole de l’assistant

**Objectif** : S’assurer que ce que tu as demandé a bien été fait. L’assistant (Cursor) n’a pas de mémoire entre les sessions et peut affirmer avoir fait un travail qui n’a pas été réalisé. Ce fichier décrit **comment vérifier** les livrables importants.

---

## Règle d’or

**Après chaque demande de modification, exige une preuve dans la même conversation :**
- « Montre-moi la preuve » ou « Fais une recherche dans le projet et affiche le résultat » ou « Ouvre la fin du fichier X et affiche les 5 dernières lignes ».

Si l’assistant ne peut pas afficher la preuve (fichier absent, phrase absente), le travail n’est pas fait.

---

## Vérifications types (à lancer toi-même ou à demander à l’assistant)

### 1. Modules Python « bloqués » (règle de blocage en fin de fichier)

**Ce qui doit être présent** : À la fin de chaque fichier `m01_config.py` … `m11_synthese_word_prof.py`, un bloc du type :
```text
# ========== RÈGLE DE BLOCAGE ==========
# Aucune modification de ce module n'est acceptée sans l'autorisation du maître d'ouvrage du projet.
```

**Comment vérifier (Terminal, depuis le dossier du projet) :**
```bash
grep -l "RÈGLE DE BLOCAGE" m*.py | wc -l
```
Résultat attendu : **11** (les 11 modules).

**Ou demander à l’assistant :** « Fais une recherche (grep) de "RÈGLE DE BLOCAGE" dans tous les fichiers m*.py et affiche le nombre de fichiers trouvés. » S’il affiche 11 et montre la liste des fichiers, c’est fait. Sinon, ce n’est pas fait.

---

### 2. Pipeline de validation (run_pipeline.py)

**Ce qui doit être fait** : Une seule commande exécute tous les modules (m01 → m09 → m10 → m11), produit les livrables (config.json, sondage_hotel_data.csv, rapport Excel, document Word), puis vérifie la règle de blocage et la présence des fichiers de sortie.

**Comment lancer :** Depuis le **Terminal macOS** (pas le terminal intégré de Cursor), dans le dossier du projet :
```bash
cd "/Users/alainpoirier/Desktop/Bernard_sondage_hotel_ua2_20260224"
python3 run_pipeline.py
```
Ou lancer `bash regenerer_livrables.sh` dans le même dossier. Exécuter depuis le terminal de Cursor peut ne pas mettre à jour les dates des fichiers dans le Finder.

**Résultat attendu** : Code de sortie **0**, message final « [OK] Pipeline terminé avec succès. Toutes les vérifications sont passées. »

**Vérifications automatiques effectuées par le pipeline :**
- Les 11 modules m*.py contiennent « RÈGLE DE BLOCAGE ».
- Les 4 fichiers de sortie existent : config.json, sondage_hotel_data.csv, rapport_validation_sondage_hotel.xlsx, synthese_elements_apprentissage_prof.docx.

Si une étape échoue (module en erreur ou vérification non passée), le script retourne un code non nul et affiche [ÉCHEC].

---

### 3. Autres livrables

Pour toute autre demande (ex. « le rapport Excel doit contenir un onglet X »), ajoute dans ce fichier une section du type :

**Livrable :** [description]  
**Où vérifier :** [fichier ou commande]  
**Preuve attendue :** [ce qu’on doit voir]

---

## À faire en fin de session

Quand l’assistant te dit avoir terminé une tâche :

1. **Dans la même conversation** : demande-lui d’exécuter la vérification correspondante (grep, extrait de fichier, etc.) et d’afficher le résultat.
2. Si le résultat ne correspond pas à ce qui est attendu → le travail n’est pas fait. Redemande la modification et la preuve.
3. Une fois la preuve reçue : **commit + push** (voir COMMENT_UTILISER_GIT.txt) pour figer l’état du projet.

---

## Résumé

- Ne te contente pas de « c’est fait ». **Exige une preuve affichée** (recherche, extrait de fichier).
- Utilise ce fichier pour noter **comment** vérifier chaque type de livrable important.
- En reprenant le projet : refais les vérifications clés (ex. grep « RÈGLE DE BLOCAGE ») pour confirmer que l’état du dépôt correspond bien à ce qui est attendu.
