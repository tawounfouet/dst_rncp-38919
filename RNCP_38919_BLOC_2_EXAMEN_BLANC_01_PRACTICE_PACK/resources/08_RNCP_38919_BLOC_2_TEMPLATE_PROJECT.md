# 08 — RNCP 38919 — Bloc 2
# Template Project — ETL + ORM + Docker + ML + Tests

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Durée officielle :** 4 heures

**Sources de cadrage :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`
- `Consignes surveillance évaluation.pdf`

> **Important**
>
> Ce document est un **template de préparation** construit à partir des livrables et technologies annoncés dans les supports.
>
> Il ne constitue pas une arborescence officielle imposée par DataScientest.
>
> Les supports fournis demandent notamment :
>
> ```text
> notebook d’exploration
> script extraction / transformation
> script création de base via ORM
> script ingestion
> script entraînement ML
> fichier synthétique
> Docker / docker-compose
> variables d’environnement
> tests d’ingestion
> ```
>
> Le jour de l’examen, **le sujet réel reste prioritaire** sur ce template.

---

# 1. Objectif

Le but du template est de disposer d’un modèle mental stable pour assembler rapidement :

```text
JSON
  ↓
Jupyter
  ↓
ETL Python / pandas
  ↓
SQLAlchemy ORM
  ↓
Base relationnelle Docker
  ↓
Ingestion
  ↓
Machine Learning
  ↓
joblib
  ↓
Tests
  ↓
Documentation
  ↓
Archive finale
```

---

# 2. Arborescence proposée

```text
rncp38919_bloc2/
│
├── data/
│   ├── raw/
│   │   └── data.json
│   └── processed/
│       └── data.csv
│
├── notebooks/
│   └── 01_exploration.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── etl.py
│   ├── database.py
│   ├── models.py
│   ├── ingest.py
│   └── train_model.py
│
├── models/
│   └── model.joblib
│
├── tests/
│   ├── test_etl.py
│   ├── test_schema.py
│   └── test_ingestion.py
│
├── Dockerfile
├── docker-compose.yml
├── .env
├── .env.example
├── requirements.txt
├── README.md
└── ARCHITECTURE.md
```

---

# 3. Correspondance avec les livrables annoncés

| Livrable annoncé | Fichier du template |
|---|---|
| Notebook d’exploration | `notebooks/01_exploration.ipynb` |
| Extraction / transformation | `src/etl.py` |
| Création DB via ORM | `src/models.py` + `src/database.py` |
| Ingestion | `src/ingest.py` |
| Entraînement ML | `src/train_model.py` |
| Sauvegarde du modèle | `models/model.joblib` |
| Tests | `tests/` |
| Fichier synthétique | `ARCHITECTURE.md` / `README.md` |
| Docker / Compose | `Dockerfile` + `docker-compose.yml` |

---

# 4. Ordre recommandé de construction

```text
1. notebook
2. ETL
3. config
4. database
5. models ORM
6. ingestion
7. ML
8. tests
9. documentation
10. archive
```

Le template doit rester :

```text
simple
lisible
exécutable
facile à diagnostiquer
```

---

# 5. `requirements.txt`

## Template proposé

```text
pandas
matplotlib
sqlalchemy
psycopg[binary]
scikit-learn
joblib
pytest
```

> À adapter au moteur de base et aux bibliothèques réellement demandées.

---

# 6. `.env.example`

## Template proposé

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dst_db
DB_USER=daniel
DB_PASSWORD=datascientest

PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin
```

---

# 7. `.env`

Le fichier `.env` reprend les valeurs de configuration réelles.

Réflexe :

```text
.env.example
→ versionnable

.env
→ configuration locale / secrets
```

---

# 8. `src/config.py`

## Template proposé

```python
import os


DB_HOST = os.getenv(
    "DB_HOST",
    "localhost",
)

DB_PORT = os.getenv(
    "DB_PORT",
    "5432",
)

DB_NAME = os.getenv(
    "DB_NAME",
    "dst_db",
)

DB_USER = os.getenv(
    "DB_USER",
    "daniel",
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    "datascientest",
)


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
```

---

# 9. `src/etl.py`

## Template proposé

```python
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "id",
    "name",
    "category",
}


def extract(
    path: str | Path,
) -> pd.DataFrame:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            path
        )

    return pd.read_json(
        path
    )


def validate_schema(
    df: pd.DataFrame,
) -> None:
    missing = (
        REQUIRED_COLUMNS
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            f"Missing columns: "
            f"{sorted(missing)}"
        )

    if df["id"].isna().any():
        raise ValueError(
            "Null id detected"
        )

    if df["id"].duplicated().any():
        raise ValueError(
            "Duplicate id detected"
        )


def transform(
    df: pd.DataFrame,
) -> pd.DataFrame:
    validate_schema(df)

    result = df.copy()

    result["name"] = (
        result["name"]
        .astype("string")
        .str.strip()
    )

    result["category"] = (
        result["category"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    return result


def save_processed(
    df: pd.DataFrame,
    path: str | Path,
) -> None:
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        path,
        index=False,
    )
```

---

# 10. `src/database.py`

## Template proposé

```python
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)

from .config import (
    DATABASE_URL,
)


engine = create_engine(
    DATABASE_URL
)


Session = sessionmaker(
    bind=engine
)
```

---

# 11. `src/models.py`

## Template aligné sur le support ORM

```python
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    declarative_base,
    relationship,
)


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String
    )


class Address(Base):
    __tablename__ = "addresses"

    id = Column(
        Integer,
        primary_key=True,
    )

    email = Column(
        String
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id"
        ),
    )

    user = relationship(
        "User"
    )
```

---

# 12. Création des tables

## Template proposé

Dans un script ou au démarrage :

```python
from .database import (
    engine,
)

from .models import (
    Base,
)


Base.metadata.create_all(
    engine,
    checkfirst=True,
)
```

---

# 13. `src/ingest.py`

## Template proposé

```python
import pandas as pd

from .database import (
    Session,
    engine,
)

from .models import (
    Base,
    User,
)


def ingest_users(
    df: pd.DataFrame,
) -> None:
    Base.metadata.create_all(
        engine,
        checkfirst=True,
    )

    session = Session()

    try:
        for _, row in df.iterrows():
            user = User(
                id=int(row["id"]),
                name=str(row["name"]),
            )

            session.add(user)

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()
```

---

# 14. Pourquoi `rollback()` dans le template

Le support ORM montre surtout :

```text
add
commit
query
```

Le `rollback()` ci-dessus est un ajout de robustesse pour l’entraînement.

Il permet de conserver un état transactionnel propre en cas d’échec.

---

# 15. `src/train_model.py`

## Template proposé

Le support n’impose pas un algorithme précis.

Exemple de classification simple :

```python
from pathlib import Path

import joblib
import pandas as pd

from sklearn.linear_model import (
    LogisticRegression,
)
from sklearn.metrics import (
    accuracy_score,
)
from sklearn.model_selection import (
    train_test_split,
)


def prepare_features(
    df: pd.DataFrame,
):
    X = df.drop(
        columns=["target"]
    )

    y = df["target"]

    X = pd.get_dummies(
        X,
        drop_first=True,
    )

    return X, y


def main() -> None:
    df = pd.read_csv(
        "data/processed/data.csv"
    )

    X, y = prepare_features(df)

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = LogisticRegression(
        max_iter=1000,
    )

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_test
    )

    score = accuracy_score(
        y_test,
        predictions,
    )

    print(
        f"Accuracy: {score:.4f}"
    )

    model_dir = Path(
        "models"
    )

    model_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        model_dir / "model.joblib",
    )


if __name__ == "__main__":
    main()
```

---

# 16. Adapter le ML au sujet réel

Le jour J :

```text
classification ?
régression ?
```

Puis adapter :

```text
target
features
modèle
métrique
```

Ne pas conserver automatiquement :

```text
LogisticRegression
+
accuracy
```

si le problème ne correspond pas.

---

# 17. `tests/test_schema.py`

## Template proposé

```python
import pandas as pd
import pytest

from src.etl import (
    validate_schema,
)


def test_valid_schema():
    df = pd.DataFrame(
        {
            "id": [1],
            "name": ["Alice"],
            "category": ["a"],
        }
    )

    validate_schema(df)


def test_missing_column():
    df = pd.DataFrame(
        {
            "id": [1],
            "name": ["Alice"],
        }
    )

    with pytest.raises(
        ValueError
    ):
        validate_schema(df)


def test_duplicate_id():
    df = pd.DataFrame(
        {
            "id": [1, 1],
            "name": [
                "Alice",
                "Alice",
            ],
            "category": [
                "a",
                "a",
            ],
        }
    )

    with pytest.raises(
        ValueError
    ):
        validate_schema(df)
```

---

# 18. `tests/test_etl.py`

## Template proposé

```python
import pandas as pd

from src.etl import (
    transform,
)


def test_category_is_normalized():
    df = pd.DataFrame(
        {
            "id": [1],
            "name": [" Alice "],
            "category": [" A "],
        }
    )

    result = transform(df)

    assert (
        result.loc[
            0,
            "category",
        ]
        == "a"
    )
```

---

# 19. `tests/test_ingestion.py`

## Template conceptuel

```python
def test_valid_ingestion():
    ...
```

```python
def test_duplicate_is_not_inserted():
    ...
```

```python
def test_invalid_schema_is_rejected():
    ...
```

La mise en œuvre exacte dépend de la base et de la stratégie retenue.

---

# 20. `docker-compose.yml`

## Profil PostgreSQL + pgAdmin

Ce profil est cohérent avec le support ORM.

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "${DB_PORT}:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD}
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  db_data:
```

---

# 21. Attention au support principal

Le support principal mentionne :

```text
phpMyAdmin
```

alors que le support ORM montre :

```text
PostgreSQL + pgAdmin
```

Le template retient ici PostgreSQL + pgAdmin car la ressource ORM est explicitement construite dessus.

Mais :

> si le sujet réel impose MySQL / MariaDB + phpMyAdmin, il faut adapter la stack et le driver.

---

# 22. `Dockerfile`

## Template proposé

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY . .

CMD [
    "python",
    "src/ingest.py"
]
```

---

# 23. Pourquoi garder un Dockerfile simple

Dans une épreuve de 4 heures :

```text
lisibilité
>
optimisation avancée
```

Objectif :

```text
build
run
debug
```

---

# 24. `README.md` — squelette

```markdown
# RNCP 38919 — Bloc 2

## Objectif

Mini-projet ETL + base relationnelle + ML.

## Architecture

JSON
→ pandas
→ SQLAlchemy
→ PostgreSQL
→ scikit-learn

## Démarrage

```bash
docker compose up -d
```

## ETL

```bash
python ...
```

## Tests

```bash
pytest -v
```

## Machine Learning

```bash
python src/train_model.py
```
```

---

# 25. `ARCHITECTURE.md` — squelette

Le support demande un fichier synthétique couvrant notamment :

```text
architecture
choix techniques
pistes d’amélioration
```

Structure proposée :

```text
# Architecture

## 1. Contexte
## 2. Données sources
## 3. Pipeline ETL
## 4. Modèle relationnel
## 5. Docker / Compose
## 6. Machine Learning
## 7. Tests
## 8. Choix techniques
## 9. Limites
## 10. Pistes d’amélioration
## 11. Impact écologique
```

---

# 26. Diagramme ASCII pour `ARCHITECTURE.md`

```text
data.json
   │
   ▼
Jupyter
   │
   ▼
pandas ETL
   │
   ▼
processed.csv
   │
   ├───────────────┐
   │               │
   ▼               ▼
SQLAlchemy        ML
   │               │
   ▼               ▼
PostgreSQL      joblib
   │
   ▼
Tests / validation
```

---

# 27. `notebooks/01_exploration.ipynb`

## Squelette de sections

```text
1. Imports
2. Chargement JSON
3. Shape
4. Colonnes
5. Types
6. Nulls
7. Doublons
8. Catégories
9. Visualisations
10. Décisions de nettoyage
11. Conclusion
```

---

# 28. Cellule d’audit rapide

```python
audit = pd.DataFrame(
    {
        "dtype": (
            df.dtypes.astype(str)
        ),
        "nulls": (
            df.isna().sum()
        ),
        "null_rate": (
            df.isna().mean()
        ),
        "unique": (
            df.nunique()
        ),
    }
)

audit
```

---

# 29. Script d’orchestration optionnel

## Template proposé

Un script léger peut chaîner :

```text
extract
transform
save
ingest
```

Exemple :

```python
from src.etl import (
    extract,
    transform,
    save_processed,
)


def main():
    df = extract(
        "data/raw/data.json"
    )

    df = transform(df)

    save_processed(
        df,
        "data/processed/data.csv",
    )


if __name__ == "__main__":
    main()
```

---

# 30. Ce qu’il ne faut pas faire avec ce template

Ne pas arriver à l’examen en pensant :

```text
je vais recopier exactement
cette structure
quoi qu’il arrive
```

Le template sert à :

```text
réduire le temps de réflexion
```

pas à :

```text
ignorer les consignes du sujet
```

---

# 31. Niveau de personnalisation attendu

Dès lecture du sujet :

```text
Template
   ↓
Adapter :
- noms de colonnes
- entités
- PK / FK
- target
- modèle
- métrique
- moteur DB
- stack Docker
```

---

# 32. Les points à remplacer immédiatement

```text
REQUIRED_COLUMNS
target
User
Address
DATABASE_URL
nom de table
variables env
modèle ML
métrique
```

---

# 33. Ordre d’exécution local

## Template proposé

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

Puis :

```bash
pip install -r requirements.txt
```

Ensuite :

```bash
docker compose up -d
```

Puis :

```bash
pytest -v
```

Puis :

```bash
python src/train_model.py
```

---

# 34. Smoke test global

Avant de considérer le projet prêt :

```text
[ ] Docker UP
[ ] DB accessible
[ ] ETL exécutable
[ ] tables créées
[ ] ingestion OK
[ ] ML entraîné
[ ] model.joblib présent
[ ] tests verts
[ ] documentation présente
```

---

# 35. Commandes de diagnostic

```bash
docker compose ps
```

```bash
docker compose logs db
```

```bash
pytest -v
```

```bash
python src/train_model.py
```

---

# 36. Flow end-to-end

```text
RAW JSON
   │
   ▼
extract()
   │
   ▼
validate_schema()
   │
   ▼
transform()
   │
   ▼
processed.csv
   │
   ├─────────────┐
   │             │
   ▼             ▼
ingest()      ML train
   │             │
   ▼             ▼
PostgreSQL   model.joblib
   │
   ▼
tests
```

---

# 37. Definition of Done — ETL

```text
[ ] JSON lu
[ ] schéma validé
[ ] nulls gérés
[ ] doublons contrôlés
[ ] catégories normalisées
[ ] output généré
```

---

# 38. Definition of Done — ORM

```text
[ ] engine créé
[ ] Base créée
[ ] modèles définis
[ ] PK définies
[ ] FK définies
[ ] create_all exécuté
[ ] session fonctionnelle
[ ] insert OK
[ ] query OK
```

---

# 39. Definition of Done — Docker

```text
[ ] compose valide
[ ] DB UP
[ ] ports corrects
[ ] env vars correctes
[ ] volume présent
[ ] admin UI accessible si nécessaire
```

---

# 40. Definition of Done — ML

```text
[ ] target définie
[ ] X défini
[ ] split réalisé
[ ] fit OK
[ ] predict OK
[ ] métrique calculée
[ ] modèle sauvegardé
```

---

# 41. Definition of Done — Tests

```text
[ ] happy path
[ ] erreur
[ ] doublon
[ ] schéma
```

---

# 42. Definition of Done — Documentation

```text
[ ] architecture
[ ] choix techniques
[ ] résultat ML
[ ] limites
[ ] pistes d’amélioration
[ ] impact écologique
```

---

# 43. Minimum viable project

Si le temps devient critique :

```text
notebook
+
etl.py
+
models.py
+
ingest.py
+
train_model.py
+
docker-compose.yml
+
tests minimum
+
ARCHITECTURE.md
```

Priorité :

```text
fonctionnel
>
parfait
```

---

# 44. Ce qu’il faut éviter

```text
framework maison complexe
architecture DDD
multiples couches inutiles
CI/CD non demandée
microservices
abstractions prématurées
```

Le Bloc 2 demande d’abord un mini-projet complet.

---

# 45. Variante MySQL / phpMyAdmin

## À utiliser uniquement si le sujet réel l’impose

Exemple conceptuel :

```yaml
services:
  db:
    image: mysql
    ...

  phpmyadmin:
    image: phpmyadmin
    ...
```

Puis le driver SQLAlchemy devra être adapté.

Ce template principal ne développe pas davantage cette variante car le support ORM fourni travaille explicitement avec PostgreSQL + pgAdmin.

---

# 46. Réflexe de migration du template

```text
Sujet reçu
   ↓
Identifier stack
   ↓
Copier structure mentale
   ↓
Renommer entités
   ↓
Adapter colonnes
   ↓
Adapter DB
   ↓
Adapter ML
   ↓
Tester
```

---

# 47. Checklist avant simulation 4 h

```text
[ ] je peux recréer l’arborescence rapidement
[ ] je peux écrire un ETL minimal
[ ] je peux écrire les modèles ORM
[ ] je peux démarrer Compose
[ ] je peux ingérer
[ ] je peux entraîner un modèle
[ ] je peux sauvegarder avec joblib
[ ] je peux écrire 3–4 tests
[ ] je peux documenter
```

---

# 48. Exercice de mémorisation

Sans regarder ce document, recréer :

```text
data/
notebooks/
src/
models/
tests/
docker-compose.yml
.env
requirements.txt
README.md
ARCHITECTURE.md
```

Puis remplir :

```text
etl.py
models.py
database.py
ingest.py
train_model.py
```

---

# 49. Template mental ultra-court

```text
EXPLORE
  ↓
ETL
  ↓
MODEL DB
  ↓
INGEST
  ↓
TRAIN
  ↓
TEST
  ↓
DOCUMENT
  ↓
ZIP
```

---

# 50. Document suivant

```text
09_RNCP_38919_BLOC_2_STRATEGIE_EXAMEN_4H.md
```

Objectif :

> transformer ce template technique en plan d’exécution chronométré :
> quoi faire dans les 15 premières minutes, quand changer de tâche,
> quels livrables prioriser et quand arrêter de coder pour sécuriser le rendu.
