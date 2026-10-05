# LAB 07 — Guide débutant (construire la solution end-to-end)

> **Public** : tu as fait les LAB 01 à 06 (ou tu veux voir la vue d'ensemble).
> Ce lab est un **challenge chronométré** : il n'a **pas** de dossier `solution/`
> exprès. Ce guide t'explique, pas à pas, comment assembler **toi-même** la
> solution complète.
>
> La solution de référence complète et vérifiée se trouve dans
> `../../exam/correction/green_delivery/`.

---

## Étape 0 — De quoi parle-t-on ?

Le challenge consiste à reproduire une mini-chaîne Data Engineering + ML :

```text
JSON brut
  → exploration (pandas)
  → ETL (nettoyage)
  → CSV propre
  → base de données (Docker + ORM)
  → ingestion
  → modèle ML
  → tests
  → documentation
```

Chaque maillon correspond à un lab :

| Maillon | Lab qui l'explique |
|---|---|
| Explorer | LAB 01 |
| Nettoyer (ETL) | LAB 02 |
| Base Docker | LAB 03 |
| ORM | LAB 04 |
| Ingestion + tests | LAB 05 |
| ML | LAB 06 |

Ce lab, c'est **tout enchaîner en 60 minutes**.

---

## Étape 1 — Préparer son espace de travail

Ne travaille **pas** dans les dossiers des labs précédents. Crée un dossier dédié :

```text
challenge/
├── data/
│   ├── raw/deliveries.json          ← copie du fichier du sujet (exam/sujet/data/raw/deliveries.json)
│   └── processed/                   ← vide au départ
├── notebooks/01_exploration.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── etl.py
│   ├── database.py
│   ├── models.py
│   ├── create_database.py
│   ├── ingest.py
│   └── train_model.py
├── tests/test_etl.py
├── models/
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── ARCHITECTURE.md
```

Tu peux partir de `../../exam/starter_project/` (structure déjà amorcée) et
compléter les `TODO`.

Le fichier de données : `../../exam/sujet/data/raw/deliveries.json`.

---

## Étape 2 — Explorer les données (15 min)

But : **comprendre** avant de transformer.

```python
import pandas as pd

df = pd.read_json("data/raw/deliveries.json")
print(df.shape)            # (24, 9)
print(df.columns.tolist())
df.info()
print(df.isna().sum())             # distance_km, traffic_level, weather : 1 chacun
print("doublons:", df.duplicated().sum())   # 1
print(df["late_delivery"].value_counts())
```

Questions à savoir te poser (voir LAB 01 pour chaque notion) :

```text
Quel est le grain ?              → une ligne = une livraison
Quelle est la clé métier ?       → delivery_id
Y a-t-il des doublons ?          → oui (delivery_id 1020)
Quelles colonnes ont des vides ? → distance_km, traffic_level, weather
Faut-il normaliser une colonne ? → customer_city (casse / espaces)
```

---

## Étape 3 — Écrire l'ETL (20 min) — LAB 02

4 fonctions, chacune avec **une responsabilité** :

```python
def extract(path):        # lit le JSON, FileNotFoundError si absent
def validate_schema(df):  # ValueError si une colonne manque
def transform(df):        # nettoie et renvoie un tableau propre
def save_processed(df, path):  # écrit le CSV
```

Décisions de nettoyage (à documenter) :

```text
doublon delivery_id  → garder la 1re occurrence (drop_duplicates)
customer_city        → strip() + lower()
vehicle_type         → strip() + lower()
distance_km vide     → médiane
traffic_level vide   → "unknown"
weather vide         → "unknown"
```

Résultat attendu : **24 lignes → 23 lignes**, 0 doublon, 0 valeur vide, et
`data/processed/deliveries_clean.csv` créé.

> Détails et explication de chaque fonction : `../LAB_02_ETL_PYTHON/solution/GUIDE_DEBUTANT.md`.

---

## Étape 4 — La base de données (15 min) — LAB 03

`docker-compose.yml` + `.env` :

```yaml
services:
  db:
    image: mariadb:11
    environment:
      MARIADB_DATABASE: ${DB_NAME}
      MARIADB_USER: ${DB_USER}
      MARIADB_PASSWORD: ${DB_PASSWORD}
      MARIADB_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    ports:
      - "${DB_PORT}:3306"
    volumes:
      - db_data:/var/lib/mysql
  phpmyadmin:
    image: phpmyadmin:latest
    environment: { PMA_HOST: db, PMA_PORT: 3306 }
    ports:
      - "${PMA_PORT}:80"
    depends_on: [db]
volumes:
  db_data:
```

```bash
cp .env.example .env
docker compose up -d
docker compose ps
```

> Rappel : dans Docker, on joint la base par le **nom de service** (`db`), pas `localhost`.
> Détails : `../LAB_03_DOCKER_COMPOSE_DB/solution/GUIDE_DEBUTANT.md`.

---

## Étape 5 — Le modèle relationnel (5 min)

```text
customers                       deliveries
──────────                      ──────────
customer_id  PK                 delivery_id   PK
customer_city                   customer_id   FK → customers.customer_id
                                vehicle_type
                                distance_km
                                traffic_level
                                weather
                                delivery_minutes
                                late_delivery
```

- **PK** : identifie une ligne de façon unique.
- **FK** : `deliveries.customer_id` pointe vers `customers.customer_id`.
- Cardinalité : **1 client → N livraisons**.

---

## Étape 6 — ORM + création des tables + ingestion (15 min) — LAB 04/05

Trois fichiers :

```text
src/config.py           → DATABASE_URL lu depuis .env
src/database.py         → engine + Session
src/models.py           → classes Customer et Delivery
src/create_database.py  → Base.metadata.create_all(engine)
src/ingest.py           → insère clients puis livraisons, sans doublon
```

**Ordre important** : insérer d'abord `customers`, **ensuite** `deliveries`
(à cause de la clé étrangère).

**Idempotence** : l'ingestion ne doit pas créer de doublon si on la relance.
Astuce : ne garder que les `delivery_id` qui n'existent pas déjà
(voir `../LAB_05_INGESTION_AND_TESTS/solution/GUIDE_DEBUTANT.md`).

```bash
python -m src.create_database
python -m src.ingest      # 22 customers, 23 deliveries
python -m src.ingest      # 0, 0  (idempotent)
```

> Pourquoi `python -m src.xxx` ? Pour que Python trouve le paquet `src`.
> Lance depuis la **racine** du projet.

---

## Étape 7 — Le modèle ML (15 min) — LAB 06

- `X` = features (`distance_km`, `customer_city`, `vehicle_type`, `traffic_level`, `weather`).
- `y` = `late_delivery`.
- **Exclure** `delivery_minutes` (fuite d'information), `delivery_id`, `customer_id`.
- Préparation **dans** la pipeline (imputation + `OneHotEncoder`).
- `train_test_split(test_size=0.30, random_state=42, stratify=y)`.
- `LogisticRegression`, métriques, puis `joblib.dump` → `models/model.joblib`.

> Détails : `../LAB_06_MACHINE_LEARNING_JOBLIB/solution/GUIDE_DEBUTANT.md`.

---

## Étape 8 — Les tests (10 min) — LAB 05

Au minimum 3 tests :

```text
- dataset valide (happy path)
- colonne obligatoire absente → ValueError
- delivery_id dupliqué → ValueError
```

```bash
pytest -v
```

> Piège classique : si `pytest` ne trouve pas `src`, ajoute un `conftest.py` vide
> à la racine du projet (il met la racine dans le chemin d'import).

---

## Étape 9 — La documentation (5 min)

`ARCHITECTURE.md` doit contenir :

```text
contexte · architecture ASCII · pipeline ETL · modèle relationnel
Docker · ORM · ingestion · ML · tests · impact écologique
choix techniques · limites · pistes d'amélioration
```

Exemple de schéma ASCII :

```text
deliveries.json → pandas → ETL → deliveries_clean.csv
                                        │
                            ┌───────────┴───────────┐
                            ▼                       ▼
                     SQLAlchemy ORM           scikit-learn
                            │                       │
                            ▼                       ▼
                      MariaDB (Docker)        model.joblib
```

---

## Étape 10 — Vérifier le rendu (DoD)

```text
[ ] 23 lignes dans deliveries_clean.csv, 0 doublon, 0 null
[ ] docker compose ps : db Up
[ ] tables customers + deliveries créées
[ ] 22 customers, 23 deliveries, ingestion idempotente
[ ] model.joblib présent
[ ] pytest : tests au vert
[ ] ARCHITECTURE.md présent
```

---

## Pourquoi `delivery_minutes` est exclu (point d'oral)

La durée réelle d'une livraison n'est connue qu'**après** la livraison.
Si on l'utilise pour prédire le retard, le modèle « triche » : il utilise une
information qu'on n'aurait pas au moment de décider. C'est une **fuite de données**.

---

## Erreurs fréquentes du challenge

| Symptôme | Réflexe |
|---|---|
| port DB occupé | changer `DB_PORT` dans `.env` |
| `Access denied` | aligner user/password/port entre `.env` et compose |
| `ModuleNotFoundError: src` | lancer depuis la racine avec `python -m src.xxx` |
| `FileNotFoundError` | chemins `Path(__file__)`, pas relatifs au cwd |
| `pytest` ne trouve pas `src` | ajouter `conftest.py` à la racine |
| temps dépassé | STOP → post-mortem (`POST_MORTEM_TEMPLATE.md`) |

---

## Après le challenge

1. Remplir `POST_MORTEM_TEMPLATE.md`.
2. Comparer ton rendu à `../../exam/correction/green_delivery/`.
3. Utiliser le kit de simulation : `../../simulation/README.md`.
