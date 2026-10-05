# LAB 07 — End-to-End Challenge

**Temps cible : 60 min** · Difficulté : ⭐⭐⭐⭐ · Prérequis : LAB 01 → 06

Objectif : reproduire une version réduite du Bloc 2, **chronométrée et sans
regarder les solutions**. C'est la répétition générale avant l'examen blanc 4 h.

## Entrée

```text
../exam/sujet/data/raw/deliveries.json
```

(chemin relatif au dossier `labs/` : `../exam/sujet/data/raw/deliveries.json`)

## Livrables en 60 minutes

```text
[ ] exploration rapide
[ ] etl.py
[ ] deliveries_clean.csv
[ ] modèles ORM Customer / Delivery
[ ] DB Docker active
[ ] ingestion
[ ] ML + model.joblib
[ ] 3 tests
[ ] architecture ASCII
```

## Timebox

```text
00–10  exploration
10–20  ETL
20–35  DB + ORM + ingestion
35–48  ML
48–55  tests
55–60  documentation
```

## Règle

Si vous dépassez 60 min, **arrêtez-vous** et rédigez un
[post-mortem](POST_MORTEM_TEMPLATE.md) **avant** de consulter les solutions des
labs précédents. Le but n'est pas la perfection, c'est de mesurer votre vitesse.

## Structure de travail conseillée

Créer un dossier de rendu séparé (ne pas polluer les labs) :

```text
challenge/
├── src/
│   ├── config.py
│   ├── etl.py
│   ├── models.py
│   ├── ingest.py
│   └── train_model.py
├── tests/test_etl.py
├── data/raw/deliveries.json
├── docker-compose.yml
├── .env
└── ARCHITECTURE.md
```

Vous pouvez partir de `../exam/starter_project/` (structure déjà amorcée avec
`requirements.txt`, `src/`, `tests/`, `docker-compose.yml`).

## Critères de réussite

- [ ] `deliveries_clean.csv` généré et cohérent (pas de doublon `delivery_id`) ;
- [ ] `docker compose ps` : DB `Up` ;
- [ ] tables créées et ingestion idempotente (2e passe = 0 nouvelle ligne) ;
- [ ] `model.joblib` sauvegardé, métriques affichées ;
- [ ] ≥ 3 tests qui passent ;
- [ ] schéma d'architecture ASCII dans `ARCHITECTURE.md`.

## Dépannage express

| Symptôme | Réflexe |
|---|---|
| port DB occupé | changer `DB_PORT` dans `.env` |
| `Access denied` | aligner `.env` (user/password/port) partout |
| `FileNotFoundError` | chemins `Path(__file__)`, jamais relatifs au cwd |
| temps dépassé | STOP → post-mortem |

## Après le challenge

1. Remplir le [post-mortem](POST_MORTEM_TEMPLATE.md).
2. Identifier le bloc le plus lent → le rejouer (LAB correspondant).
3. Comparer avec `../exam/correction/12_RNCP_38919_BLOC_2_CORRIGE_EXAMEN_BLANC_01.md`.
