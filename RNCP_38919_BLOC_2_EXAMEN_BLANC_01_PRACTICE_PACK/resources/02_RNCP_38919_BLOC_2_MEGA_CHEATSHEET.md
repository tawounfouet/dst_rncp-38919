# 02 — RNCP 38919 — Bloc 2
# Mega Cheatsheet

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Durée officielle :** 4 heures  
**Support complémentaire :** ORM — 120 min

**Sources :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`
- `Consignes surveillance évaluation.pdf`

> Cette cheatsheet condense les notions visibles dans les supports.  
> Les exemples de code servent de **réflexes de révision** ; ils ne constituent pas des consignes supplémentaires de DataScientest.

---

# 1. Chaîne complète à mémoriser

```text
JSON
 ↓
Jupyter
 ↓
pandas
 ↓
Nettoyage
 ↓
Modélisation relationnelle
 ↓
SQLAlchemy ORM
 ↓
Base SQL sous Docker
 ↓
Ingestion
 ↓
scikit-learn
 ↓
Évaluation
 ↓
joblib
 ↓
docker-compose
 ↓
Tests
 ↓
Documentation
 ↓
ZIP
```

---

# 2. Exam setup

```text
Durée : 4 h
Plateforme : Learn + Mereos
Navigateur : Chrome
Second écran : interdit
Caméra : requise
Micro : requis
Localisation : requise
Pauses : autorisées
Chronomètre : ne s’arrête pas
```

Checklist immédiate :

```text
[ ] ID prête
[ ] caméra OK
[ ] micro OK
[ ] Chrome OK
[ ] Mereos installé
[ ] environnement propre
[ ] eau / pause préparées
```

---

# 3. Jupyter / JSON

## Charger

```python
import pandas as pd

df = pd.read_json("data.json")
```

## Inspecter

```python
df.head()
df.tail()
df.shape
df.columns
df.info()
df.describe(include="all")
```

## Nulls

```python
df.isna().sum()
```

## Doublons

```python
df.duplicated().sum()
```

## Cardinalité

```python
df.nunique()
```

Réflexe :

```text
shape
columns
types
nulls
duplicates
target
```

---

# 4. pandas — opérations essentielles

## Sélection

```python
df["col"]
df[["a", "b"]]
```

## Filtre

```python
df[df["age"] > 18]
df[df["status"] == "active"]
```

## Tri

```python
df.sort_values("score")
df.sort_values("score", ascending=False)
```

## Renommage

```python
df = df.rename(columns={"old": "new"})
```

## Types

```python
df["age"] = pd.to_numeric(df["age"], errors="coerce")
```

## Dates

```python
df["date"] = pd.to_datetime(df["date"], errors="coerce")
```

## Valeurs manquantes

```python
df.dropna()
df.fillna(0)
df["age"] = df["age"].fillna(df["age"].median())
```

## Doublons

```python
df.drop_duplicates()
df.drop_duplicates(subset=["id"])
```

## GroupBy

```python
df.groupby("category")["value"].mean()
df.groupby("category").size()
```

## Export

```python
df.to_csv("output.csv", index=False)
```

---

# 5. matplotlib — minimum utile

```python
import matplotlib.pyplot as plt
```

## Histogramme

```python
df["value"].hist()
plt.show()
```

## Bar chart

```python
df["category"].value_counts().plot(kind="bar")
plt.show()
```

---

# 6. Structure Python minimale

```python
def extract(path):
    return pd.read_json(path)


def transform(df):
    return df


def load(df):
    ...


def main():
    df = extract("data.json")
    df = transform(df)
    load(df)


if __name__ == "__main__":
    main()
```

Règle :

```text
extract
transform
load
```

---

# 7. Variables d’environnement

## `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app
DB_USER=app
DB_PASSWORD=secret
```

## Python

```python
import os

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
```

Réflexe :

```text
Code ≠ Config ≠ Secrets
```

---

# 8. Docker — commandes réflexes

```bash
docker ps
docker ps -a
docker images
docker logs <container>
docker stop <container>
docker rm <container>
docker exec -it <container> bash
```

---

# 9. Docker Compose — commandes réflexes

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose logs -f
docker compose down
```

Avec reconstruction :

```bash
docker compose up -d --build
```

---

# 10. Docker Compose — squelette

```yaml
services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

Concepts :

```text
services
image
environment
ports
volumes
depends_on
```

---

# 11. Modélisation relationnelle

Toujours répondre :

```text
Quel est le grain ?
Quelle est la PK ?
Quelles sont les FK ?
Relation 1-1 ?
Relation 1-N ?
Relation N-N ?
```

Exemple :

```text
User
  1
  │
  N
Address
```

---

# 12. SQLAlchemy — imports

```python
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
)
```

---

# 13. SQLAlchemy — connexion

Le support ORM montre une connexion PostgreSQL via SQLAlchemy.

Pattern :

```python
DATABASE_URL = (
    "postgresql+psycopg://"
    "user:password@host:5432/database"
)

engine = create_engine(DATABASE_URL)
```

---

# 14. SQLAlchemy — Base

```python
Base = declarative_base()
```

---

# 15. SQLAlchemy — modèle simple

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
```

Mapping mental :

```text
Class Python
↔
Table SQL
```

---

# 16. SQLAlchemy — création tables

```python
Base.metadata.create_all(engine)
```

Le support ORM présente également la suppression via :

```python
Base.metadata.drop_all(engine)
```

---

# 17. SQLAlchemy — session

```python
Session = sessionmaker(bind=engine)
session = Session()
```

---

# 18. SQLAlchemy — insert

```python
user = User(name="Alice")

session.add(user)
session.commit()
```

---

# 19. SQLAlchemy — query

```python
users = session.query(User).all()
```

## Filter

```python
user = session.query(User).filter_by(id=1).all()
```

---

# 20. SQLAlchemy — relation

```python
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    email = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship("User")
```

À retenir :

```text
ForeignKey
=
contrainte DB

relationship
=
relation côté ORM
```

---

# 21. SQLAlchemy — pattern complet

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine(DATABASE_URL)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    email = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship("User")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

user = User(name="Alice")
session.add(user)
session.commit()
```

---

# 22. Ingestion — pattern

```python
def ingest(df, session):
    for _, row in df.iterrows():
        obj = User(
            name=row["name"]
        )
        session.add(obj)

    session.commit()
```

Réflexes :

```text
transaction
PK
FK
duplicates
schema
errors
```

---

# 23. Machine Learning — squelette

Le support annonce l’utilisation de `scikit-learn`.

## Split

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)
```

## Train

```python
model.fit(X_train, y_train)
```

## Predict

```python
pred = model.predict(X_test)
```

---

# 24. Machine Learning — préparation catégorielle

Le support annonce la gestion des colonnes catégorielles.

Réflexe simple possible :

```python
X = pd.get_dummies(X, drop_first=True)
```

> Le support fourni n’impose pas cette méthode en particulier.

---

# 25. joblib

## Sauvegarde

```python
import joblib

joblib.dump(model, "model.joblib")
```

## Chargement

```python
model = joblib.load("model.joblib")
```

---

# 26. Tests — 3 axes annoncés

Le support de préparation cite :

```text
1. gestion des erreurs
2. détection de doublons
3. conformité au schéma
```

Réflexe :

```text
happy path
invalid input
duplicate
missing column
wrong type
```

---

# 27. pytest — squelette de révision

```python
def test_valid_ingestion():
    ...
```

```python
def test_duplicate_is_detected():
    ...
```

```python
def test_missing_required_column():
    ...
```

---

# 28. Vérification de schéma

Réflexe possible :

```python
required = {"id", "name"}

missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing columns: {missing}")
```

---

# 29. Détection de doublons

```python
duplicates = df[df.duplicated(subset=["id"], keep=False)]
```

Ou :

```python
if df["id"].duplicated().any():
    raise ValueError("Duplicate id detected")
```

---

# 30. Gestion d’erreur Python

```python
try:
    ...
except Exception as exc:
    print(exc)
    raise
```

Réflexe :

```text
erreur visible
≠
erreur silencieuse
```

---

# 31. Impact écologique

Le support demande une estimation de l’impact écologique.

Points à commenter rapidement :

```text
durée d’exécution
CPU
RAM
stockage
services actifs
conteneurs inutiles
volume traité
```

Ne pas inventer une formule officielle si le sujet n’en fournit pas.

---

# 32. Livrables attendus

Checklist source :

```text
[ ] notebook exploration
[ ] script extraction / transformation
[ ] script création DB via ORM
[ ] script ingestion
[ ] script entraînement ML
[ ] fichier synthétique
```

Le fichier synthétique doit notamment couvrir :

```text
architecture
choix techniques
pistes d’amélioration
```

---

# 33. Structure projet — réflexe de révision

```text
project/
│
├── notebooks/
│   └── exploration.ipynb
│
├── src/
│   ├── transform.py
│   ├── database.py
│   ├── ingest.py
│   └── train_model.py
│
├── tests/
│   └── test_ingestion.py
│
├── models/
│   └── model.joblib
│
├── data/
│
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md
```

> Exemple d’organisation de révision, pas structure obligatoire du sujet officiel.

---

# 34. Requirements — réflexe

```text
pandas
matplotlib
sqlalchemy
psycopg
scikit-learn
joblib
pytest
```

À adapter au sujet réel.

---

# 35. Commandes environnement Python

```bash
python -m venv .venv
```

Linux / macOS :

```bash
source .venv/bin/activate
```

Windows :

```powershell
.venv\Scripts\activate
```

Installation :

```bash
pip install -r requirements.txt
```

---

# 36. Debug rapide Docker

Si ça ne marche pas :

```text
1. docker compose ps
2. docker compose logs
3. vérifier ports
4. vérifier variables env
5. vérifier hostname
6. vérifier credentials
7. vérifier volume
```

---

# 37. Debug rapide SQLAlchemy

Checklist :

```text
DATABASE_URL correcte ?
driver installé ?
DB démarrée ?
host correct ?
port correct ?
database existe ?
credentials corrects ?
tables créées ?
session commit ?
```

---

# 38. Debug rapide pandas

Checklist :

```text
fichier existe ?
JSON valide ?
colonnes attendues ?
types corrects ?
nulls ?
doublons ?
```

---

# 39. Debug rapide ML

Checklist :

```text
target présente ?
X sans target ?
NaN ?
catégories encodées ?
mêmes colonnes train/test ?
fit appelé ?
métrique adaptée ?
```

---

# 40. Stratégie 4 h — rappel ultra-court

Réflexe de préparation :

```text
00:00–00:15  lire / organiser
00:15–00:45  exploration
00:45–01:20  ETL Python
01:20–02:00  DB + ORM
02:00–02:30  ingestion
02:30–03:00  ML
03:00–03:25  Compose
03:25–03:40  tests
03:40–03:55  doc
03:55–04:00  ZIP / upload
```

> Cette répartition est une stratégie de préparation, pas un découpage officiel.

---

# 41. Les 10 réflexes absolus

```text
1. Lire avant de coder
2. Identifier les livrables
3. Commencer simple
4. Garder du code exécutable
5. Vérifier PK / FK
6. Commit DB explicitement
7. Tester tôt
8. Ne pas surcomplexifier le ML
9. Documenter avant la dernière minute
10. Garder 5 min pour le ZIP
```

---

# 42. 30 secondes avant de rendre

```text
[ ] tous les fichiers présents
[ ] notebook lisible
[ ] scripts présents
[ ] DB / ORM présent
[ ] ingestion présente
[ ] ML présent
[ ] modèle sauvegardé si demandé
[ ] documentation présente
[ ] archive créée
[ ] archive vérifiée
[ ] upload terminé
```

---

# 43. One-liner final

```text
JSON
→ pandas
→ ORM
→ SQL
→ ML
→ joblib
→ Docker
→ tests
→ docs
→ ZIP
```

---

# 44. Document suivant

```text
03_RNCP_38919_BLOC_2_ETL_PYTHON_GUIDE.md
```

Objectif :

> approfondir uniquement la partie `JSON → Jupyter → pandas → nettoyage → scripts ETL`, avec exercices et patterns réutilisables.
