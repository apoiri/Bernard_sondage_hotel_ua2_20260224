# Validation des chiffres du rapport – Analyse du fichier sondage

Les valeurs du **RAPPORT_DETAILLE_VALIDATION_ANALYSES.md** et de la **synthèse professeur** (synthese_elements_apprentissage_prof.docx) ne sont pas une simple reprise de modèle : elles ont été **vérifiées sur le fichier sondage_hotel_data.csv** avec le script `verif_calculs_stats.py` et le module m10.

## Commande de vérification

```bash
python3 verif_calculs_stats.py
```

## Correspondance rapport ↔ fichier CSV (dernière vérification)

| Indicateur | Rapport / Synthèse | Sortie verif_calculs_stats.py (CSV actuel) |
|------------|--------------------|--------------------------------------------|
| % Annulées | 18,7 % | 18,74 % |
| % Rev_Spa > 0 | 52,3 % | 52,35 % |
| % Forfait Gastronomique | 42,1 % | 42,05 % |
| Khi² (Segment × Type_Forfait) | 2841,56 / 2842 | 2841,56 |
| Pearson r (Rev_Spa × NPS) | 0,45 (brut) | 0,448 |
| ANOVA F (Rev_Resto par Segment) | 10 362,84 / 10 363 | 10 362,84 |
| Régression : Rev_Chambre ; Rev_Resto ; Rev_Spa | 1,00 ; 1,08 ; 1,29 | 0,999 ; 1,083 ; 1,295 |
| R² | 0,9997 | 0,9997 |
| Taux annulation Direct | 6,8 % | 6,82 % |
| Taux annulation Intermédiaire | 30,5 % | 30,50 % |
| Externes avec Nuits > 0 | 15 | 15 |
| Annulee = Oui avec Nuits > 0 | 4 | 4 |
| NPS = 99 | 3 | 3 |
| Manquants Rev_Spa / Rev_Resto | 526 (5 %) | 526 |
| Doublons | 10 | 10 |

**Conclusion :** les chiffres du rapport et de la synthèse correspondent à l’analyse du fichier sondage_hotel_data.csv. Pour toute nouvelle version du CSV, relancer `verif_calculs_stats.py` et comparer au rapport si besoin.

**Note :** La section « Tarification active (Saison_calendrier) » et les montants Haute ~412 $ / Basse ~265 $ s’appliquent au CSV produit par le **pipeline évolution** (run_pipeline_evolution.py), qui ajoute les colonnes Saison_calendrier et Tarif_applique. Si le CSV a été généré par le pipeline classique, ces colonnes peuvent être absentes ; le reste des indicateurs reste valide.
