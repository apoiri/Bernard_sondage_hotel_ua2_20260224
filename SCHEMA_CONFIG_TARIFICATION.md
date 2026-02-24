# Schéma – config_tarification_dynamique.json

Fichier lu par **m00_config_etendue.py**. Toutes les clés sont optionnelles (si absentes, seules les clés de m01 sont disponibles).

| Clé | Type | Description |
|-----|------|--------------|
| **types_chambre** | liste d’objets | Chaque objet : `nom` (string), `nb_chambres` (int), `prix_base` (number, $/nuit). |
| **taux_occupation_mois** | liste de 12 nombres | Taux d’occupation moyen par mois (janvier à décembre), entre 0 et 1. |
| **repartition_sexe** | objet | Clés M, F, Autre (ou autres) ; valeurs = proportion (somme 1). |
| **plages_revenus** | liste d’objets | Chaque objet : `libelle`, `min`, `max` (revenus annuels). |
| **pays** | liste d’objets | Chaque objet : `code`, `nom`, `poids` (proportion). |
| **provinces_par_pays** | objet | Clé = code pays ; valeur = liste d’objets `code`, `nom`, `poids`. |
| **villes_exemples** | objet | Clé = code province ; valeur = liste de noms de villes (exemples pour tirage). |

Fichier d’exemple : **config_tarification_dynamique_exemple.json**.
