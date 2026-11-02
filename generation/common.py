# -*- coding: utf-8 -*-
"""Blocs réutilisés : tableaux de codes, voyants, caractéristiques, historiques, procédures."""
import os, json
from lib import *
from ref import EQUIP, CODES, HIST, TECHS, SITE

RESULTS = {}   # document_id -> dict(pages, anchors, meta)

def f(name): return os.path.join(FIG, name)

def record(doc_id, res, **meta):
    res.update(meta); RESULTS[doc_id] = res
    return res

def specs_table(eid, n):
    e = EQUIP[eid]
    return table([["Caractéristique", "Valeur"]] + list(e["specs"]), [0.38, 0.62],
                 anchor=f"tableau {n}", caption=f"Tableau {n} — Caractéristiques techniques {e['modele']}",
                 header_color=ACC[e["fabricant"]])

def voyants_table(eid, n):
    e = EQUIP[eid]
    return table([["Voyant", "État", "Signification"]] + list(e["voyants"]), [0.14, 0.14, 0.72],
                 anchor=f"tableau {n}", caption=f"Tableau {n} — Signification des voyants ({e['modele']})",
                 header_color=ACC[e["fabricant"]])

def codes_summary(eid, n):
    e = EQUIP[eid]
    rows = [["Code", "Libellé", "Voyant", "Niveau"]] + [[c[0], c[1], c[2], c[3]] for c in CODES[eid]]
    return table(rows, [0.08, 0.58, 0.18, 0.16], anchor=f"tableau {n}",
                 caption=f"Tableau {n} — Récapitulatif des codes d'alarme {e['modele']}", header_color=ACC[e["fabricant"]])

def codes_doc(eid, relpath, ref_, version, intro):
    e = EQUIP[eid]; mk = e["fabricant"]
    title = f"Table des codes d'alarme {e['modele']}"
    st = cover(mk, title, f"{e['nom']} — référence de diagnostic", ref_, version, eid,
               [["Contrôleur", e["controleur"]], ["Codes couverts", f"{CODES[eid][0][0]} à {CODES[eid][-1][0]}"]])
    st += [SP(4), P(intro), PB(), H1("1. Lecture des codes")]
    st += [P("Chaque alarme est identifiée par un code à trois caractères affiché sur l'écran du contrôleur et "
             "enregistré dans son journal. Le niveau indique la conséquence sur le fonctionnement :"),
           bullets(["<b>Information</b> : aucune conséquence, message de service.",
                    "<b>Préalarme</b> : l'équipement continue de fonctionner, une action est attendue avant que le seuil d'arrêt ne soit atteint.",
                    "<b>Alarme</b> : fonctionnement dégradé, intervention à planifier rapidement.",
                    "<b>Arrêt / Défaut / Critique</b> : l'équipement est arrêté ou la charge n'est plus protégée ; réarmement après diagnostic."]),
           SP(2)]
    st += note("Une alarme ne constitue pas un diagnostic. Les causes listées sont les plus probables ; "
               "toute intervention suit les procédures de sécurité et est réalisée par un technicien habilité.", "NOTE")
    st += [H1("2. Table détaillée")]
    rows = [["Code", "Libellé", "Voyant", "Niveau", "Causes probables", "Action recommandée"]] + [list(c) for c in CODES[eid]]
    st += table(rows, [0.065, 0.21, 0.1, 0.105, 0.23, 0.29], anchor="tableau 2.1",
                caption=f"Tableau 2.1 — Codes d'alarme {e['modele']}", header_color=ACC[mk], font=7.2)
    st += [H1("3. Réarmement"), P("Après suppression de la cause, appuyer sur RESET (ou acquitter depuis l'écran). "
            "Un code dont la cause persiste réapparaît immédiatement. Trois réarmements successifs sans succès "
            "imposent l'ouverture d'un ticket de maintenance.")]
    return record(os.path.splitext(os.path.basename(relpath))[0], build(relpath, mk, title, ref_, version, st))

def history_doc(eid, relpath, ref_, version):
    e = EQUIP[eid]
    title = f"Historique des interventions {eid}"
    st = cover("Exploitation", title, f"{e['nom']} — {SITE}", ref_, version, eid,
               [["Période", "janvier 2024 — octobre 2026"], ["Source", "Extraction de la GMAO de démonstration (fictive)"]])
    st += [SP(4), P("Extraction des interventions enregistrées sur l'équipement. Les essais mensuels conformes ne sont pas "
                    "tous reportés : seuls figurent les essais avec observation et un échantillon trimestriel. "
                    "Les noms des techniciens sont fictifs."), PB()]
    st += [H1("1. Synthèse")]
    rows = HIST[eid]
    ouverts = [r for r in rows if r[10].startswith("Ouvert")]
    st += table([["Indicateur", "Valeur"], ["Nombre d'interventions", str(len(rows))],
                 ["Correctives", str(sum(r[3] == "Correctif" for r in rows))],
                 ["Préventives", str(sum(r[3] == "Préventif" for r in rows))],
                 ["Tickets ouverts", ", ".join(r[0] for r in ouverts) or "aucun"]], [0.4, 0.6],
                anchor="tableau 1.1", caption="Tableau 1.1 — Synthèse")
    st += [H1("2. Journal des interventions")]
    data = [["N°", "Date", "Techn.", "Type", "Code", "Compteur", "Constat", "Actions / pièces", "Statut"]]
    for r in rows:
        data.append([r[0], r[1], TECHS[r[2]], r[3], r[4], r[5], r[6], r[7] + (f" — <i>{r[8]}</i>" if r[8] != "—" else ""), r[10]])
    st += table(data, [0.15, 0.095, 0.075, 0.09, 0.055, 0.07, 0.18, 0.195, 0.09], anchor="tableau 2.1",
                caption="Tableau 2.1 — Interventions", font=6.2)
    return record(os.path.splitext(os.path.basename(relpath))[0], build(relpath, "Exploitation", title, ref_, version, st))

def procedure_doc(relpath, maker, title, ref_, version, equip, objet, epi, outils, etapes, controles,
                  figures=(), avant=(), apres=(), supersede=None, extra_cover=None):
    st = cover(maker, title, "Procédure de maintenance", ref_, version, equip,
               [["Habilitation", "Technicien de maintenance habilité"]] + (extra_cover or []))
    if supersede: st += note(supersede, "NOTE")
    st += [H1("1. Objet et domaine"), P(objet)]
    st += [H1("2. Sécurité et équipements de protection")] + list(avant) + [bullets(epi)]
    st += [H2("Outillage et consommables"), bullets(outils)]
    for fg in figures: st += fg
    st += [H1("3. Mode opératoire")]
    for sec, items in etapes:
        if sec: st.append(H2(sec))
        st.append(bullets(items, numbered=True))
    st += list(apres)
    st += [H1("4. Contrôles et traçabilité"), bullets(controles)]
    doc_id = os.path.splitext(os.path.basename(relpath))[0]
    return record(doc_id, build(relpath, maker, title, ref_, version, st))
