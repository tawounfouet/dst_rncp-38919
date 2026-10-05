# Protocole — Simulation Examen Blanc Bloc 2 (4 h)

Objectif : reproduire les conditions réelles et mesurer ta vitesse réelle.
**Ne jamais ouvrir la correction avant la fin.**

---

## 0. Avant de lancer le chrono (5 min)

```bash
cd simulation
./start_mock_exam.sh            # prépare candidate_workspace/ + venv + .env
# (optionnel) ./start_mock_exam.sh --force   pour repartir de zéro
```

Ce que tu as le droit d'ouvrir :

```text
✅ exam/sujet/11_RNCP_38919_BLOC_2_EXAMEN_BLANC_01.md
✅ exam/starter_project/            (référence de structure)
✅ resources/03..09                  (guides, en cas de blocage > 3 min, pas avant)
✅ la doc officielle des libs (pandas / SQLAlchemy / scikit-learn)
```

Interdit :

```text
❌ exam/correction/   (le .md ET green_delivery/)
❌ les labs/ solution/
❌ IA générative pour écrire le code
```

---

## 1. Règles de simulation

```text
Durée              : 240 min, chrono continu, sans pause
Écran              : idéalement un seul
Tél                : en mode avion
Blocage            : > 3 min → note-le et passe au suivant
À 03:55            : STOP CODING
À 04:00            : archive de rendu
```

**Règle d'or** : un livrable manquant ne se remplace pas par une explication.

---

## 2. Planning cible

```text
00:00–00:15  Lecture / cadrage
00:15–00:45  Notebook exploration
00:45–01:20  ETL
01:20–02:00  Docker + DB + ORM
02:00–02:30  Ingestion
02:30–03:00  ML
03:00–03:25  Intégration / Compose
03:25–03:40  Tests
03:40–03:55  Documentation
03:55–04:00  Archive / vérification
```

---

## 3. Commandes de survie

```bash
# environnement (déjà fait par start_mock_exam.sh)
cd candidate_workspace && source .venv/bin/activate

# DB
cp .env.example .env
docker compose up -d
docker compose ps
docker compose exec db mariadb -u<user> -p<pass> <db> -e "SHOW TABLES;"

# pipeline
python -m src.etl
python -m src.create_database
python -m src.ingest
python -m src.train_model
pytest -v
```

---

## 4. Definition of Done (le blanc est réussi si tout est ✅)

```text
[ ] notebooks/01_exploration.ipynb présent et exécuté
[ ] src/etl.py : extract / validate / transform / save
[ ] data/processed/deliveries_clean.csv : 23 lignes, 0 doublon, 0 null
[ ] docker-compose.yml : DB + phpMyAdmin + volume + env
[ ] src/models.py : PK, FK, relationship
[ ] src/create_database.py : create_all
[ ] src/database.py + src/config.py : URL depuis .env
[ ] src/ingest.py : idempotent (2e passe = 0 ajout)
[ ] customers = 22, deliveries = 23
[ ] src/train_model.py : pipeline + métriques
[ ] models/model.joblib présent
[ ] tests : schéma + doublon + erreur → pytest OK
[ ] ARCHITECTURE.md : schéma ASCII + limites + impact écologique
[ ] archive de rendu créée
```

---

## 5. Auto-correction (après le chrono uniquement)

```bash
cd simulation
python grade.py candidate_workspace --with-db
```

Le script applique le barème d'entraînement (document 12, section 45) et sort un score /100.

| Bloc | Points |
|---|---:|
| Exploration / notebook | 10 |
| ETL / qualité Python | 15 |
| Modèle relationnel | 10 |
| Docker / variables / persistance | 10 |
| SQLAlchemy / ORM | 15 |
| Ingestion | 10 |
| Machine Learning | 15 |
| Tests | 10 |
| Documentation / impact | 5 |
| **TOTAL** | **100** |

Puis compare à la solution de référence : `exam/correction/green_delivery/`.

Interprétation :

```text
90–100  chaîne très maîtrisée
75–89   bon niveau, quelques fragilités
60–74   pipeline compris, automatismes à renforcer
< 60    refaire le blanc après révision ciblée
```

---

## 6. Post-mortem (obligatoire, à chaud)

Remplir immédiatement :

```text
Temps réel exploration    : ____
Temps réel ETL            : ____
Temps réel Docker/ORM     : ____
Temps réel ingestion      : ____
Temps réel ML             : ____
Temps réel tests          : ____
Temps réel documentation  : ____
TOTAL                     : ____ / 240
```

Puis répondre :

```text
Bloc le plus lent :
Bug le plus coûteux :
Syntaxe que j'ai dû rechercher :
Livrable commencé trop tard :
Automatisme à travailler avant le prochain blanc :
```

Utiliser aussi `exam/.../labs/LAB_07_END_TO_END_CHALLENGE/POST_MORTEM_TEMPLATE.md`.

---

## 7. Questions orales à savoir défendre (sans notes)

1. Quel est le grain du dataset ?
2. Pourquoi `delivery_id` est-il la PK ?
3. Pourquoi `customer_id` est-il une FK dans `deliveries` ?
4. Différence entre `ForeignKey` et `relationship` ?
5. Pourquoi normaliser `customer_city` ?
6. Comment as-tu traité les nulls et le doublon ?
7. Pourquoi un volume Docker ?
8. Pourquoi des variables d'environnement ?
9. Pourquoi exclure `delivery_minutes` du modèle ?
10. Pourquoi les métriques ML sont-elles fragiles ici ?
11. Pourquoi sauvegarder la pipeline entière avec `joblib` ?
12. Quels tests protègent l'ingestion ?
13. Quelles sont les limites de ta solution ?
14. Que ferais-tu avec 2 h de plus ?

---

## 8. Dépannage express

| Symptôme | Réflexe |
|---|---|
| port 3306 occupé | changer `DB_PORT` dans `.env` (3307) |
| `Access denied` | aligner user/password/port entre `.env` et compose |
| `ModuleNotFoundError: src` | lancer depuis la racine (`python -m src.xxx`) |
| `FileNotFoundError` | chemins `Path(__file__)`, pas relatifs au cwd |
| `pytest` ne trouve pas `src` | ajouter `conftest.py` à la racine du projet |
| chrono dépassé | STOP → post-mortem |
