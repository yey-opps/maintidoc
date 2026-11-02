# MaintiDoc — Livrable 1 : cadrage, corpus et architecture

> **Mise à jour (2 novembre 2026) :** Abdellah a rejoint le projet. L'équipe, initialement composée de Yasmina seule, devient l'équipe YASMINA-ABDELLAH.

**Équipe :** YASMINA-ABDELLAH

**Membres :**

- Yasmina — corpus, ingestion, recherche multimodale, reranker, décodeur RE
- Abdellah — orchestrateur LangGraph, VLM, serveur MCP, interface, déploiement

**Module :** IA générative multimodale, EMSI 2026

## Objectif du projet

MaintiDoc est un assistant documentaire multimodal et agentique pour les techniciens de maintenance. À partir d'une question et d'une photo (voyant, écran, plaque signalétique), il retrouve les documents pertinents, répond en citant la page et l'élément exacts, consulte l'historique de l'équipement via un serveur MCP et prépare un ticket que l'utilisateur doit approuver avant sa création.

Le prototype couvre deux familles d'équipements de secours énergie d'un data center fictif :

- **famille_1 — groupes électrogènes** : GE-A-01 (GA-250), GE-B-02 (GB-500)
- **famille_2 — onduleurs** : UPS-A-01 (VA-20), UPS-B-02 (VB-60M)

Une extension optionnelle de rétro-ingénierie (lecture seule) décodera les registres et journaux binaires des équipements pour détecter les écarts avec les manuels.

## Contenu du ZIP

| Élément | Description |
|---|---|
| `L1_MaintiDoc_YASMINA-ABDELLAH_Rapport.pdf` | Rapport complet, parties 2.1 à 2.6 (14 pages + annexes) |
| `L1_MaintiDoc_YASMINA-ABDELLAH_LienGitHub.txt` | URL du dépôt GitHub |
| `README.md` | Ce fichier |
| `L1_MaintiDoc_YASMINA-ABDELLAH_Corpus/` | 39 documents (32 PDF, 7 photos), `inventaire.csv`, `prompts_corpus.md` |

Corpus : 100 % synthétique, en français ; 37 documents avec éléments visuels, 2 documents scannés, 2 paires de documents contradictoires, 1 document piégé (injection de prompt), 2 photos ambiguës.

## Structure du dépôt

```
maintidoc/
├── README.md
├── .gitignore            # exclut .env, .venv, modèles et index
├── requirements.txt
├── docs/
│   └── diagrammes/       # architecture et flux (figures du rapport)
├── corpus/
│   ├── inventaire.csv
│   ├── prompts_corpus.md
│   ├── documents/
│   │   ├── famille_1/
│   │   └── famille_2/
│   └── images/
├── generation/           # scripts ayant produit le corpus (fiche de référence)
├── interne/              # vérité terrain du module RE (ne pas indexer)
├── app/  agents/  rag/  mcp_server/  prompts/  ui/  data/  tests/   # code (à partir de S2)
```
