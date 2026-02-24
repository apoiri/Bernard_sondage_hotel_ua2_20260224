# Interface utilisateur – Modification de la config tarification dynamique

Une **interface graphique (Streamlit)** permet de modifier les valeurs de la configuration étendue (types de chambre, taux d'occupation, sexe, revenus, pays, etc.) puis d'exporter **config_tarification_dynamique.json**. Après export, relancez **run_pipeline_evolution.py** pour régénérer le CSV avec ces valeurs.

## Installation

```bash
pip install -r requirements_interface.txt
```

(ou : `pip install streamlit`)

## Lancer l'interface

Depuis le dossier du projet :

**Option 1 – Ouvrir directement dans Chrome (recommandé si Safari pose problème) :**
```bash
cd "/Users/alainpoirier/Desktop/Bernard_sondage_hotel_ua2_20260224"
./lancer_interface_chrome.sh
```
Ce script lance Streamlit puis ouvre **Chrome** sur la page (pas Safari). Pour arrêter : **Ctrl+C** dans le terminal.

**Option 2 – Lancer Streamlit seul (le navigateur par défaut s’ouvrira) :**
```bash
streamlit run interface_streamlit_config.py
```
Si rien ne s’ouvre, ouvrez **Chrome** et allez à : **http://localhost:8501**

## Ce que vous pouvez modifier

1. **Types de chambre** : nom, nombre de chambres, prix de base ($/nuit). Bouton pour ajouter un type.
2. **Taux d'occupation** : 12 curseurs (janvier à décembre), entre 0 et 100 %.
3. **Répartition sexe** : proportions M / F / Autre (la somme doit faire 1).
4. **Plages de revenus** : libellé, min, max pour chaque tranche.
5. **Pays** : code, nom, poids pour chaque pays.

Après avoir modifié les valeurs, cliquez sur **« Enregistrer config_tarification_dynamique.json »**. Le fichier est écrit à la racine du projet. Puis exécutez :

```bash
python3 run_pipeline_evolution.py
```

pour régénérer **sondage_hotel_data.csv**, le rapport Excel et la synthèse Word avec les nouvelles valeurs.

## Fichiers concernés

| Fichier | Rôle |
|---------|------|
| **interface_streamlit_config.py** | Application Streamlit (formulaires, export JSON). |
| **interface_config_tarification.py** | Script en ligne de commande (sans interface graphique) ; option `--interactif` pour une saisie limitée. |
| **config_tarification_dynamique.json** | Fichier produit par l’interface (ou le script). Lu par m00 et par le pipeline évolution. |

L’interface ne modifie **aucun** des modules m00, m02b, m02c, m02d, m03b ; elle ne fait qu’écrire le fichier JSON.
