# -*- coding: utf-8 -*-
"""Figures (schémas, panneaux, pictogrammes) et photos synthétiques du corpus."""
import os, math, random
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from lib import FIG, CORPUS

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
INK = "#1d2733"; GRID = "#9aa3ad"
LED = {"vert": "#2fbf4a", "orange": "#ff8c1a", "rouge": "#e0261b", "jaune": "#f2d21b", "off": "#5d636b"}

def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w * 10); ax.set_ylim(0, h * 10); ax.axis("off"); ax.set_aspect("equal")
    return fig, ax

def save(fig, name):
    p = os.path.join(FIG, name); fig.savefig(p, bbox_inches="tight", pad_inches=0.08, facecolor="white"); plt.close(fig)
    return p

def box(ax, x, y, w, h, txt="", fc="#f4f6f8", ec=INK, fs=8, lw=1.2, r=0.6, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if txt: ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=fs, color=INK,
                    fontweight="bold" if bold else "normal", wrap=True)

def arrow(ax, x1, y1, x2, y2, txt="", col=INK, lw=1.4, style="-|>", fs=7, dash=False):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=10, color=col, lw=lw,
                                 linestyle="--" if dash else "-"))
    if txt: ax.text((x1+x2)/2, (y1+y2)/2 + 0.8, txt, ha="center", va="bottom", fontsize=fs, color=col)

def line(ax, pts, col=INK, lw=1.4, dash=False):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=col, lw=lw, ls="--" if dash else "-")

def led(ax, x, y, col, label, on=True, r=1.1):
    ax.add_patch(Circle((x, y), r + 0.35, fc="#2b2f35", ec="#111"))
    ax.add_patch(Circle((x, y), r, fc=LED[col] if on else LED["off"], ec="#111", lw=0.6))
    if on: ax.add_patch(Circle((x - r*0.3, y + r*0.3), r*0.28, fc="white", alpha=0.55, ec="none"))
    ax.text(x, y - r - 1.4, label, ha="center", va="top", fontsize=6.5, color="white")

def callout(ax, x, y, n, tx, ty):
    ax.plot([x, tx], [y, ty], color=INK, lw=0.8)
    ax.add_patch(Circle((tx, ty), 1.3, fc="white", ec=INK, lw=0.9))
    ax.text(tx, ty, str(n), ha="center", va="center", fontsize=7, fontweight="bold")

def switch(ax, x, y, label, closed=True, vertical=False):
    ax.add_patch(Circle((x, y), 0.35, fc=INK));
    if vertical:
        ax.add_patch(Circle((x, y - 3), 0.35, fc=INK))
        if closed: line(ax, [(x, y), (x, y - 3)])
        else: line(ax, [(x, y), (x + 1.6, y - 2.4)])
        ax.text(x + 1.2, y - 1.5, label, fontsize=7, va="center", fontweight="bold")
    else:
        ax.add_patch(Circle((x + 3, y), 0.35, fc=INK))
        if closed: line(ax, [(x, y), (x + 3, y)])
        else: line(ax, [(x, y), (x + 2.6, y + 1.5)])
        ax.text(x + 1.5, y + 1.0, label, fontsize=7, ha="center", fontweight="bold")

# ======================================================== panneaux de commande
def panel_ge_a(lcd=("A12 PRÉALARME", "TEMP. LIQ. 96 °C", "MODE AUTO  1 250 h"), leds=("vert", "orange")):
    fig, ax = canvas(9, 6)
    box(ax, 1, 1, 88, 58, fc="#3a414a", ec="#15181c", r=2, lw=2)
    ax.text(5, 54, "NORDAL  CTRL-GA", color="white", fontsize=10, fontweight="bold")
    box(ax, 6, 30, 44, 19, fc="#9fc5a8", ec="#15181c", r=0.8, lw=1.5)
    for i, t in enumerate(lcd):
        ax.text(9, 45 - i * 5.5, t, fontsize=9.5, family="DejaVu Sans Mono", color="#102015")
    led(ax, 62, 45, "vert", "MARCHE / PRÊT", "vert" in leds)
    led(ax, 72, 45, "orange", "PRÉALARME", "orange" in leds)
    led(ax, 82, 45, "rouge", "ARRÊT DÉFAUT", "rouge" in leds)
    for i, b in enumerate(["ARRÊT", "MANU", "AUTO", "TEST", "RESET"]):
        box(ax, 6 + i * 10, 14, 8, 8, b, fc="#d8dde3", fs=6.5, r=0.8)
    ax.add_patch(Circle((78, 20), 7.5, fc="#f2d21b", ec="#15181c", lw=1.2))
    ax.add_patch(Circle((78, 20), 5, fc="#d2231a", ec="#15181c", lw=1.2))
    ax.text(78, 9.5, "ARRÊT D'URGENCE", ha="center", fontsize=6.5, color="white")
    ax.text(62, 34, "Port Modbus RTU", fontsize=6.5, color="#c9ced4")
    return fig, ax

def panel_ge_b(lcd=("GB-500   AUTO   PRÊT", "U 401 V   F 50,0 Hz", "BATT 23,4 V", "B07 DÉFAUT CHARGE BATT"), leds=("vert", "orange")):
    fig, ax = canvas(9, 6)
    box(ax, 1, 1, 88, 58, fc="#2f3b47", ec="#121518", r=2, lw=2)
    ax.text(5, 54, "NORDAL  CTRL-GB", color="white", fontsize=10, fontweight="bold")
    box(ax, 6, 26, 52, 23, fc="#7fb3d5", ec="#121518", r=0.8, lw=1.5)
    for i, t in enumerate(lcd):
        ax.text(8.5, 45 - i * 5, t, fontsize=8.5, family="DejaVu Sans Mono", color="#0a1a26")
    ys = [45, 36, 27]
    for (c, lab), y in zip([("vert", "MARCHE"), ("orange", "CHARGE BATT."), ("rouge", "DÉFAUT")], ys):
        led(ax, 70, y, c, lab, c in leds)
    for i, b in enumerate(["◀", "▶", "OK", "ESC"]):
        box(ax, 6 + i * 9, 12, 7, 7, b, fc="#cfd5db", fs=7, r=0.8)
    for i, b in enumerate(["STOP", "MANU", "AUTO", "START"]):
        box(ax, 44 + i * 9, 12, 8, 7, b, fc="#cfd5db", fs=6, r=0.8)
    ax.add_patch(Circle((82, 47), 2.2, fc="#111", ec="#555")); ax.text(82, 42.5, "BUZZER", ha="center", fontsize=5.5, color="white")
    return fig, ax

def panel_ups_a(state="orange"):
    fig, ax = canvas(9, 5)
    box(ax, 1, 1, 88, 48, fc="#e9ebee", ec="#2a2f36", r=2, lw=2)
    ax.text(5, 43.5, "VOLTARIS  VA-20", color="#22408c", fontsize=10, fontweight="bold")
    box(ax, 5, 18, 40, 20, fc="#20262d", ec="#111", r=0.8)
    lines = {"orange": ["SUR BATTERIE  (U08)", "AUTONOMIE 18 min", "CHARGE 46 %"],
             "vert": ["ONLINE - NORMAL", "CHARGE 46 %", "BATT 100 %"]}[state]
    for i, t in enumerate(lines):
        ax.text(7.5, 33 - i * 5.5, t, fontsize=8.5, family="DejaVu Sans Mono", color="#7cf09b")
    labels = [("vert", "NORMAL"), ("orange", "BATTERIE"), ("orange", "BATT. FAIBLE"), ("jaune", "BYPASS"), ("rouge", "DÉFAUT")]
    ax.add_patch(Rectangle((50, 16), 37, 24, fc="#2a2f36"))
    on = {"orange": [1], "vert": [0]}[state]
    for i, (c, lab) in enumerate(labels):
        led(ax, 54 + i * 7.3, 31, c, lab, i in on, r=1.0)
    for i, b in enumerate(["ON", "OFF", "▲", "▼", "ENTER"]):
        box(ax, 5 + i * 9, 6, 7, 7, b, fc="#cfd5db", fs=6.5, r=0.8)
    return fig, ax

def front_ups_b(code="M17", txt=("ALARME ACTIVE", "M17 TEMP. ARMOIRE BAT.", "37,5 °C  (seuil 35 °C)")):
    fig, ax = canvas(7, 9)
    box(ax, 4, 2, 62, 86, fc="#dfe3e8", ec="#22282f", r=1.5, lw=2)
    ax.text(8, 83, "VOLTARIS  VB-60M", color="#22408c", fontsize=10, fontweight="bold")
    box(ax, 10, 64, 34, 15, fc="#1b2229", ec="#111", r=0.6)
    for i, t in enumerate(txt):
        ax.text(12, 75 - i * 4.4, t, fontsize=7.2, family="DejaVu Sans Mono", color="#ffb35c" if i else "#ffffff")
    ax.add_patch(Rectangle((48, 64), 14, 15, fc="#2a2f36"))
    for i, (c, lab) in enumerate([("vert", "NORMAL"), ("orange", "ALARME"), ("rouge", "CRITIQUE")]):
        led(ax, 55, 76 - i * 5, c, "", c in ("vert", "orange"), r=0.9)
        ax.text(59, 76 - i * 5, lab, fontsize=5, color="white", va="center")
    for k in range(3):
        y = 44 - k * 16
        box(ax, 10, y, 50, 13, "", fc="#c3c9d0", ec="#22282f", r=0.6)
        ax.text(13, y + 9, f"MODULE {k+1}  VB-PM20", fontsize=7, fontweight="bold")
        led(ax, 54, y + 6.5, "vert", "", True, r=0.8)
        for j in range(6): ax.add_patch(Rectangle((14 + j * 5.5, y + 2), 4, 4, fc="#8c939b"))
    ax.text(35, 5, "Emplacement module 4 (N+1) : obturateur", ha="center", fontsize=6.5)
    return fig, ax

# ============================================================ schémas
def overview_ge(model, tank, kva):
    fig, ax = canvas(10, 5)
    box(ax, 2, 6, 96, 4, fc="#b6bcc3")                 # châssis
    box(ax, 4, 10, 14, 30, "Radiateur", fc="#d7e6f2")
    box(ax, 20, 10, 36, 28, "Moteur diesel", fc="#e8e2d6")
    box(ax, 58, 12, 24, 24, "Alternateur", fc="#dfe9df")
    box(ax, 84, 14, 12, 26, "Coffret\ncontrôleur", fc="#e4e4ef", fs=7)
    box(ax, 22, 0.5, 60, 5.2, f"Réservoir journalier ({tank})", fc="#f1e6c9", fs=7)
    box(ax, 30, 38, 10, 5, "Filtre air", fc="#f4f6f8", fs=6.5)
    box(ax, 44, 40, 10, 6, "Échappement", fc="#f4f6f8", fs=6)
    for n, (x, y, tx, ty) in enumerate([(10, 38, 8, 46), (40, 36, 36, 47), (70, 36, 72, 45), (90, 38, 93, 46),
                                        (52, 4, 60, -3), (28, 16, 20, -3), (48, 16, 44, -3)], 1):
        callout(ax, x, y, n, tx, ty)
    ax.text(50, 49, f"{model} — vue latérale côté accès ({kva})", ha="center", fontsize=9, fontweight="bold")
    return fig

def unifilaire_ge_a():
    fig, ax = canvas(10, 7)
    box(ax, 4, 56, 22, 8, "Réseau public\n400 V 50 Hz", fc="#e6eef7")
    box(ax, 70, 56, 24, 8, "Alternateur GE-A-01\n250 kVA", fc="#dfe9df")
    box(ax, 34, 36, 32, 10, "Inverseur de source (ATS)\nQN réseau / QG groupe", fc="#fff3d6")
    line(ax, [(15, 56), (15, 50), (40, 50), (40, 46)]); line(ax, [(82, 56), (82, 50), (60, 50), (60, 46)])
    switch(ax, 40, 53.5, "QN", True, vertical=True); switch(ax, 60, 53.5, "QG", False, vertical=True)
    line(ax, [(50, 36), (50, 30)])
    box(ax, 30, 22, 40, 8, "TGBT secouru — salle E1", fc="#eef1f4")
    for x, t in [(36, "UPS-A-01\n(20 kVA)"), (50, "Climatisation\nlocal batteries"), (64, "Éclairage\nsécurité")]:
        line(ax, [(x, 22), (x, 15)]); box(ax, x - 6.5, 6, 13, 9, t, fs=6.5, fc="#f4f6f8")
    arrow(ax, 72, 40, 66, 40, "ordre démarrage\n(contact sec)", dash=True, fs=6)
    line(ax, [(72, 40), (88, 40), (88, 56)], dash=True)
    ax.text(50, 68, "Schéma unifilaire simplifié — alimentation secourue", ha="center", fontweight="bold")
    ax.text(4, 2, "QN fermé / QG ouvert : position normale (réseau présent). Interverrouillage mécanique QN/QG.", fontsize=7)
    return fig

def charge_batt_ge_a():
    fig, ax = canvas(10, 6)
    box(ax, 4, 30, 18, 12, "Chargeur\n27,6 V / 6 A", fc="#eef1f4")
    box(ax, 34, 30, 14, 12, "Batterie 1\n12 V 140 Ah", fc="#f1e6c9")
    box(ax, 54, 30, 14, 12, "Batterie 2\n12 V 140 Ah", fc="#f1e6c9")
    box(ax, 78, 30, 18, 12, "Démarreur\n24 V 7 kW", fc="#e8e2d6")
    line(ax, [(48, 36), (54, 36)]); ax.text(51, 38, "série", ha="center", fontsize=6.5)
    line(ax, [(22, 39), (34, 39)]); line(ax, [(68, 39), (78, 39)])
    box(ax, 4, 8, 18, 10, "Fusible F3\n10 A", fc="#fde8e6", fs=7)
    line(ax, [(13, 30), (13, 18)])
    box(ax, 40, 8, 24, 10, "Contrôleur CTRL-GA\nmesure U batt. (40013)", fc="#e4e4ef", fs=7)
    line(ax, [(61, 30), (61, 18)], dash=True)
    box(ax, 78, 8, 18, 10, "Relais démarreur K2", fc="#f4f6f8", fs=7)
    line(ax, [(87, 18), (87, 30)])
    ax.text(50, 50, "Circuit de charge et de démarrage 24 V — GE-A-01", ha="center", fontweight="bold")
    ax.text(4, 2, "Seuil A16 : 23,0 V. Tension de charge d'entretien nominale : 27,6 V.", fontsize=7)
    return fig

def capteurs_ge_a():
    fig, ax = canvas(10, 7)
    sens = [("Sonde température liquide (CTN)", "40011"), ("Capteur pression huile", "40012"),
            ("Capteur vitesse (pick-up magnétique)", "40010"), ("Jauge niveau carburant", "40014"),
            ("Pressostat filtre à air", "—"), ("Mesures U/I/F alternateur", "40001-40009")]
    for i, (s, r) in enumerate(sens):
        y = 60 - i * 9.5
        box(ax, 2, y, 30, 7, s, fs=6.5, fc="#f4f6f8")
        arrow(ax, 32, y + 3.5, 42, 36)
        ax.text(33, y + 5.6, r, fontsize=5.8, color="#22408c")
    box(ax, 42, 24, 22, 24, "Contrôleur\nCTRL-GA\n\nlogique d'alarme\n+ seuils\nparamétrables", fc="#e4e4ef", fs=7)
    outs = [("Voyants vert / orange / rouge", "#fff3d6"), ("Écran LCD (codes Axx)", "#eef1f4"),
            ("Port Modbus RTU → supervision", "#e6eef7"), ("Relais d'arrêt moteur", "#fde8e6")]
    for i, (o, c) in enumerate(outs):
        y = 52 - i * 10
        arrow(ax, 64, 36, 72, y + 3.5); box(ax, 72, y, 26, 7, o, fs=6.5, fc=c)
    ax.text(50, 70, "Chaîne de mesure et de signalisation — GE-A-01", ha="center", fontweight="bold")
    ax.text(2, 1, "Les seuils sont des paramètres du contrôleur (cf. manuel §5 et §8).", fontsize=7)
    return fig

def carburant_ge_b(page=1):
    fig, ax = canvas(10, 6)
    if page == 1:
        box(ax, 2, 24, 18, 18, "Réservoir\njournalier\n900 L", fc="#f1e6c9")
        chain = [("Préfiltre +\nséparateur d'eau", 26), ("Pompe\nd'alimentation", 44), ("Filtre\nsecondaire 5 µm", 62), ("Rampe\nd'injection", 80)]
        prev = 20
        for t, x in chain:
            arrow(ax, prev, 33, x, 33); box(ax, x, 27, 14, 12, t, fs=6.5, fc="#f4f6f8"); prev = x + 14
        line(ax, [(87, 27), (87, 14), (11, 14)], dash=True); arrow(ax, 11, 14, 11, 24, dash=True)
        ax.text(48, 10.5, "Retour carburant (excédent d'injection)", ha="center", fontsize=7)
        ax.text(26, 22, "Purge eau", fontsize=6.5); ax.text(50, 50, "Circuit carburant moteur — GE-B-02", ha="center", fontweight="bold")
    else:
        box(ax, 2, 18, 22, 22, "Cuve externe\n5 000 L\n(double paroi)", fc="#f1e6c9")
        box(ax, 34, 24, 16, 10, "Pompe de\ntransfert", fc="#f4f6f8", fs=7)
        box(ax, 62, 18, 20, 22, "Réservoir\njournalier\n900 L", fc="#f1e6c9")
        arrow(ax, 24, 29, 34, 29); arrow(ax, 50, 29, 62, 29)
        box(ax, 84, 30, 14, 8, "Flotteur\nhaut / bas", fs=6.5, fc="#eef1f4")
        line(ax, [(84, 34), (82, 34)])
        box(ax, 34, 6, 16, 8, "Relais K7", fs=7, fc="#fde8e6"); line(ax, [(42, 14), (42, 24)], dash=True)
        line(ax, [(91, 30), (91, 10), (50, 10)], dash=True)
        box(ax, 62, 44, 20, 6, "Bac de rétention (B11)", fs=6.5, fc="#fde8e6")
        ax.text(50, 54, "Transfert depuis la cuve externe — GE-B-02", ha="center", fontweight="bold")
        ax.text(2, 1, "Démarrage pompe : niveau bas journalier ; arrêt : niveau haut. Défaut → B18.", fontsize=7)
    return fig

def vidange_ge_a():
    fig, ax = canvas(9, 6)
    box(ax, 15, 18, 50, 30, "Carter moteur", fc="#e8e2d6")
    box(ax, 70, 30, 12, 14, "Filtre\nà huile", fc="#f1e6c9", fs=7)
    line(ax, [(65, 37), (70, 37)])
    box(ax, 35, 48, 8, 6, "Bouchon\nremplissage", fs=6, fc="#f4f6f8")
    box(ax, 36, 13, 8, 5, "Bouchon\nvidange", fs=6, fc="#fde8e6")
    box(ax, 18, 30, 6, 12, "Jauge", fs=6, fc="#f4f6f8")
    box(ax, 30, 2, 20, 8, "Bac de récupération\n≥ 35 L", fs=6.5, fc="#eef1f4")
    arrow(ax, 40, 13, 40, 10)
    for n, (x, y, tx, ty) in enumerate([(39, 54, 30, 58), (40, 13, 56, 8), (76, 44, 82, 52), (21, 42, 12, 50)], 1):
        callout(ax, x, y, n, tx, ty)
    ax.text(45, 60, "Points de vidange — GE-A-01", ha="center", fontweight="bold")
    return fig

def batteries_ge_b():
    fig, ax = canvas(9, 5)
    box(ax, 10, 14, 26, 18, "Batterie 1\n12 V 180 Ah", fc="#f1e6c9"); box(ax, 52, 14, 26, 18, "Batterie 2\n12 V 180 Ah", fc="#f1e6c9")
    for x, s in [(14, "+"), (32, "–"), (56, "+"), (74, "–")]:
        ax.add_patch(Circle((x, 32), 1.6, fc="#d2231a" if s == "+" else "#222")); ax.text(x, 35, s, ha="center", fontsize=10, fontweight="bold")
    line(ax, [(32, 32), (32, 38), (56, 38), (56, 32)], col="#555"); ax.text(44, 39.5, "pont série", ha="center", fontsize=6.5)
    line(ax, [(14, 32), (14, 44)], col="#d2231a"); ax.text(15, 44, "+24 V vers démarreur", fontsize=6.5)
    line(ax, [(74, 32), (74, 44)], col="#222"); ax.text(58, 44, "masse châssis", fontsize=6.5)
    ax.text(45, 6, "Dépose : 1) câble masse (–)  2) pont série  3) câble (+).  Repose : ordre inverse.", ha="center", fontsize=7)
    ax.text(45, 50, "Raccordement des batteries de démarrage — GE-B-02", ha="center", fontweight="bold")
    return fig

def consignation(kind="ge"):
    fig, ax = canvas(10, 4)
    steps = (["Séparer\n(mode ARRÊT +\nouverture QG)", "Condamner\n(cadenas + étiquette)", "Isoler batterie\n(coupe-batterie)", "Vérifier absence\nde tension (VAT)", "Signaler\nla zone"]
             if kind == "ge" else
             ["Transférer charge\n(bypass maint.)", "Ouvrir Q1, Q4,\nQB", "Condamner\n(cadenas + étiq.)", "Attendre 5 min\n(condensateurs)", "VAT bus DC\net sortie"])
    for i, s in enumerate(steps):
        box(ax, 2 + i * 20, 12, 16, 16, s, fs=6.5, fc="#fff3d6" if i in (1, 3) else "#f4f6f8")
        ax.add_patch(Circle((10 + i * 20, 31), 1.6, fc=INK)); ax.text(10 + i * 20, 31, str(i + 1), color="white", ha="center", va="center", fontsize=7, fontweight="bold")
        if i < 4: arrow(ax, 18 + i * 20, 20, 22 + i * 20, 20)
    ax.text(50, 37, "Étapes de consignation", ha="center", fontweight="bold")
    return fig

def synoptique_ups(model="VA-20", modes=False):
    fig, ax = canvas(10, 6)
    if not modes:
        box(ax, 2, 40, 12, 7, "Entrée\nredresseur", fs=6.5, fc="#e6eef7"); box(ax, 2, 50, 12, 7, "Entrée\nbypass", fs=6.5, fc="#e6eef7")
        switch(ax, 15, 43.5, "Q1"); switch(ax, 15, 53.5, "Q2")
        box(ax, 22, 37, 16, 13, "Redresseur\n(AC → DC)", fs=7, fc="#f4f6f8")
        box(ax, 46, 37, 16, 13, "Onduleur\n(DC → AC)", fs=7, fc="#f4f6f8")
        line(ax, [(38, 43.5), (46, 43.5)]); ax.text(42, 45, "bus DC", ha="center", fontsize=6)
        line(ax, [(42, 43.5), (42, 28)]); switch(ax, 42, 28, "QB", True, vertical=True)
        box(ax, 34, 12, 16, 12, "Batteries\n±240 V\n40 × 12 V 9 Ah", fs=6.5, fc="#f1e6c9")
        box(ax, 34, 50, 28, 7, "Bypass statique (thyristors)", fs=6.5, fc="#fff3d6")
        line(ax, [(18, 53.5), (34, 53.5)]); line(ax, [(62, 53.5), (70, 53.5), (70, 43.5)])
        line(ax, [(62, 43.5), (66, 43.5)]); switch(ax, 66, 43.5, "Q4"); line(ax, [(69, 43.5), (78, 43.5)])
        line(ax, [(8, 57), (8, 63), (74, 63), (74, 47)], dash=True); switch(ax, 74, 50, "Q3", False, vertical=True)
        ax.text(40, 64.5, "Bypass de maintenance (manuel)", ha="center", fontsize=6.5)
        box(ax, 80, 39, 16, 9, "Sortie charges\n400 V", fs=7, fc="#dfe9df")
        ax.text(50, 70, f"Schéma synoptique — onduleur {model}", ha="center", fontweight="bold")
        ax.text(2, 3, "Q1 entrée redresseur · Q2 entrée bypass · QB batterie · Q4 sortie onduleur · Q3 bypass de maintenance (normalement ouvert)", fontsize=6.5)
    else:
        titles = ["Mode normal (VERT)", "Sur batterie (ORANGE)", "Bypass statique (JAUNE)"]
        for k, t in enumerate(titles):
            x0 = 2 + k * 33
            box(ax, x0, 8, 30, 50, "", fc="white", ec=GRID)
            ax.text(x0 + 15, 54, t, ha="center", fontsize=7.5, fontweight="bold")
            for (lbl, y) in [("Réseau", 45), ("Redresseur", 35), ("Batterie", 24), ("Onduleur", 35), ("Charge", 14)]:
                pass
            box(ax, x0 + 2, 40, 9, 6, "Réseau", fs=6); box(ax, x0 + 2, 28, 9, 6, "Redr.", fs=6)
            box(ax, x0 + 19, 28, 9, 6, "Ond.", fs=6); box(ax, x0 + 10, 18, 10, 6, "Batt.", fs=6, fc="#f1e6c9")
            box(ax, x0 + 10, 10, 10, 5, "Charge", fs=6, fc="#dfe9df")
            hot = "#e0261b"
            if k == 0:
                arrow(ax, x0 + 6.5, 40, x0 + 6.5, 34, col=hot); arrow(ax, x0 + 11, 31, x0 + 19, 31, col=hot)
                arrow(ax, x0 + 23.5, 28, x0 + 18, 15, col=hot); arrow(ax, x0 + 13, 28, x0 + 14, 24, col="#888")
            elif k == 1:
                arrow(ax, x0 + 16, 24, x0 + 21, 28, col=hot); arrow(ax, x0 + 23.5, 28, x0 + 18, 15, col=hot)
                ax.text(x0 + 6.5, 37, "✕", ha="center", fontsize=10, color=hot)
            else:
                line(ax, [(x0 + 11, 43), (x0 + 27, 43), (x0 + 27, 13), (x0 + 20, 13)], col=hot)
                ax.text(x0 + 27.5, 40, "bypass", fontsize=5.5, rotation=90)
        ax.text(50, 64, f"Chemins de puissance selon le mode — {model}", ha="center", fontweight="bold")
    return fig

def batteries_ups_b():
    fig, ax = canvas(10, 6)
    for k, (name, y) in enumerate([("Chaîne C1", 38), ("Chaîne C2", 14)]):
        ax.text(2, y + 14, name + " — 40 blocs 12 V 65 Ah en série (480 V)", fontsize=7.5, fontweight="bold")
        for i in range(10):
            fc = "#f1e6c9"
            if k == 1 and i == 4: fc = "#fde8e6"
            box(ax, 4 + i * 8.5, y, 7, 10, f"{i*4+1}…{i*4+4}" if i < 9 else "37…40", fs=5.5, fc=fc, r=0.3)
            if i < 9: line(ax, [(11 + i * 8.5, y + 5), (12.5 + i * 8.5, y + 5)])
        line(ax, [(90, y + 5), (94, y + 5), (94, 30)])
    box(ax, 89, 24, 10, 8, "QF-BAT", fs=6.5, fc="#fff3d6")
    ax.text(4, 3, "Blocs numérotés Cx-01 à Cx-40 de gauche à droite et de haut en bas ; sonde de température au centre de l'armoire.", fontsize=6.5)
    ax.text(50, 58, "Câblage des chaînes batteries — armoire AB-60 (UPS-B-02)", ha="center", fontweight="bold")
    return fig

def ordre_batt_ups_a():
    fig, ax = canvas(9, 5)
    for t, x in enumerate([6, 48]):
        ax.text(x + 17, 42, f"Tiroir {'supérieur (+240 V)' if t == 0 else 'inférieur (–240 V)'}", ha="center", fontsize=7.5, fontweight="bold")
        for i in range(20):
            r, c = divmod(i, 5)
            box(ax, x + c * 7, 30 - r * 7, 6, 6, str(i + 1 + 20 * t), fs=6, fc="#f1e6c9", r=0.3)
    ax.text(45, 3, "Remplacer un tiroir complet à la fois ; ne jamais mélanger blocs neufs et usagés.", ha="center", fontsize=7)
    ax.text(45, 48, "Disposition des 40 blocs — UPS-A-01", ha="center", fontweight="bold")
    return fig

def bypass_schema():
    fig = synoptique_ups("VA-20")
    return fig

def picto(kind):
    fig, ax = canvas(2.2, 2.2)
    if kind in ("flamme", "corrosif", "gaz"):
        ax.add_patch(Polygon([(11, 21), (21, 11), (11, 1), (1, 11)], fc="white", ec="#d2231a", lw=3))
        if kind == "flamme":
            ax.add_patch(Polygon([(11, 17), (14, 12), (13.5, 8), (8.5, 8), (8, 12)], fc=INK))
        elif kind == "corrosif":
            ax.add_patch(Rectangle((6, 6), 10, 2, fc=INK)); ax.add_patch(Polygon([(7, 14), (9, 14), (8, 10)], fc=INK))
            ax.add_patch(Polygon([(13, 14), (15, 14), (14, 10)], fc=INK))
        else:
            ax.text(11, 11, "H₂", ha="center", va="center", fontsize=14, fontweight="bold")
    elif kind == "elec":
        ax.add_patch(Polygon([(11, 20), (21, 2), (1, 2)], fc="#f2d21b", ec=INK, lw=2))
        ax.add_patch(Polygon([(12, 16), (8, 9), (11, 9), (9, 4), (14, 11), (11, 11)], fc=INK))
    elif kind == "attention":
        ax.add_patch(Polygon([(11, 20), (21, 2), (1, 2)], fc="#f2d21b", ec=INK, lw=2))
        ax.text(11, 8, "!", ha="center", va="center", fontsize=20, fontweight="bold")
    elif kind == "gants":
        ax.add_patch(Circle((11, 11), 10, fc="#22408c")); ax.text(11, 11, "GANTS", ha="center", va="center", color="white", fontsize=7, fontweight="bold")
    elif kind == "lunettes":
        ax.add_patch(Circle((11, 11), 10, fc="#22408c")); ax.text(11, 11, "LUNETTES", ha="center", va="center", color="white", fontsize=5.5, fontweight="bold")
    elif kind == "flamme_interdite":
        ax.add_patch(Circle((11, 11), 10, fc="white", ec="#d2231a", lw=3)); ax.add_patch(Polygon([(11, 16), (13.5, 11), (13, 7), (9, 7), (8.5, 11)], fc=INK))
        line(ax, [(4, 4), (18, 18)], col="#d2231a", lw=3)
    return fig

def picto_row(kinds, name):
    ims = []
    for k in kinds:
        p = save(picto(k), f"_p_{k}.png"); ims.append(Image.open(p).convert("RGB").resize((260, 260)))
    out = Image.new("RGB", (len(ims) * 290, 270), "white")
    for i, im in enumerate(ims): out.paste(im, (i * 290 + 15, 5))
    p = os.path.join(FIG, name); out.save(p); return p

# ============================================================== photos (PIL)
def photoize(img, out, persp=0.06, blur=0.8, noise=9, dark=0.9, vignette=0.55, motion=0, quality=82, seed=1, warm=1.0):
    rnd = np.random.default_rng(seed)
    im = img.convert("RGB")
    W, H = im.size
    bg = Image.new("RGB", (int(W * 1.25), int(H * 1.3)), (88, 92, 96))
    a = np.array(bg).astype(float)
    a += rnd.normal(0, 6, a.shape); a[..., 0] *= warm
    bg = Image.fromarray(np.clip(a, 0, 255).astype("uint8"))
    bg.paste(im, ((bg.width - W) // 2, (bg.height - H) // 2))
    W2, H2 = bg.size; d = persp
    coeffs = _find_coeffs([(0, 0), (W2, 0), (W2, H2), (0, H2)],
                          [(W2 * d, H2 * d * 0.6), (W2 * (1 - d * 0.3), 0), (W2, H2), (W2 * d * 0.4, H2 * (1 - d * 0.5))])
    bg = bg.transform((W2, H2), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    a = np.array(bg).astype(float)
    yy, xx = np.mgrid[0:H2, 0:W2]
    r = np.sqrt(((xx - W2 * 0.45) / W2) ** 2 + ((yy - H2 * 0.4) / H2) ** 2)
    a *= (1 - vignette * r ** 1.6)[..., None] * dark
    a += rnd.normal(0, noise, a.shape)
    im = Image.fromarray(np.clip(a, 0, 255).astype("uint8"))
    if motion:
        k = np.zeros((motion, motion)); k[motion // 2, :] = 1.0 / motion
        from PIL import ImageFilter as F
        im = im.filter(F.Kernel((motion, motion), k.flatten().tolist(), scale=1)) if motion in (3, 5) else im.filter(F.BoxBlur(motion / 2))
    im = im.filter(ImageFilter.GaussianBlur(blur))
    im = im.resize((int(W2 * 0.75), int(H2 * 0.75)), Image.LANCZOS)
    im.save(out, "JPEG", quality=quality)
    return out

def _find_coeffs(pa, pb):
    m = []
    for p1, p2 in zip(pa, pb):
        m.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        m.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
    A = np.array(m, dtype=float); B = np.array(pb).reshape(8)
    res = np.linalg.solve(A, B)
    # transform() attend la correspondance inverse (sortie → entrée)
    A2 = []
    for p1, p2 in zip(pb, pa):
        A2.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        A2.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
    return np.linalg.solve(np.array(A2, float), np.array(pa).reshape(8)).tolist()

def fig_to_img(fig):
    p = save(fig, "_tmp.png"); return Image.open(p).convert("RGB")

def glow(img, spots):
    """Ajoute un halo lumineux autour des voyants allumés (coordonnées relatives)."""
    im = img.convert("RGB"); W, H = im.size
    layer = Image.new("RGB", im.size, (0, 0, 0)); d = ImageDraw.Draw(layer)
    for (x, y, col, r) in spots:
        cx, cy = x * W, y * H
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    layer = layer.filter(ImageFilter.GaussianBlur(28))
    return Image.fromarray(np.clip(np.array(im).astype(int) + np.array(layer).astype(int) * 0.8, 0, 255).astype("uint8"))

def nameplate(lines, size=(1500, 820), plate=(205, 205, 200), font_sz=46):
    im = Image.new("RGB", size, plate); d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_sz + 10)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf", font_sz)
    d.rectangle([8, 8, size[0] - 8, size[1] - 8], outline=(60, 60, 60), width=6)
    for (x, y) in [(40, 40), (size[0] - 40, 40), (40, size[1] - 40), (size[0] - 40, size[1] - 40)]:
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(150, 150, 150), outline=(80, 80, 80), width=3)
    d.text((80, 50), lines[0], font=f, fill=(25, 25, 25))
    for i, t in enumerate(lines[1:]):
        d.text((80, 150 + i * 72), t, font=f2, fill=(30, 30, 30))
    a = np.array(im).astype(float); a += np.random.default_rng(3).normal(0, 5, a.shape)
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8"))

def battery_rack():
    W, H = 1800, 1200
    im = Image.new("RGB", (W, H), (70, 74, 78)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    for row in range(3):
        y0 = 80 + row * 370
        d.rectangle([40, y0 + 300, W - 40, y0 + 330], fill=(150, 150, 155))
        for c in range(7):
            x0 = 80 + c * 240; n = 15 + c if row == 1 else None
            bulge = (row == 1 and c == 2)
            if bulge:
                d.rounded_rectangle([x0 - 14, y0 + 40, x0 + 214, y0 + 300], radius=40, fill=(32, 32, 34), outline=(10, 10, 10), width=4)
                d.ellipse([x0 - 22, y0 + 90, x0 + 30, y0 + 260], fill=(36, 36, 38))
                d.ellipse([x0 + 170, y0 + 90, x0 + 222, y0 + 260], fill=(36, 36, 38))
            else:
                d.rectangle([x0, y0 + 50, x0 + 200, y0 + 300], fill=(28, 28, 30), outline=(10, 10, 10), width=3)
            d.rectangle([x0 + 25, y0 + 25, x0 + 55, y0 + 50], fill=(170, 30, 25)); d.rectangle([x0 + 145, y0 + 25, x0 + 175, y0 + 50], fill=(40, 40, 40))
            if row == 1:
                d.rectangle([x0 + 50, y0 + 150, x0 + 150, y0 + 190], fill=(230, 230, 230))
                d.text((x0 + 58, y0 + 152), f"C2-{15 + c:02d}", font=f, fill=(20, 20, 20))
            if c < 6: d.line([x0 + 175, y0 + 37, x0 + 265, y0 + 37], fill=(190, 150, 60), width=8)
    return im

def build_all():
    out = {}
    def S_(fig, name): out[name] = save(fig, name)
    f, _ = panel_ge_a(); S_(f, "ge_a_panel.png")
    f, _ = panel_ge_b(); S_(f, "ge_b_panel.png")
    S_(overview_ge("GA-250", "400 L", "250 kVA"), "ge_a_overview.png")
    S_(overview_ge("GB-500", "900 L", "500 kVA"), "ge_b_overview.png")
    S_(unifilaire_ge_a(), "ge_a_unifilaire.png"); S_(charge_batt_ge_a(), "ge_a_charge.png"); S_(capteurs_ge_a(), "ge_a_capteurs.png")
    S_(carburant_ge_b(1), "ge_b_carburant1.png"); S_(carburant_ge_b(2), "ge_b_carburant2.png")
    S_(vidange_ge_a(), "ge_a_vidange.png"); S_(batteries_ge_b(), "ge_b_batteries.png")
    S_(consignation("ge"), "consignation_ge.png"); S_(consignation("ups"), "consignation_ups.png")
    S_(synoptique_ups("VA-20"), "ups_a_synoptique.png"); S_(synoptique_ups("VA-20", modes=True), "ups_a_modes.png")
    f, _ = panel_ups_a("vert"); S_(f, "ups_a_panel.png")
    f, _ = front_ups_b(txt=("SYSTÈME NORMAL", "CHARGE 41 %  3/3 MODULES", "BATT 100 %  24,1 °C")); S_(f, "ups_b_front.png")
    S_(batteries_ups_b(), "ups_b_batteries.png"); S_(ordre_batt_ups_a(), "ups_a_ordre_batt.png")
    out["picto_gazole.png"] = picto_row(["flamme", "attention", "flamme_interdite", "gants"], "picto_gazole.png")
    out["picto_batt.png"] = picto_row(["corrosif", "gaz", "elec", "lunettes", "flamme_interdite"], "picto_batt.png")
    out["picto_elec.png"] = picto_row(["elec", "attention", "gants"], "picto_elec.png")

    # ---- photos synthétiques
    imgd = os.path.join(CORPUS, "images"); os.makedirs(imgd, exist_ok=True)
    f, _ = panel_ge_a(lcd=("A12 PRÉALARME", "TEMP. LIQ. 92 °C", "MODE AUTO  2770 h"))
    im = glow(fig_to_img(f), [(0.69, 0.25, (60, 255, 90), 18), (0.80, 0.25, (255, 150, 30), 26)])
    photoize(im, os.path.join(imgd, "photo_panneau_ge_a.jpg"), seed=11, persp=0.05)
    f, _ = panel_ge_b(lcd=("", "", "", ""), leds=("vert", "orange"))
    im = glow(fig_to_img(f), [(0.78, 0.26, (60, 255, 90), 18), (0.78, 0.41, (255, 150, 30), 28)])
    photoize(im, os.path.join(imgd, "photo_panneau_ge_b.jpg"), seed=12, persp=0.09, blur=1.3, dark=0.75)
    f, _ = panel_ups_a("orange")
    im = glow(fig_to_img(f), [(0.66, 0.38, (255, 150, 30), 26)])
    photoize(im, os.path.join(imgd, "photo_panneau_ups_a.jpg"), seed=13, persp=0.07)
    f, _ = front_ups_b()
    im = glow(fig_to_img(f), [(0.78, 0.24, (60, 255, 90), 14), (0.78, 0.30, (255, 150, 30), 22)])
    photoize(im, os.path.join(imgd, "photo_ecran_alarme_ups_b.jpg"), seed=14, persp=0.06)
    plate_a = nameplate(["NORDAL ÉNERGIE — GROUPE ÉLECTROGÈNE", "Modèle : GA-250        N° série : NA250-23-0117",
                         "Puissance : 250 kVA ESP / 225 kVA PRP", "Tension : 400/230 V 3~ 50 Hz   cos φ 0,8",
                         "Courant nominal : 361 A      Masse : 2 350 kg", "Année : 2023     Équipement : GE-A-01"])
    photoize(plate_a, os.path.join(imgd, "photo_plaque_ge_a.jpg"), seed=15, persp=0.05, blur=0.6)
    plate_b = nameplate(["NORDAL ÉNERGIE — GROUPE ÉLECTROGÈNE", "Modèle : GB-500        N° série : NB500-21-0042",
                         "Puissance : 500 kVA ESP / 450 kVA PRP", "Tension : 400/230 V 3~ 50 Hz   cos φ 0,8",
                         "Courant nominal : 722 A      Masse : 4 900 kg", "Année : 2021     Équipement : GE-B-02"], plate=(170, 165, 150))
    photoize(plate_b, os.path.join(imgd, "photo_plaque_ge_floue.jpg"), seed=16, persp=0.12, blur=7, dark=0.55, noise=18, quality=55)
    photoize(battery_rack(), os.path.join(imgd, "photo_batteries_ups_b.jpg"), seed=17, persp=0.08, blur=1.0, dark=0.8)
    return out

if __name__ == "__main__":
    o = build_all(); print(len(o), "figures ;", sorted(os.listdir(os.path.join(CORPUS, "images"))))
