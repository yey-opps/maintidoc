# -*- coding: utf-8 -*-
"""Famille 1 — groupes électrogènes (GE-A-01, GE-B-02)."""
from common import *
from ref import MODBUS_GE_A

D1 = "documents/famille_1/"
NE = "NORDAL Énergie"

# ===================================================================== manuels
def manuel_ge(eid, relpath, ref_, version, overview, panel, intro, install, exploitation, maint, depannage, pieces, revisions, panel_txt):
    e = EQUIP[eid]; s = e["seuils"]
    title = f"Manuel d'utilisation {e['modele']}"
    st = cover(NE, title, f"{e['nom']} {e['specs'][0][1].split(' /')[0]} — utilisation et maintenance de premier niveau",
               ref_, version, eid, [["Contrôleur", e["controleur"]], ["Site", SITE]])
    st += [SP(6), H2("Sommaire"), P("1. Consignes de sécurité · 2. Description · 3. Caractéristiques · 4. Installation · "
            "5. Panneau de commande et voyants · 6. Exploitation · 7. Maintenance préventive · 8. Codes d'alarme et seuils · "
            "9. Diagnostic · 10. Pièces de rechange · 11. Révisions"), PB()]
    # 1
    st += [H1("1. Consignes de sécurité")]
    st += note("Le groupe peut démarrer automatiquement à tout moment en mode AUTO (perte du réseau ou essai programmé). "
               "Placer le sélecteur sur ARRÊT et consigner le groupe avant toute intervention.", "DANGER")
    st += note("Ne jamais ouvrir le bouchon du radiateur moteur chaud : liquide sous pression à plus de 90 °C.", "DANGER")
    st += [bullets(["Intervention réservée au personnel formé et habilité (habilitation électrique adaptée).",
                    "Porter les EPI : chaussures de sécurité, gants, lunettes, protections auditives (niveau sonore > 85 dB(A) en marche).",
                    "Gaz d'échappement toxiques : ne jamais faire fonctionner le groupe dans un local non ventilé.",
                    "Gazole inflammable : interdiction de fumer et de toute flamme nue à moins de 5 m (voir fiche de sécurité gazole).",
                    "Batteries : risque de projection d'acide et de dégagement d'hydrogène lors de la charge.",
                    "Ne pas shunter les sécurités du contrôleur (arrêt d'urgence, sécurités moteur)."])]
    st += [PB()]
    # 2
    st += [H1("2. Description générale")] + [P(t) for t in intro]
    st += figure(f(overview), 160, f"Figure 2.1 — Vue d'ensemble du {e['modele']}", "fig 2.1")
    st += table([["Repère", "Élément"], ["1", "Radiateur et ventilateur de refroidissement"], ["2", "Moteur diesel et filtre à air"],
                 ["3", "Alternateur synchrone"], ["4", "Coffret contrôleur et disjoncteur de sortie"], ["5", "Réservoir journalier intégré au châssis"],
                 ["6", "Point de vidange huile moteur"], ["7", "Filtres à carburant"]], [0.15, 0.85],
                anchor="tableau 2.1", caption="Tableau 2.1 — Légende de la figure 2.1")
    st += [PB(), H1("3. Caractéristiques techniques")] + specs_table(eid, "3.1")
    st += [P("Les puissances sont données pour une température ambiante de 25 °C et une altitude inférieure à 1 000 m. "
             "Déclassement : 3 % par tranche de 5 °C au-delà de 40 °C.")]
    st += [H1("4. Installation et raccordement")] + [P(t) for t in install]
    st += [PB(), H1("5. Panneau de commande et voyants")]
    st += figure(f(panel), 150, f"Figure 5.1 — Panneau de commande {e['controleur'].split(' ')[0]}", "fig 5.1")
    st += voyants_table(eid, "5.1")
    st += [P(t) for t in panel_txt]
    st += [PB(), H1("6. Exploitation")]
    for h, items in exploitation:
        st += [H2(h), bullets(items, numbered=True)]
    st += [PB(), H1("7. Maintenance préventive")]
    st += [P("Les intervalles ci-dessous s'appliquent à un usage secours (moins de 500 h par an). Le premier terme atteint "
             "(heures ou durée) déclenche l'opération. Le contrôleur affiche le code de maintenance due lorsque le compteur "
             "programmé est atteint.")]
    st += table([["Opération", "Intervalle", "Référence"]] + maint, [0.5, 0.25, 0.25], anchor="tableau 7.1",
                caption="Tableau 7.1 — Plan de maintenance préventive", header_color=ACC[NE])
    st += [PB(), H1("8. Codes d'alarme et seuils")]
    st += [P(f"Le tableau 8.1 récapitule les codes ; la table détaillée (causes, actions) fait l'objet du document "
             f"« Table des codes d'alarme {e['modele']} ». Les seuils de protection usine sont donnés au tableau 8.2.")]
    st += codes_summary(eid, "8.1")
    st += table([["Grandeur", "Préalarme", "Arrêt"],
                 ["Température liquide de refroidissement", f"≥ {s['temp_prealarme']} °C", f"≥ {s['temp_arret']} °C"],
                 ["Pression d'huile", f"< {s['huile_prealarme']:.1f} bar".replace(".", ","), f"< {s['huile_arret']:.1f} bar".replace(".", ",")],
                 ["Vitesse", "—", f"> {s['survitesse']:,} tr/min".replace(",", " ")],
                 ["Tension batterie", f"< {s['batt_basse']:.1f} V".replace(".", ","), "—"],
                 ["Niveau carburant", f"< {s['carburant_bas']} %", "—"]], [0.5, 0.25, 0.25],
                anchor="tableau 8.2", caption="Tableau 8.2 — Seuils de protection (réglage usine)", header_color=ACC[NE])
    st += note("Les seuils sont des paramètres du contrôleur. Toute modification doit être tracée dans l'historique de l'équipement.", "ATTENTION")
    st += [PB(), H1("9. Diagnostic et dépannage")]
    st += table([["Symptôme", "Cause possible", "Action"]] + depannage, [0.28, 0.32, 0.40], anchor="tableau 9.1",
                caption="Tableau 9.1 — Aide au diagnostic", header_color=ACC[NE])
    st += [H1("10. Pièces de rechange et consommables")]
    st += table([["Référence", "Désignation", "Quantité"]] + pieces, [0.22, 0.58, 0.2], anchor="tableau 10.1",
                caption="Tableau 10.1 — Pièces de rechange", header_color=ACC[NE])
    st += [H1("11. Historique des révisions")]
    st += table([["Version", "Date", "Modification"]] + revisions, [0.15, 0.2, 0.65], anchor="tableau 11.1",
                caption="Tableau 11.1 — Révisions du document")
    doc_id = relpath.split("/")[-1][:-4]
    return record(doc_id, build(relpath, NE, title, ref_, version, st))


def manuel_ge_a():
    return manuel_ge("GE-A-01", D1 + "manuel_ge_a.pdf", "NE-GA250-MU-FR", "v2.1 (2025-02)", "ge_a_overview.png", "ge_a_panel.png",
        intro=["Le GA-250 est un groupe électrogène diesel de secours destiné à alimenter le tableau secouru (TGBT) du site en cas de "
               "perte du réseau public. Associé à un inverseur de source automatique (ATS), il démarre sur ordre du contrôleur, "
               "atteint sa tension nominale en moins de 10 secondes puis reprend la charge.",
               "Sur le site DC-01, le GE-A-01 secourt notamment l'onduleur UPS-A-01, qui assure seul l'alimentation des charges "
               "critiques pendant le démarrage du groupe."],
        install=["Le groupe est posé sur un massif béton avec plots antivibratoires. Prévoir un dégagement de 1 m sur les côtés "
                 "d'accès et une évacuation de l'air chaud du radiateur vers l'extérieur (section libre ≥ 1,5 m²).",
                 "Le raccordement puissance s'effectue sur le disjoncteur de sortie (400 A) vers la position « groupe » de l'inverseur "
                 "de source. Le contact sec d'ordre de démarrage provenant de l'ATS est câblé sur le bornier X2 (bornes 5-6). "
                 "Le schéma électrique simplifié (document NE-GA250-SE) détaille ces liaisons.",
                 "Avant la première mise en service : vérifier les niveaux (huile, liquide, carburant), le serrage des connexions et "
                 "la tension des batteries (≥ 25 V)."],
        exploitation=[("Démarrage manuel", ["Vérifier niveaux et absence de fuite.", "Placer le sélecteur sur MANU.",
                       "Appuyer sur MARCHE : le contrôleur lance jusqu'à 3 tentatives de démarrage de 10 s.",
                       "Attendre la stabilisation (voyant VERT, 400 V / 50 Hz) avant de prendre la charge."]),
                      ("Mode automatique", ["Placer le sélecteur sur AUTO : voyant VERT fixe = groupe prêt.",
                       "En cas de perte du réseau > 3 s, le groupe démarre et l'ATS bascule sur QG.",
                       "Au retour du réseau, temporisation de 5 min avant retransfert, puis refroidissement à vide de 3 min."]),
                      ("Arrêt", ["Délester la charge (ou laisser l'ATS retransférer).", "Laisser tourner à vide 3 min.",
                       "Placer le sélecteur sur ARRÊT. L'arrêt d'urgence est réservé aux situations dangereuses."])],
        maint=[["Contrôle visuel, niveaux, fuites", "Hebdomadaire", "—"], ["Essai en charge (75 %, 1 h)", "Mensuel", "Procédure d'essai en charge"],
               ["Vidange huile moteur + filtre à huile", "500 h ou 12 mois", "Procédure de vidange v2"],
               ["Remplacement filtres à carburant", "500 h ou 12 mois", "§10"], ["Inspection courroie", "250 h", "—"],
               ["Remplacement filtre à air", "1 000 h ou sur alarme A21", "§10"], ["Remplacement liquide de refroidissement", "2 ans", "—"],
               ["Contrôle batteries et chargeur", "Mensuel", "§9"]],
        depannage=[["Voyant ORANGE fixe", "Préalarme active (souvent A12)", "Lire le code sur l'écran ; consulter la table des codes"],
                   ["Le groupe ne démarre pas (A01)", "Batterie < 24 V, carburant, démarreur", "Contrôler tension batterie, niveau, purge"],
                   ["Fumée noire", "Surcharge, filtre à air colmaté", "Réduire la charge ; contrôler le filtre à air"],
                   ["Fumée blanche au démarrage", "Moteur froid, eau dans le gazole", "Purger le séparateur d'eau"],
                   ["Préalarme température en été", "Radiateur encrassé, ventilation du local", "Nettoyer le radiateur ; vérifier la ventilation"],
                   ["Tension instable", "Régulateur AVR, charge déséquilibrée", "Contrôler la répartition des charges"]],
        pieces=[["FH-250", "Filtre à huile", "1"], ["FC-250-P / FC-250-S", "Filtres à carburant primaire / secondaire", "1 + 1"],
                ["FA-250", "Cartouche filtre à air", "1"], ["CR-250", "Courroie de ventilateur", "1"], ["HM-15W40", "Huile moteur SAE 15W-40", "28 L"],
                ["BT-12-140", "Batterie 12 V 140 Ah", "2"]],
        revisions=[["v1.0", "2023-02", "Première édition"], ["v2.0", "2024-06", "Mise à jour du contrôleur CTRL-GA, codes A21 à A24"],
                   ["v2.1", "2025-02", "Intervalle de vidange porté à 500 h ou 12 mois (alignement sur la procédure v2)"]],
        panel_txt=["Le voyant ORANGE fixe signale une préalarme : le groupe continue de fonctionner, mais une action est attendue. "
                   "Dans la majorité des cas il s'agit de la préalarme de température du liquide de refroidissement (A12, seuil 95 °C).",
                   "Les valeurs mesurées et l'état du groupe sont également disponibles sur le port Modbus RTU du contrôleur "
                   "(table des registres : document NE-GA250-MB)."])


def manuel_ge_b():
    return manuel_ge("GE-B-02", D1 + "manuel_ge_b.pdf", "NE-GB500-MU-FR", "v1.4 (2024-09)", "ge_b_overview.png", "ge_b_panel.png",
        intro=["Le GB-500 est un groupe électrogène diesel de forte puissance dédié au secours des infrastructures du bâtiment "
               "(climatisation de production, onduleur modulaire UPS-B-02). Son réservoir journalier de 900 L est réalimenté "
               "automatiquement depuis une cuve externe de 5 000 L par une pompe de transfert.",
               "Un réchauffeur de liquide de refroidissement maintient le moteur à 40 °C environ à l'arrêt pour garantir une prise "
               "de charge rapide."],
        install=["Le groupe est installé dans un local dédié avec rétention. Le bac de rétention est équipé d'un détecteur de fuite (code B11).",
                 "La pompe de transfert est commandée par le contrôleur via le relais K7, sur information du flotteur du réservoir "
                 "journalier (voir schéma du circuit carburant NE-GB500-SC).",
                 "Le contrôleur CTRL-GB communique avec la supervision en Modbus TCP (port 502)."],
        exploitation=[("Démarrage", ["Vérifier niveaux, réchauffeur actif (liquide ≈ 40 °C).", "Sélectionner MANU puis START.",
                       "Attendre 400 V / 50 Hz et voyant VERT avant toute prise de charge."]),
                      ("Mode automatique", ["Sélectionner AUTO.", "Perte du réseau : démarrage et prise de charge en moins de 15 s.",
                       "Retour réseau : retransfert après 5 min, refroidissement 5 min."]),
                      ("Arrêt", ["Délester, laisser refroidir 5 min à vide.", "Sélectionner STOP."])],
        maint=[["Contrôle visuel, niveaux, bac de rétention", "Hebdomadaire", "—"], ["Essai en charge (75 %, 1 h)", "Mensuel", "Procédure d'essai en charge"],
               ["Vidange huile + 2 filtres", "500 h ou 12 mois", "§10"], ["Filtres à carburant et purge séparateur", "500 h ou 12 mois", "§10"],
               ["Contrôle batteries de démarrage (tension par batterie)", "Mensuel", "Procédure batteries"],
               ["Contrôle pompe de transfert et flotteur", "Trimestriel", "Schéma carburant"], ["Contrôle réchauffeur", "Trimestriel", "—"]],
        depannage=[["Voyant ORANGE fixe", "Défaut charge batterie (B07) ou chargeur (B08)", "Mesurer la tension de chaque batterie et la sortie du chargeur"],
                   ["Buzzer + message à l'écran", "Préalarme (B04, B06, B10…)", "Lire le code et consulter la table des codes"],
                   ["Niveau journalier qui baisse", "Pompe de transfert ou relais K7 (B18)", "Contrôler K7, le flotteur et la cuve externe"],
                   ["Démarrage lent par temps froid", "Réchauffeur hors service (B17)", "Contrôler la résistance 3 kW"],
                   ["Fuite détectée (B11)", "Raccord carburant ou huile", "Localiser, stopper, absorber ; ne pas redémarrer avant contrôle"]],
        pieces=[["FH-500", "Filtre à huile", "2"], ["FC-500", "Filtre à carburant / séparateur", "2"], ["FA-500", "Cartouche filtre à air", "2"],
                ["BT-12-180", "Batterie 12 V 180 Ah", "2"], ["CH-24-10", "Chargeur de batterie 24 V 10 A", "1"], ["K7-24", "Relais pompe de transfert 24 V", "1"]],
        revisions=[["v1.0", "2021-05", "Première édition"], ["v1.3", "2023-10", "Ajout du code B20 (Modbus TCP)"],
                   ["v1.4", "2024-09", "Précisions sur le voyant orange (B07/B08)"]],
        panel_txt=["Contrairement au GA-250, le voyant ORANGE du GB-500 est réservé aux défauts du circuit de charge des batteries "
                   "de démarrage (B07, B08). Les autres préalarmes (pression d'huile, température, carburant) sont signalées "
                   "uniquement par l'écran et le buzzer.",
                   "Un voyant ORANGE fixe doit donc conduire à mesurer la tension de chaque batterie (moteur arrêté) et la tension "
                   "de sortie du chargeur (27,6 V attendus)."])

# ====================================================================== schémas
def schema_electrique_ge_a():
    t = "Schéma électrique simplifié GA-250"
    st = [H1(t), P("Ce document regroupe trois vues simplifiées utiles au diagnostic. Il ne remplace pas les schémas "
                   "d'exécution du constructeur.")]
    st += figure(f("ge_a_unifilaire.png"), 165, "Figure 1 — Schéma unifilaire : réseau, groupe et inverseur de source", "fig 1")
    st += [P("En fonctionnement normal, QN est fermé et QG ouvert. Sur perte du réseau, l'ATS envoie l'ordre de démarrage au groupe ; "
             "une fois la tension stabilisée, QN s'ouvre puis QG se ferme (interverrouillage mécanique)."), PB()]
    st += figure(f("ge_a_charge.png"), 165, "Figure 2 — Circuit de charge et de démarrage 24 V", "fig 2")
    st += [P("Les deux batteries 12 V sont montées en série. Le chargeur d'entretien délivre 27,6 V ; la tension batterie est "
             "mesurée par le contrôleur et publiée dans le registre Modbus 40013 (résolution 0,1 V)."), PB()]
    st += figure(f("ge_a_capteurs.png"), 165, "Figure 3 — Chaîne de mesure et de signalisation", "fig 3")
    st += [P("Chaque capteur est lu par le contrôleur, qui compare les mesures aux seuils paramétrés et pilote les voyants, "
             "l'écran, la sortie Modbus et le relais d'arrêt moteur.")]
    return record("schema_electrique_ge_a", build(D1 + "schema_electrique_ge_a.pdf", NE, t, "NE-GA250-SE", "v1.0 (2024-11)", st))

def schema_carburant_ge_b():
    t = "Schéma du circuit carburant GB-500"
    st = [H1(t)]
    st += figure(f("ge_b_carburant1.png"), 165, "Figure 1 — Circuit carburant moteur", "fig 1")
    st += [P("Le préfiltre séparateur d'eau doit être purgé à chaque essai mensuel. Le retour d'excédent d'injection revient au "
             "réservoir journalier."), PB()]
    st += figure(f("ge_b_carburant2.png"), 165, "Figure 2 — Transfert depuis la cuve externe", "fig 2")
    st += [P("La pompe de transfert démarre au niveau bas du réservoir journalier et s'arrête au niveau haut. Une absence de "
             "remontée de niveau pendant 10 min déclenche le code B18.")]
    return record("schema_carburant_ge_b", build(D1 + "schema_carburant_ge_b.pdf", NE, t, "NE-GB500-SC", "v1.0 (2024-09)", st))

# =================================================================== procédures
EPI_GE = ["Chaussures de sécurité, gants de protection chimique, lunettes", "Protections auditives si le groupe voisin est en marche",
          "Groupe consigné (voir fiche de consignation)"]

def proc_demarrage_ge_a():
    return procedure_doc(D1 + "proc_demarrage_ge_a.pdf", NE, "Procédure de démarrage et d'arrêt GA-250", "NE-GA250-P01", "v1.3 (2025-02)", "GE-A-01",
        "Décrire le démarrage manuel, la remise en mode automatique et l'arrêt du groupe GE-A-01 en dehors des essais programmés.",
        ["Chaussures de sécurité, protections auditives", "Ne pas porter de vêtements flottants près des pièces en mouvement"],
        ["Aucun outillage spécifique", "Cahier de suivi du groupe"],
        [("Contrôles avant démarrage", ["Vérifier l'absence de fuite sous le groupe.", "Contrôler le niveau d'huile (entre MIN et MAX).",
           "Contrôler le niveau de liquide de refroidissement (vase d'expansion, moteur froid).", "Vérifier le niveau de carburant (> 50 % recommandé).",
           "Vérifier qu'aucun défaut n'est affiché (voyant ROUGE éteint)."]),
         ("Démarrage manuel", ["Placer le sélecteur sur MANU.", "Appuyer sur MARCHE.", "Attendre le voyant VERT et 400 V / 50 Hz à l'écran.",
           "Noter dans le cahier : heure, compteur horaire, tension, fréquence."]),
         ("Retour en mode automatique", ["Vérifier que le réseau est présent.", "Placer le sélecteur sur AUTO : le groupe s'arrête après 3 min de refroidissement.",
           "Vérifier le voyant VERT fixe (groupe prêt)."]),
         ("Arrêt", ["Délester la charge.", "Laisser tourner à vide 3 min.", "Placer le sélecteur sur ARRÊT."])],
        ["Aucun voyant ORANGE ou ROUGE après retour en AUTO", "Compteur horaire et observations reportés dans le cahier"])

def proc_vidange(v):
    v1 = v == 1
    fig = [figure(f("ge_a_vidange.png"), 130, "Figure 1 — Points de vidange (1 remplissage, 2 vidange, 3 filtre, 4 jauge)", "fig 1")]
    return procedure_doc(D1 + f"proc_vidange_ge_a_v{v}.pdf", NE, f"Procédure de vidange huile moteur GA-250 (v{v})",
        "NE-GA250-P04", "v1 (2023-04)" if v1 else "v2 (2025-01)", "GE-A-01",
        ("Remplacer l'huile moteur et le filtre à huile du GE-A-01. Périodicité : <b>toutes les 250 heures de fonctionnement ou "
         "tous les 6 mois</b>, au premier terme atteint.") if v1 else
        ("Remplacer l'huile moteur et le filtre à huile du GE-A-01 et prélever un échantillon pour analyse. Périodicité : "
         "<b>toutes les 500 heures de fonctionnement ou tous les 12 mois</b>, au premier terme atteint."),
        EPI_GE, ["Clé à douille 24 mm, clé à filtre", "Clé dynamométrique (40–60 N·m)", "Bac de récupération ≥ 35 L, absorbants",
                 "28 L d'huile SAE 15W-40 (API CI-4), filtre FH-250"] + ([] if v1 else ["Flacon de prélèvement pour analyse d'huile"]),
        [("Préparation", ["Faire tourner le groupe 10 min à vide pour fluidifier l'huile, puis l'arrêter.", "Consigner le groupe (sélecteur ARRÊT, coupe-batterie ouvert).",
           "Placer le bac sous le bouchon de vidange (repère 2)."]),
         ("Vidange", ["Retirer le bouchon de remplissage (repère 1) pour faciliter l'écoulement.", "Dévisser le bouchon de vidange et laisser s'écouler l'huile (≈ 15 min).",
           ] + ([] if v1 else ["Prélever 100 mL d'huile en milieu d'écoulement dans le flacon d'analyse."]) +
           [f"Remplacer le joint du bouchon et le revisser au couple de <b>{'45' if v1 else '50'} N·m</b>."]),
         ("Filtre", ["Déposer le filtre à huile (repère 3) avec la clé à filtre.", "Huiler le joint du filtre neuf et le serrer à la main de 3/4 de tour après contact."]),
         ("Remplissage", ["Remplir avec 26 L d'huile neuve, attendre 5 min.", "Compléter jusqu'au repère MAX de la jauge (repère 4) — capacité totale 28 L.",
           "Déconsigner, démarrer 5 min à vide, vérifier l'absence de fuite et de préalarme A04.", "Arrêter, attendre 10 min, contrôler à nouveau le niveau."])],
        ["Remise à zéro du compteur de maintenance (code A22)", "Déchets (huile, filtre) évacués en filière agréée",
         "Intervention enregistrée dans l'historique avec le compteur horaire"] + ([] if v1 else ["Échantillon envoyé au laboratoire, résultat joint à l'historique"]),
        figures=fig,
        supersede=None if v1 else "Cette version remplace la v1 du 2023-04. Modifications : intervalle porté de 250 h / 6 mois à 500 h / 12 mois ; "
                                  "couple du bouchon de vidange porté à 50 N·m ; ajout de l'analyse d'huile.")

def proc_essai_charge():
    rel = [["Grandeur", "Attendu", "Relevé"], ["Temps de démarrage", "< 10 s (GA-250) / < 15 s (GB-500)", ""], ["Tension L1-L2 / L2-L3 / L3-L1", "400 V ±2 %", ""],
           ["Fréquence", "50,0 Hz ±0,5", ""], ["Charge", "75 % de la puissance nominale", ""], ["Température liquide après 1 h", "< seuil de préalarme", ""],
           ["Pression d'huile", "> 3,0 bar", ""], ["Tension batterie avant démarrage", "> 25 V", ""], ["Fuites / vibrations", "Aucune", ""], ["Codes affichés", "Aucun", ""]]
    apres = [PB(), H1("Annexe — Fiche de relevés")] + table(rel, [0.38, 0.32, 0.30], anchor="tableau A.1",
             caption="Tableau A.1 — Relevés de l'essai en charge mensuel")
    return procedure_doc(D1 + "proc_essai_charge_ge.pdf", "Exploitation", "Procédure d'essai en charge mensuel", "EXP-GE-P02", "v1.1 (2025-03)",
        "GE-A-01 ; GE-B-02",
        "Vérifier chaque mois la capacité des groupes électrogènes à démarrer et à tenir 75 % de leur charge nominale pendant une heure, "
        "soit sur la charge réelle (essai avec transfert ATS), soit sur banc de charge résistif.",
        ["Protections auditives obligatoires", "Gants et lunettes pour le contrôle des niveaux", "Informer l'exploitation avant un essai avec transfert"],
        ["Banc de charge 300 kW (si essai hors charge réelle)", "Pince ampèremétrique", "Fiche de relevés (annexe)"],
        [("Préparation", ["Prévenir l'exploitation et le responsable de site.", "Contrôler niveaux et absence de fuite.", "Relever la tension batterie (> 25 V)."]),
         ("Essai", ["Lancer l'essai (TEST sur le GA-250, START puis prise de charge sur le GB-500).", "Chronométrer le temps de démarrage.",
           "Monter progressivement à 75 % de charge.", "Relever les grandeurs toutes les 15 min pendant 1 h.",
           "Surveiller les voyants : tout voyant ORANGE ou ROUGE est noté avec son code."]),
         ("Fin d'essai", ["Délester, laisser refroidir à vide (3 min GA-250, 5 min GB-500).", "Remettre en mode AUTO et vérifier le voyant VERT.",
           "Compléter la fiche de relevés et l'historique."])],
        ["Fiche de relevés signée et archivée", "Toute anomalie fait l'objet d'un ticket"], apres=apres)

def proc_batterie_ge_b():
    return procedure_doc(D1 + "proc_batterie_demarrage_ge_b.pdf", NE, "Remplacement des batteries de démarrage GB-500", "NE-GB500-P07", "v1.0 (2024-10)", "GE-B-02",
        "Remplacer les deux batteries 12 V 180 Ah du circuit de démarrage 24 V du GE-B-02, notamment après un défaut de charge "
        "batterie persistant (B07) avec chargeur conforme.",
        ["Gants isolants et lunettes (risque d'acide)", "Outils isolés 1 000 V", "Retirer montre, bagues et bracelets"],
        ["Clés isolées 13 mm", "Multimètre", "Graisse pour cosses", "2 batteries 12 V 180 Ah (réf. BT-12-180)"],
        [("Contrôle préalable", ["Mesurer la sortie du chargeur : 27,6 V attendus. Si nulle → code B08, remplacer le chargeur et non les batteries.",
           "Mesurer chaque batterie moteur arrêté après 12 h de charge : remplacement si < 12,2 V."]),
         ("Dépose", ["Placer le contrôleur sur STOP et ouvrir le coupe-batterie.", "Débrancher le câble de masse (–) en premier.",
           "Déposer le pont série, puis le câble (+).", "Déposer les batteries (32 kg chacune, à deux personnes)."]),
         ("Repose", ["Installer les batteries neuves, cosses propres et graissées.", "Raccorder le câble (+), puis le pont série, puis la masse (–) en dernier.",
           "Serrer les cosses au couple de 8 N·m.", "Fermer le coupe-batterie : tension attendue ≥ 25 V.", "Revenir en AUTO : le voyant ORANGE doit s'éteindre."])],
        ["Tension après remplacement notée dans l'historique", "Batteries usagées remises à un collecteur agréé"],
        figures=[figure(f("ge_b_batteries.png"), 140, "Figure 1 — Raccordement des batteries et ordre de dépose", "fig 1")])

# ================================================================ fiches sécurité
def fiche_gazole():
    t = "Fiche de sécurité — manipulation du gazole"
    st = [H1(t), P("Fiche interne de prévention rédigée pour les opérations de remplissage, de purge et de maintenance des "
                   "circuits carburant des groupes électrogènes. Elle ne se substitue pas à la fiche de données de sécurité du fournisseur.")]
    st += figure(f("picto_gazole.png"), 120, "Figure 1 — Pictogrammes applicables", "fig 1")
    st += table([["Danger", "Mesure de prévention"], ["Liquide et vapeurs inflammables", "Aucune flamme ni étincelle à moins de 5 m ; outillage antidéflagrant pour les cuves"],
                 ["Irritation cutanée", "Gants nitrile ; laver la peau à l'eau et au savon en cas de contact"],
                 ["Nocif par aspiration", "Ne jamais siphonner à la bouche ; en cas d'ingestion, ne pas faire vomir et appeler les secours"],
                 ["Toxique pour l'environnement aquatique", "Travailler au-dessus d'une rétention ; absorbants à proximité"]],
                [0.35, 0.65], anchor="tableau 1", caption="Tableau 1 — Dangers et prévention")
    st += [H2("Déversement accidentel"), bullets(["Arrêter la fuite si cela peut se faire sans risque.", "Contenir avec des absorbants, empêcher l'écoulement vers les réseaux.",
           "Collecter les absorbants souillés comme déchets dangereux.", "Signaler l'incident au responsable."])]
    st += [H2("Incendie"), bullets(["Extincteurs adaptés : poudre, mousse, CO2.", "Ne pas utiliser de jet d'eau direct.", "Évacuer et appeler les secours."])]
    return record("fiche_securite_gazole", build(D1 + "fiche_securite_gazole.pdf", "Exploitation", t, "EXP-SEC-01", "v1.0 (2024-06)", st))

def fiche_consignation_ge():
    t = "Consignation avant intervention sur groupe électrogène"
    st = [H1(t), P("La consignation garantit qu'un groupe ne peut pas démarrer, ni être remis sous tension, pendant une intervention. "
                   "Elle est obligatoire pour toute opération sur le moteur, l'alternateur ou le coffret.")]
    st += note("En mode AUTO, un groupe peut démarrer sans préavis sur perte du réseau ou essai programmé.", "DANGER")
    st += [H2("Responsabilités"), bullets(["Le chargé de consignation réalise et atteste la consignation.", "Le chargé de travaux vérifie la consignation avant de commencer.",
           "Chaque intervenant pose son propre cadenas."]), PB()]
    st += figure(f("consignation_ge.png"), 165, "Figure 1 — Étapes de consignation d'un groupe électrogène", "fig 1")
    st += [H2("Détail des étapes"), bullets(["Séparer : sélecteur sur ARRÊT, ouverture de QG (position groupe de l'inverseur de source).",
           "Condamner : cadenas sur le sélecteur et sur QG, étiquette « Ne pas manœuvrer — travaux en cours ».",
           "Isoler la batterie de démarrage avec le coupe-batterie (empêche tout démarrage).",
           "Vérifier l'absence de tension sur la sortie alternateur avec un VAT adapté.",
           "Baliser la zone d'intervention."], numbered=True)]
    st += [H2("Déconsignation"), P("Retrait des outils, fermeture des capots, retrait des cadenas par leurs propriétaires, remise en AUTO et "
                                  "contrôle du voyant VERT. La déconsignation est consignée dans le registre.")]
    return record("fiche_securite_consignation_ge", build(D1 + "fiche_securite_consignation_ge.pdf", "Exploitation", t, "EXP-SEC-02", "v1.2 (2025-01)", st))

# ================================================================ registres Modbus
def registres_modbus_ge_a():
    t = "Table partielle des registres Modbus CTRL-GA"
    st = [H1(t), P("Le contrôleur CTRL-GA expose ses mesures et états sur une liaison Modbus RTU (RS-485). Cette table décrit les "
                   "registres de maintien (holding registers) accessibles en lecture par la fonction 03.")]
    st += table([["Paramètre", "Valeur"], ["Liaison", "RS-485 deux fils, bornier X4"], ["Vitesse / format", "19 200 bauds, 8 bits, sans parité, 1 bit de stop (8N1)"],
                 ["Adresse esclave", "1 (par défaut)"], ["Fonction", "03 — lecture de registres de maintien"], ["Ordre des octets", "Big-endian (poids fort en premier)"]],
                [0.35, 0.65], anchor="tableau 1", caption="Tableau 1 — Paramètres de communication")
    st += [PB(), H1("Registres documentés")]
    st += table([["Registre", "Grandeur", "Unité", "Échelle / codage", "Type"]] + [list(r) for r in MODBUS_GE_A],
                [0.14, 0.38, 0.1, 0.26, 0.12], anchor="tableau 2", caption="Tableau 2 — Registres de maintien CTRL-GA (firmware v4.x)")
    st += note("Les registres 40110 à 40118 sont réservés au constructeur et ne sont pas documentés dans cette version de la table.", "NOTE")
    st += [H2("Exemple de lecture"), P("Requête : 01 03 00 0A 00 01 [CRC] — lecture du registre 40011 (offset 10). "
            "Réponse : 01 03 02 00 5D [CRC] → 0x005D = 93, soit une température de liquide de 93 °C."),
           H2("Codage du registre 40021"), P("Valeur 0 : aucune alarme. Valeur n (1 à 24) : alarme A(n) active, par exemple 12 = A12 "
            "(préalarme température liquide).")]
    return record("registres_modbus_ge_a", build(D1 + "registres_modbus_ge_a.pdf", NE, t, "NE-GA250-MB", "v0.9 (2024-12)", st))


def build_famille_1():
    manuel_ge_a(); manuel_ge_b()
    codes_doc("GE-A-01", D1 + "codes_alarme_ge_a.pdf", "NE-GA250-CA", "v2.1 (2025-02)",
              "Table de référence des codes d'alarme du contrôleur CTRL-GA équipant le groupe GA-250 (GE-A-01). "
              "Le voyant ORANGE fixe correspond aux préalarmes et alarmes non bloquantes ; le voyant ROUGE à un arrêt.")
    codes_doc("GE-B-02", D1 + "codes_alarme_ge_b.pdf", "NE-GB500-CA", "v1.4 (2024-09)",
              "Table de référence des codes d'alarme du contrôleur CTRL-GB équipant le groupe GB-500 (GE-B-02). "
              "Attention : sur ce modèle, le voyant ORANGE est réservé aux défauts de charge batterie (B07, B08).")
    schema_electrique_ge_a(); schema_carburant_ge_b(); proc_demarrage_ge_a()
    proc_vidange(1); proc_vidange(2); proc_essai_charge(); proc_batterie_ge_b()
    fiche_gazole(); fiche_consignation_ge()
    history_doc("GE-A-01", D1 + "historique_ge_a_01.pdf", "HIST-GE-A-01", "v1 (2026-10)")
    history_doc("GE-B-02", D1 + "historique_ge_b_02.pdf", "HIST-GE-B-02", "v1 (2026-10)")
    registres_modbus_ge_a()

if __name__ == "__main__":
    build_famille_1()
    for k, v in RESULTS.items(): print(f"{k:34s} {v['pages']:3d} p  {v['anchors'][:4]}")
