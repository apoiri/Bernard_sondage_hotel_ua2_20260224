# -*- coding: utf-8 -*-
"""
Module 11 – Synthèse Word à l'intention du professeur
Simulation « L'Hôtel Boutique Art de Vivre »
Génère un document Word listant tous les éléments d'apprentissage que les étudiants
peuvent réaliser avec le fichier sondage_hotel_data.csv, pour que le professeur
puisse couvrir toutes les activités pédagogiques.
"""

from pathlib import Path

# ========== HYPOTHÈSES DU SCRIPT (modifiables par l'opérateur) ==========
FICHIER_WORD_SORTIE = "synthese_elements_apprentissage_prof.docx"
REPERTOIRE = None   # None = même dossier que ce script
FICHIER_CSV_REFERENCE = "sondage_hotel_data.csv"

# ========== NE PAS MODIFIER CI-DESSOUS (logique du script) ==========

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
except ImportError:
    raise ImportError("Module python-docx requis. Installer avec : pip install python-docx")


def _repertoire():
    return Path(REPERTOIRE) if REPERTOIRE else Path(__file__).resolve().parent


def _add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    return p


def _add_para(doc, text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    if bold:
        run.bold = True
    return p


def run():
    """Génère le document Word de synthèse pour le professeur."""
    doc = Document()
    rep = _repertoire()
    chemin_sortie = rep / FICHIER_WORD_SORTIE

    # ---- Titre ----
    _add_heading(doc, "Synthèse – Éléments d'apprentissage", level=0)
    _add_para(doc, "Document à l'intention du professeur – Simulation « L'Hôtel Boutique Art de Vivre »", bold=True)
    _add_para(doc, "Ce document recense tous les éléments d'apprentissage que les étudiants peuvent réaliser avec le fichier de données généré, afin d'assurer la couverture complète des objectifs pédagogiques en analyse de sondage et prise de décision.")
    doc.add_paragraph()

    # ---- 1. Présentation du jeu de données ----
    _add_heading(doc, "1. Présentation du jeu de données", level=1)
    _add_para(doc, f"Fichier de travail : {FICHIER_CSV_REFERENCE}")
    _add_para(doc, "Contenu : Réservations simulées sur une année complète pour un hôtel de 100 chambres (taux d'occupation moyen 72 %). Le fichier contient environ 10 500 lignes (réservations) plus des lignes dupliquées volontaires pour l'exercice de nettoyage.")
    _add_para(doc, "Variables principales :")
    variables = [
        ("ID_Client", "Identifiant unique (ex. AB-00001)"),
        ("Segment", "Persona : Affaires_Solo, Congressiste, Loisirs_Couple, Local_Gourmet, Local_Spa"),
        ("Type_Client", "Interne (séjourne) / Externe (ne séjourne pas)"),
        ("Saison", "Haute / Basse"),
        ("Canal_reservation", "Source : Site Web, Courriel, Téléphone, Booking.com, Expedia, etc."),
        ("Type_canal", "Direct / Intermediaire"),
        ("Annulee", "Oui / Non (taux annulation ~18 %, plus élevé via intermédiaires)"),
        ("Nuits", "Nombre de nuits (0 si Externe ou annulé)"),
        ("Rev_Chambre", "Revenus chambre ($)"),
        ("Rev_Banquet", "Revenus banquet ($)"),
        ("Rev_Resto", "Revenus restaurant ($)"),
        ("Rev_Spa", "Revenus spa ($)"),
        ("Type_Forfait", "Forfait Gastronomique / Chambre Seule"),
        ("Satisfaction_NPS", "Score NPS 0–10 (NaN si annulé)"),
        ("Total_Facture", "Montant total ($)"),
    ]
    for nom, desc in variables:
        _add_para(doc, f"  • {nom} : {desc}")
    doc.add_paragraph()

    # ---- 2. Éléments d'apprentissage (tableau) ----
    _add_heading(doc, "2. Éléments d'apprentissage à réaliser avec le fichier", level=1)
    _add_para(doc, "Le tableau ci-dessous liste chaque technique ou objectif pédagogique, les variables à utiliser et le type de sortie attendu. Le professeur peut s'en servir pour construire les exercices ou vérifier que tous les éléments sont couverts.")
    doc.add_paragraph()

    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text = "Élément d'apprentissage"
    hdr[1].text = "Variables utilisées"
    hdr[2].text = "Objectif / Sortie attendue"
    hdr[3].text = "Coché"
    for cell in hdr:
        cell.paragraphs[0].runs[0].bold = True

    lignes = [
        ("Statistiques descriptives", "Toutes (effectifs, moyennes, écarts-types, min/max)", "Tableaux de synthèse par segment, Type_Client, Saison, Annulee ; description des variables numériques (Nuits, Rev_*, Total_Facture, Satisfaction_NPS).", "☐"),
        ("Proportions et intervalles de confiance", "Annulee ; Rev_Spa ; Type_Forfait", "Estimer une proportion en population (ex. % annulées, % utilisant le spa, % Forfait Gastronomique) et calculer l'IC 95 %.", "☐"),
        ("Test du Khi-deux (indépendance)", "Segment × Type_Forfait", "Vérifier la liaison entre segment et type de forfait (Loisirs → Forfait Gastronomique, Congressiste → Chambre Seule) ; khi², ddl, p-value.", "☐"),
        ("Corrélation de Pearson", "Rev_Spa, Satisfaction_NPS (lignes non annulées)", "Mesurer la liaison linéaire entre dépense spa et satisfaction ; r, p-value. Attendu : corrélation positive (données conçues pour r ≈ 0,75 avant anomalies).", "☐"),
        ("Comparaison de moyennes (ANOVA)", "Rev_Resto par Segment", "Comparer les dépenses restaurant entre segments ; F, p-value. Attendu : différences significatives entre segments (p < 0,05).", "☐"),
        ("Régression linéaire multiple", "Total_Facture ~ Rev_Chambre + Rev_Resto + Rev_Spa", "Prédire la facture totale à partir des revenus par poste ; coefficients, R², interprétation. Attendu : coefficients proches de 1 ; 1,1 ; 1,3.", "☐"),
        ("Annulations par canal", "Type_canal, Annulee ; Canal_reservation", "Comparer les taux d'annulation Direct vs Intermédiaire ; tableaux et graphiques. Attendu : ~7 % direct, ~29 % intermédiaire.", "☐"),
        ("Nettoyage des données (data cleaning)", "Type_Client & Nuits ; Satisfaction_NPS ; Rev_Spa, Rev_Resto ; doublons", "Détecter et traiter : Externes avec Nuits > 0 (incohérence) ; valeurs aberrantes (ex. NPS = 99) ; valeurs manquantes (Rev_Spa, Rev_Resto) ; lignes dupliquées.", "☐"),
        ("Prise de décision / recommandations", "Segments, revenus, satisfaction, canal", "Synthétiser les résultats pour formuler des recommandations (ex. cibler les canaux à faible annulation, segments à forte dépense spa, etc.).", "☐"),
    ]
    for elem, vars_, objectif, coche in lignes:
        row = table.add_row()
        row.cells[0].text = elem
        row.cells[1].text = vars_
        row.cells[2].text = objectif
        row.cells[3].text = coche
    doc.add_paragraph()

    # ---- 3. Anomalies pédagogiques ----
    _add_heading(doc, "3. Anomalies pédagogiques (pour l'exercice de nettoyage)", level=1)
    _add_para(doc, "Le fichier contient volontairement les anomalies suivantes, à faire détecter et corriger par les étudiants :")
    anomalies = [
        "Incohérence logique : des clients « Externes » ont Nuits > 0 (une quinzaine de lignes).",
        "Outliers : quelques lignes avec Satisfaction_NPS = 99 (erreur de saisie simulée).",
        "Valeurs manquantes : environ 5 % de cellules vides dans Rev_Spa et Rev_Resto.",
        "Doublons : une dizaine de lignes sont dupliquées (à identifier et supprimer ou fusionner).",
    ]
    for a in anomalies:
        _add_para(doc, f"  • {a}")
    _add_para(doc, "Après nettoyage, les analyses (proportions, régression, Pearson, etc.) peuvent être refaites pour comparer les résultats avec/sans anomalies.")
    doc.add_paragraph()

    # ---- 4. Checklist professeur ----
    _add_heading(doc, "4. Checklist – Éléments traités en cours / TD", level=1)
    _add_para(doc, "Le professeur peut cocher (manuellement dans ce document) les éléments d'apprentissage déjà traités avec les étudiants, afin de s'assurer que tous les objectifs du fichier sont couverts.")
    _add_para(doc, "Les lignes du tableau de la section 2 contiennent une colonne « Coché » à cocher au fur et à mesure.")
    doc.add_paragraph()
    _add_para(doc, "— Fin du document —", bold=True)

    doc.save(chemin_sortie)
    return chemin_sortie


if __name__ == "__main__":
    print("=" * 60)
    print("HYPOTHÈSES MODULE 11 (Synthèse Word professeur)")
    print("=" * 60)
    print(f"  Fichier Word sortie = {FICHIER_WORD_SORTIE}")
    print("=" * 60)
    chemin = run()
    print(f"Document Word enregistré : {chemin}")

# ========== RÈGLE DE BLOCAGE ==========
# Aucune modification de ce module n'est acceptée sans l'autorisation du maître d'ouvrage du projet.
