# Fiche de référence MaintiDoc (interne — hors corpus)

Source unique de vérité utilisée pour générer le corpus. **Ne pas indexer** : la section vérité terrain sert à évaluer le module RE.

## GE-A-01 — Groupe électrogène diesel GA-250 (NORDAL Énergie)

| Voyant | État | Signification |
|---|---|---|
| VERT | Fixe | Groupe prêt (mode AUTO) ou en marche, aucun défaut |
| ORANGE | Fixe | Préalarme active : le groupe reste en marche (voir code sur l'écran ; cas le plus fréquent : A12 température liquide ≥ 95 °C) |
| ORANGE | Clignotant | Maintenance due (A22) |
| ROUGE | Fixe | Arrêt sur défaut : le groupe est arrêté et verrouillé jusqu'au réarmement |

Seuils : temp_prealarme = 95, temp_arret = 105, huile_prealarme = 2.0, huile_arret = 1.4, survitesse = 1725, batt_basse = 23.0, carburant_bas = 20

Tickets ouverts : INT-GEA-2026-012 (Préalarme température à 92 °C lue sur l'écran (ambiante 41 °C))

## GE-B-02 — Groupe électrogène diesel GB-500 (NORDAL Énergie)

| Voyant | État | Signification |
|---|---|---|
| VERT | Fixe | Groupe en marche ou prêt en mode AUTO |
| ORANGE | Fixe | Défaut de charge batterie de démarrage (B07) ou défaut chargeur (B08) — les autres préalarmes s'affichent uniquement sur l'écran avec le buzzer |
| ROUGE | Fixe | Arrêt sur défaut, réarmement nécessaire |

Seuils : temp_prealarme = 98, temp_arret = 108, huile_prealarme = 2.2, huile_arret = 1.5, survitesse = 1740, batt_basse = 24.0, carburant_bas = 25

Tickets ouverts : INT-GEB-2026-010 (Essai en charge mensuel)

## UPS-A-01 — Onduleur online double conversion VA-20 (VOLTARIS)

| Voyant | État | Signification |
|---|---|---|
| VERT | Fixe | Fonctionnement normal sur réseau (online) |
| ORANGE | Fixe | Fonctionnement sur batterie : réseau absent ou hors tolérance (U07, U08) |
| ORANGE | Clignotant | Batterie faible : autonomie restante < 3 min (U09) |
| JAUNE | Fixe | Charge alimentée par le bypass (statique ou maintenance) |
| ROUGE | Fixe | Défaut — voir le code sur l'écran |

Tickets ouverts : aucun

## UPS-B-02 — Onduleur modulaire VB-60M (VOLTARIS)

| Voyant | État | Signification |
|---|---|---|
| VERT | Fixe | Système normal |
| ORANGE | Fixe | Alarme active non critique — lire le code Mxx sur l'écran |
| ROUGE | Fixe | Alarme critique ou charge non protégée |

Tickets ouverts : INT-UPSB-2026-012 (Inspection armoire : bloc C2-17 gonflé (photo))

## Contradictions prévues

- **proc_vidange_ge_a_v1 / proc_vidange_ge_a_v2** : Intervalle de vidange 250 h (v1) contre 500 h (v2) ; couple de serrage du bouchon 45 N·m (v1) contre 50 N·m (v2). La v2 fait foi (historique INT-GEA-2025-002).
- **proc_bypass_ups_a_v1 / proc_bypass_ups_a_v2** : v1 fait fermer Q3 avant le transfert sur bypass statique (cause de l'incident INT-UPSA-2024-018) ; v2 impose le transfert sur bypass statique d'abord. La v2 fait foi.
- **manuel_ge_a / données du contrôleur (module RE)** : Seuil de préalarme température 95 °C dans le manuel contre 92 °C configuré (registre 40112, firmware v4.2).
- **manuel_ups_a / journal binaire (module RE)** : Test batterie automatique tous les 30 jours selon le manuel contre tous les 7 jours dans le journal (événement 0x2C).

## Cas ambigus

- Voyant ORANGE fixe : préalarme (GE A), défaut de charge batterie (GE B), fonctionnement sur batterie (UPS A), alarme générale (UPS B).
- photo_panneau_ge_b : orange allumé sans écran lisible, peut être confondu avec un panneau d'onduleur.
- photo_plaque_ge_floue : modèle non identifiable — clarification attendue.

## Vérité terrain du module de reverse engineering

### GE-A-01 registres 40110-40118

- `40110` : Compteur de démarrages
- `40111` : Compteur de démarrages échoués
- `40112` : Seuil de préalarme température configuré (°C) — valeur réelle 92 depuis le firmware v4.2, alors que le manuel indique 95 °C
- `40113` : Seuil d'arrêt température configuré (°C) — 105
- `40114` : Temps cumulé en préalarme (min)
- `40115` : Code du dernier défaut (même codage que 40021)
- `40116-40117` : Horodatage du dernier défaut (uint32, secondes Unix, poids fort en premier)
- `40118` : État des voyants (bit0 vert, bit1 orange, bit2 orange clignotant, bit3 rouge)

### UPS-A-01 événements 0x2A-0x31

- `0x2A` : Ventilateur 1 — vitesse basse
- `0x2B` : Ventilateur 2 — vitesse basse
- `0x2C` : Test batterie automatique démarré — en pratique tous les 7 jours, alors que le manuel indique 30 jours
- `0x2D` : Test batterie automatique interrompu (réseau instable)
- `0x2E` : Dérive de température batterie (> 28 °C, pré-seuil de U22)
- `0x2F` : Transfert bypass statique réussi (durée en ms dans le champ valeur)
- `0x30` : Retour onduleur après bypass
- `0x31` : Seuil d'alarme batterie faible reconfiguré

### UPS-A-01 — octets réservés du journal EVENTS.BIN

- octets 6-7 : valeur associée à l'événement (int16, ex. durée de transfert en ms pour 0x2F)
- octets 8-9 : charge de sortie au moment de l'événement (uint16, %)
- octets 10-11 : tension batterie (uint16, ×0,1 V)
- octets 12-13 : température batterie (int16, ×0,1 °C)
