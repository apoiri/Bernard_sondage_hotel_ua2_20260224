# Saison vs tarification dynamique – Note pour vérification et pédagogie

Cette note répond au **diagnostic** d’une vérification indépendante de la tarification active et précise comment interpréter les colonnes **Saison** et **Saison_calendrier** dans le CSV.

---

## 1. Ce que la vérification indépendante a constaté

- **Tarification active (dynamique) : OUI** — elle est **très nette** quand on regarde le **mois du séjour** (Mois_sejour) : été (juin–août) nettement plus cher que hiver (déc–fév), +50 à 55 % selon les types de chambre.
- **Colonne Saison (Haute/Basse) :** elle **ne reflète pas** cette hausse. En comparant Tarif_applique selon Saison, Haute et Basse sont quasi identiques (non significatif). Donc, avec la seule variable **Saison**, on ne peut pas conclure à une tarification active.

**Raison technique :**  
- **Saison** vient du module 2 (segments) : elle est tirée selon le **profil client** (ex. Congressiste → plus souvent « Basse », Loisirs → plus souvent « Haute »), pas selon le **calendrier**.  
- **Tarif_applique** et **Rev_Chambre** sont calculés par le module de tarification dynamique à partir du **mois** (Mois_sejour) et des coefficients par mois, **sans utiliser** la colonne Saison.

D’où le décalage : **Saison** = saison « marketing » par segment ; **tarification dynamique** = pilotée par le **mois**.

---

## 2. Modifications apportées pour aligner analyse et pédagogie

### Nouvelle colonne : **Saison_calendrier**

Une colonne **Saison_calendrier** a été ajoutée au CSV, **dérivée du mois** (Mois_sejour), pour que les analyses « haute vs basse saison » soient **cohérentes avec la tarification** :

| Saison_calendrier | Mois (Mois_sejour) |
|-------------------|---------------------|
| **Haute**         | 6 (juin), 7 (juillet), 8 (août) |
| **Basse**         | 12 (décembre), 1 (janvier), 2 (février) |
| **Épaule**        | 3, 4, 5, 9, 10, 11 (mars–mai, sept.–nov.) |

Avec **Saison_calendrier** :
- Les comparaisons « Haute vs Basse » sur Tarif_applique (ou Rev_Chambre) montrent bien la **tarification active** (été plus cher que hiver).
- L’effet reste visible **par type de chambre** (environ +50–55 % en Haute vs Basse).

### Colonne **Saison** (inchangée)

La colonne **Saison** (Haute/Basse) est **conservée** telle quelle : elle reste basée sur le **segment client** et continue d’alimenter d’autres modules (ex. revenus centres de profit, forfait). Elle **ne doit pas** être utilisée pour analyser la tarification dynamique ; pour cela, utiliser **Saison_calendrier** ou **Mois_sejour**.

---

## 3. Recommandations pour les analyses et la formation

- **Pour analyser la tarification active (prix selon la période) :**  
  utiliser **Mois_sejour** ou **Saison_calendrier** (et non Saison). Exemples :  
  - Tarif_applique moyen par **Saison_calendrier** (Haute > Basse).  
  - Comparaison été (6–8) vs hiver (12–2) sur Tarif_applique ou Rev_Chambre.

- **Pour les exercices pédagogiques :**  
  - **Saison** : liaison avec le segment, comportement client, autres indicateurs (hors tarification dynamique).  
  - **Saison_calendrier** (ou Mois_sejour) : tarification dynamique, effet « haute vs basse » sur les prix et revenus chambre.

- **Pour Ottawa / Québec :**  
  Le codage retenu (Haute = 6–8, Basse = 12–2, Épaule = reste) peut être adapté dans le module **m02e_saison_calendrier.py** si vous fixez d’autres mois officiels pour haute/basse saison.

---

## 4. Résumé pour le client et les professeurs

| Élément | Conclusion |
|--------|------------|
| **Tarification active dans le fichier** | **Oui** — très nette via **Mois_sejour** (été vs hiver, +50–55 % par type de chambre). |
| **Colonne Saison (Haute/Basse)** | Reflète la **saison par segment**, pas le calendrier ; **ne pas** l’utiliser pour la tarification dynamique. |
| **Colonne Saison_calendrier** | Dérivée du **mois** ; **alignée** sur la logique de tarification ; à utiliser pour analyser « haute vs basse » sur les tarifs et revenus chambre. |

Les données sont **valides** pour démontrer la tarification active ; l’usage de **Saison_calendrier** (ou Mois_sejour) permet de le faire de façon claire et cohérente pour les étudiants et les vérifications indépendantes.
