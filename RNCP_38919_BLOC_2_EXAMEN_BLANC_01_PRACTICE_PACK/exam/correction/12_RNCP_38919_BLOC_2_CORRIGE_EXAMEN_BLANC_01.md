# 12 — RNCP 38919 — Bloc 2
# Corrigé de l’Examen blanc 01 — Projet ETL & ML

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Document corrigé :** `11_RNCP_38919_BLOC_2_EXAMEN_BLANC_01.md`  
**Durée de référence :** 4 heures

**Sources de cadrage :**
- `Examen_Bloc_2_RNCP_Data_Engineer_Projet_ETL_ML.md`
- `Examen RNCP 38919 _ Bloc 2 - ORM.pdf`
- `Consignes surveillance évaluation.pdf`

> **Nature de ce document**
>
> Ce corrigé porte sur **l’examen blanc créé dans le document 11**.
> Il ne constitue pas un corrigé officiel DataScientest et ne révèle pas le contenu de l’épreuve réelle.
>
> Le support officiel de préparation annonce le périmètre :
>
> ```text
> JSON / Jupyter
> Python structuré
> pandas / matplotlib
> valeurs manquantes
> catégories
> base relationnelle / Docker
> variables d’environnement
> PK / FK
> SQLAlchemy / ORM
> scikit-learn
> joblib
> docker-compose
> tests d’ingestion
> impact écologique
> ```
>
> Les choix techniques proposés ci-dessous sont **une solution de référence possible**.
> D’autres solutions peuvent être correctes si elles satisfont le besoin et sont justifiées.

---

# 1. Résultat attendu en une vue

Une solution complète peut suivre ce flux :

```text
deliveries.json
      │
      ▼
Jupyter
      │
      ▼
Exploration
      │
      ▼
ETL pandas
      │
      ▼
deliveries_clean.csv
      │
      ├───────────────────────┐
      │                       │
      ▼                       ▼
SQLAlchemy ORM           scikit-learn
      │                       │
      ▼                       ▼
MariaDB / MySQL           Pipeline ML
      │                       │
      ▼                       ▼
phpMyAdmin             model.joblib
      │
      ▼
Tests d’ingestion
      │
      ▼
Documentation / ZIP
```

---

# 2. Résultats factuels du dataset blanc

Sur le dataset fourni dans le document 11 :

```text
Lignes brutes                  : 24
Colonnes                       : 9
Doublons complets              : 1
delivery_id dupliqué           : 1
Valeurs nulles distance_km     : 1
Valeurs nulles traffic_level   : 1
Valeurs nulles weather         : 1
```

Le doublon concerne :

```text
delivery_id = 1020
```

Après suppression du doublon sur `delivery_id` :

```text
Livraisons                     : 23
Clients uniques                : 22
late_delivery = 0              : 13
late_delivery = 1              : 10
```

Distribution :

```text
0 → 56,5 %
1 → 43,5 %
```

Le dataset n’est donc pas extrêmement déséquilibré, mais il est **très petit**.

---

# 3. Exploration — ce qu’il fallait observer

## Grain

Le grain est :

```text
une ligne
=
une livraison
```

La clé métier naturelle proposée dans le sujet est :

```text
delivery_id
```

---

# 4. Valeurs manquantes

Résultat attendu :

```text
distance_km     → 1 valeur manquante
traffic_level   → 1 valeur manquante
weather         → 1 valeur manquante
```

Les autres colonnes ne contiennent pas de valeur manquante dans le dataset fourni.

Code :

```python
df.isna().sum()
```

---

# 5. Doublons

Code :

```python
df.duplicated().sum()
```

Résultat :

```text
1
```

Puis :

```python
df["delivery_id"].duplicated().sum()
```

Résultat :

```text
1
```

Une solution correcte doit donc :

```text
détecter
puis
traiter explicitement
```

ce doublon.

---

# 6. Normalisation de `customer_city`

Avant normalisation, Paris apparaît notamment sous :

```text
Paris
PARIS
 Paris 
```

Une transformation simple :

```python
df["customer_city"] = (
    df["customer_city"]
    .astype("string")
    .str.strip()
    .str.lower()
)
```

Après normalisation et déduplication :

```text
paris                 : 8
poissy                : 5
nanterre              : 4
versailles            : 3
boulogne-billancourt  : 3
```

---

# 7. Choix de nettoyage de référence

Une correction possible est :

```text
delivery_id dupliqué
→ conserver la première occurrence

distance_km manquant
→ médiane

traffic_level manquant
→ "unknown"

weather manquant
→ "unknown"

customer_city
→ strip + lower
```

La médiane de `distance_km`, après déduplication et avant imputation, vaut :

```text
8.45 km
```

Ces choix ne sont pas uniques.

Ce qui compte dans le cadre de l’exercice est :

```text
décision explicite
+
code reproductible
+
justification
```

---

# 8. Notebook d’exploration — correction minimale

```python
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_json(
    "data/raw/deliveries.json"
)


display(df.head())

print(
    "shape:",
    df.shape,
)

print(
    "columns:",
    df.columns.tolist(),
)

df.info()

display(
    df.isna().sum()
)

print(
    "full duplicates:",
    df.duplicated().sum(),
)

print(
    "delivery_id duplicates:",
    df["delivery_id"]
    .duplicated()
    .sum(),
)

display(
    df["late_delivery"]
    .value_counts(
        normalize=True
    )
)
```

---

# 9. Visualisations de référence

## Target

```python
df["late_delivery"].value_counts().sort_index().plot(
    kind="bar"
)

plt.title(
    "Distribution de late_delivery"
)

plt.xlabel(
    "Late delivery"
)

plt.ylabel(
    "Count"
)

plt.show()
```

## Distance

```python
df["distance_km"].hist(
    bins=8
)

plt.title(
    "Distribution de distance_km"
)

plt.xlabel(
    "Distance (km)"
)

plt.show()
```

---

# 10. `src/etl.py` — correction de référence

```python
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "delivery_id",
    "customer_id",
    "customer_city",
    "vehicle_type",
    "distance_km",
    "traffic_level",
    "weather",
    "delivery_minutes",
    "late_delivery",
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


def transform(
    df: pd.DataFrame,
) -> pd.DataFrame:
    validate_schema(df)

    result = df.copy()

    result = (
        result
        .drop_duplicates(
            subset=["delivery_id"],
            keep="first",
        )
        .copy()
    )

    result["customer_city"] = (
        result["customer_city"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    result["vehicle_type"] = (
        result["vehicle_type"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    result["traffic_level"] = (
        result["traffic_level"]
        .astype("string")
        .str.strip()
        .str.lower()
        .fillna("unknown")
    )

    result["weather"] = (
        result["weather"]
        .astype("string")
        .str.strip()
        .str.lower()
        .fillna("unknown")
    )

    result["distance_km"] = (
        pd.to_numeric(
            result["distance_km"],
            errors="coerce",
        )
    )

    median_distance = (
        result["distance_km"]
        .median()
    )

    result["distance_km"] = (
        result["distance_km"]
        .fillna(
            median_distance
        )
    )

    numeric_columns = [
        "delivery_id",
        "customer_id",
        "delivery_minutes",
        "late_delivery",
    ]

    for column in numeric_columns:
        result[column] = (
            pd.to_numeric(
                result[column],
                errors="raise",
            )
        )

    if result["delivery_id"].isna().any():
        raise ValueError(
            "Null delivery_id detected"
        )

    if not result["delivery_id"].is_unique:
        raise ValueError(
            "Duplicate delivery_id detected"
        )

    if not result["late_delivery"].isin(
        [0, 1]
    ).all():
        raise ValueError(
            "late_delivery must contain "
            "only 0 or 1"
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


def main() -> None:
    raw_path = Path(
        "data/raw/deliveries.json"
    )

    output_path = Path(
        "data/processed/"
        "deliveries_clean.csv"
    )

    df = extract(
        raw_path
    )

    clean_df = transform(
        df
    )

    save_processed(
        clean_df,
        output_path,
    )

    print(
        f"{len(clean_df)} rows "
        f"written to {output_path}"
    )


if __name__ == "__main__":
    main()
```

---

# 11. Résultat ETL attendu

Avec la correction ci-dessus :

```text
23 lignes
9 colonnes
0 delivery_id dupliqué
0 valeur manquante
```

Le dataset transformé doit donc pouvoir devenir une entrée stable pour :

```text
ORM
ingestion
ML
```

---

# 12. Schéma relationnel — correction

Une modélisation minimale cohérente :

```text
customers
──────────────────────
customer_id      PK
customer_city

          1
          │
          │
          N

deliveries
──────────────────────
delivery_id      PK
customer_id      FK
vehicle_type
distance_km
traffic_level
weather
delivery_minutes
late_delivery
```

---

# 13. Réponses aux questions de modélisation

### 1. Pourquoi `customer_id` comme PK ?

Parce qu’il identifie un client dans le dataset blanc.

### 2. Pourquoi `delivery_id` comme PK ?

Parce que le grain est la livraison et que cet identifiant doit être unique.

### 3. Où placer la FK ?

Dans :

```text
deliveries.customer_id
```

qui référence :

```text
customers.customer_id
```

### 4. Cardinalité

```text
1 Customer
→ N Deliveries
```

### 5. Nullabilité

Après la transformation de référence, les champs conservés sont rendus exploitables sans null pour le pipeline choisi.

---

# 14. Docker — choix de correction

Le sujet blanc demandait volontairement :

```text
MySQL ou MariaDB
+
phpMyAdmin
```

La correction choisit :

```text
MariaDB
+
phpMyAdmin
```

Ce choix est propre au **sujet blanc**.

Le support DataScientest principal mentionne `phpMyAdmin`, tandis que la ressource ORM dédiée utilise PostgreSQL + pgAdmin.

---

# 15. `.env.example`

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=green_delivery
DB_USER=green_user
DB_PASSWORD=green_password

DB_ROOT_PASSWORD=root_password

PMA_PORT=8080
```

---

# 16. `docker-compose.yml`

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
    environment:
      PMA_HOST: db
      PMA_PORT: 3306
    ports:
      - "${PMA_PORT}:80"
    depends_on:
      - db

volumes:
  db_data:
```

Démarrage :

```bash
docker compose up -d
```

Vérification :

```bash
docker compose ps
```

Logs :

```bash
docker compose logs db
```

---

# 17. `requirements.txt`

Correction possible :

```text
pandas
matplotlib
sqlalchemy
pymysql
python-dotenv
scikit-learn
joblib
pytest
```

`PyMySQL` et `python-dotenv` sont ici des choix d’implémentation du corrigé, pas des dépendances imposées dans la page de préparation DataScientest.

---

# 18. `src/config.py`

```python
import os

from dotenv import load_dotenv


load_dotenv()


DB_HOST = os.getenv(
    "DB_HOST",
    "localhost",
)

DB_PORT = os.getenv(
    "DB_PORT",
    "3306",
)

DB_NAME = os.getenv(
    "DB_NAME",
    "green_delivery",
)

DB_USER = os.getenv(
    "DB_USER",
    "green_user",
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    "green_password",
)


DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
```

---

# 19. `src/database.py`

```python
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)

from src.config import (
    DATABASE_URL,
)


engine = create_engine(
    DATABASE_URL,
)


Session = sessionmaker(
    bind=engine,
)
```

---

# 20. `src/models.py`

```python
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    declarative_base,
    relationship,
)


Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(
        Integer,
        primary_key=True,
    )

    customer_city = Column(
        String(100),
        nullable=False,
    )

    deliveries = relationship(
        "Delivery",
        back_populates="customer",
    )


class Delivery(Base):
    __tablename__ = "deliveries"

    delivery_id = Column(
        Integer,
        primary_key=True,
    )

    customer_id = Column(
        Integer,
        ForeignKey(
            "customers.customer_id"
        ),
        nullable=False,
    )

    vehicle_type = Column(
        String(50),
        nullable=False,
    )

    distance_km = Column(
        Float,
        nullable=False,
    )

    traffic_level = Column(
        String(50),
        nullable=False,
    )

    weather = Column(
        String(50),
        nullable=False,
    )

    delivery_minutes = Column(
        Integer,
        nullable=False,
    )

    late_delivery = Column(
        Integer,
        nullable=False,
    )

    customer = relationship(
        "Customer",
        back_populates="deliveries",
    )
```

---

# 21. `src/create_database.py`

```python
from src.database import (
    engine,
)

from src.models import (
    Base,
)


def main() -> None:
    Base.metadata.create_all(
        engine,
        checkfirst=True,
    )

    print(
        "Database tables created"
    )


if __name__ == "__main__":
    main()
```

---

# 22. Test de connexion SQLAlchemy

Une vérification simple :

```python
from sqlalchemy import text

from src.database import engine


with engine.connect() as conn:
    result = conn.execute(
        text("SELECT 1")
    )

    print(
        result.fetchone()
    )
```

Résultat attendu :

```text
(1,)
```

ou équivalent selon le driver.

---

# 23. `src/ingest.py`

Une correction simple et idempotente pour ce petit dataset :

```python
import pandas as pd

from src.database import (
    Session,
)

from src.models import (
    Customer,
    Delivery,
)


def ingest(
    df: pd.DataFrame,
) -> None:
    session = Session()

    try:
        customers = (
            df[
                [
                    "customer_id",
                    "customer_city",
                ]
            ]
            .drop_duplicates(
                subset=[
                    "customer_id"
                ]
            )
        )

        for row in (
            customers
            .to_dict(
                orient="records"
            )
        ):
            exists = (
                session
                .query(Customer)
                .filter_by(
                    customer_id=int(
                        row[
                            "customer_id"
                        ]
                    )
                )
                .first()
            )

            if exists is None:
                session.add(
                    Customer(
                        customer_id=int(
                            row[
                                "customer_id"
                            ]
                        ),
                        customer_city=str(
                            row[
                                "customer_city"
                            ]
                        ),
                    )
                )

        session.commit()

        for row in (
            df.to_dict(
                orient="records"
            )
        ):
            exists = (
                session
                .query(Delivery)
                .filter_by(
                    delivery_id=int(
                        row[
                            "delivery_id"
                        ]
                    )
                )
                .first()
            )

            if exists is not None:
                continue

            session.add(
                Delivery(
                    delivery_id=int(
                        row[
                            "delivery_id"
                        ]
                    ),
                    customer_id=int(
                        row[
                            "customer_id"
                        ]
                    ),
                    vehicle_type=str(
                        row[
                            "vehicle_type"
                        ]
                    ),
                    distance_km=float(
                        row[
                            "distance_km"
                        ]
                    ),
                    traffic_level=str(
                        row[
                            "traffic_level"
                        ]
                    ),
                    weather=str(
                        row[
                            "weather"
                        ]
                    ),
                    delivery_minutes=int(
                        row[
                            "delivery_minutes"
                        ]
                    ),
                    late_delivery=int(
                        row[
                            "late_delivery"
                        ]
                    ),
                )
            )

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def main() -> None:
    df = pd.read_csv(
        "data/processed/"
        "deliveries_clean.csv"
    )

    ingest(df)

    print(
        "Ingestion completed"
    )


if __name__ == "__main__":
    main()
```

---

# 24. Résultat d’ingestion attendu

Après une première ingestion :

```text
customers  → 22 lignes
deliveries → 23 lignes
```

Après une seconde exécution de la fonction de référence :

```text
customers  → toujours 22
deliveries → toujours 23
```

Cette propriété permet de vérifier que l’ingestion de référence n’ajoute pas silencieusement les mêmes IDs une seconde fois.

---

# 25. Machine Learning — hypothèse fonctionnelle

Pour le corrigé, on adopte l’hypothèse suivante :

> la prédiction de retard doit être réalisable **avant la fin de la livraison**.

Par conséquent, la correction exclut :

```text
delivery_minutes
```

des features.

Pourquoi ?

Parce que la durée réellement constatée est potentiellement une information connue seulement après ou pendant la livraison et peut être très directement liée au label de retard.

Cette exclusion est un **choix de modélisation du corrigé**, pas une exigence de la page DataScientest.

---

# 26. Features retenues

```text
customer_city
vehicle_type
distance_km
traffic_level
weather
```

Exclusions :

```text
delivery_id
→ identifiant technique

customer_id
→ identifiant à forte cardinalité
   peu pertinent sur ce minuscule dataset

delivery_minutes
→ risque de fuite d’information
   selon l’hypothèse de prédiction pré-livraison
```

Target :

```text
late_delivery
```

---

# 27. `src/train_model.py` — correction de référence

```python
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import (
    ColumnTransformer,
)

from sklearn.impute import (
    SimpleImputer,
)

from sklearn.linear_model import (
    LogisticRegression,
)

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

from sklearn.model_selection import (
    train_test_split,
)

from sklearn.pipeline import (
    Pipeline,
)

from sklearn.preprocessing import (
    OneHotEncoder,
)


DATA_PATH = (
    "data/processed/"
    "deliveries_clean.csv"
)

MODEL_PATH = (
    "models/model.joblib"
)


NUMERIC_FEATURES = [
    "distance_km",
]

CATEGORICAL_FEATURES = [
    "customer_city",
    "vehicle_type",
    "traffic_level",
    "weather",
]


def main() -> None:
    df = pd.read_csv(
        DATA_PATH
    )

    feature_columns = (
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
    )

    X = df[
        feature_columns
    ]

    y = df[
        "late_delivery"
    ]

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy=(
                        "most_frequent"
                    )
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown=(
                        "ignore"
                    )
                ),
            ),
        ]
    )

    preprocessing = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    model = LogisticRegression(
        max_iter=1000,
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessing",
                preprocessing,
            ),
            (
                "model",
                model,
            ),
        ]
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y,
    )

    pipeline.fit(
        X_train,
        y_train,
    )

    predictions = (
        pipeline.predict(
            X_test
        )
    )

    metrics = {
        "accuracy": (
            accuracy_score(
                y_test,
                predictions,
            )
        ),
        "precision": (
            precision_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "recall": (
            recall_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "f1": (
            f1_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
    }

    for name, value in (
        metrics.items()
    ):
        print(
            f"{name}: "
            f"{value:.4f}"
        )

    model_path = Path(
        MODEL_PATH
    )

    model_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        pipeline,
        model_path,
    )


if __name__ == "__main__":
    main()
```

---

# 28. Résultat ML de référence

Avec :

```text
déduplication du dataset
features ci-dessus
test_size = 0.30
random_state = 42
stratify = y
LogisticRegression
```

une exécution de référence sur le dataset blanc produit :

```text
accuracy  ≈ 0.7143
precision ≈ 1.0000
recall    ≈ 0.3333
f1        ≈ 0.5000
```

Matrice de confusion de cette exécution :

```text
[[4, 0],
 [2, 1]]
```

Soit seulement :

```text
7 observations
```

dans le jeu de test.

## Interprétation correcte

Il ne faut **pas** conclure :

```text
"le modèle est performant"
```

à partir de ce seul score.

Le dataset est beaucoup trop petit.

La bonne conclusion ressemble plutôt à :

> Le pipeline de classification fonctionne techniquement, mais les métriques sont très instables compte tenu du faible nombre d’observations. Une collecte beaucoup plus importante serait nécessaire avant toute conclusion sur la performance réelle.

Les valeurs exactes peuvent différer si :

```text
le split
le preprocessing
les features
ou le modèle
```

diffèrent.

---

# 29. Pourquoi sauvegarder la Pipeline complète

Le corrigé utilise :

```python
joblib.dump(
    pipeline,
    model_path,
)
```

et non uniquement :

```python
joblib.dump(
    model,
    ...
)
```

Avantage :

```text
préprocessing
+
encodage
+
modèle
```

sont sauvegardés ensemble.

C’est une amélioration pratique du corrigé ; le support DataScientest demande simplement la sauvegarde du modèle via `joblib`.

---

# 30. Rechargement

```python
pipeline = joblib.load(
    "models/model.joblib"
)
```

Puis :

```python
prediction = pipeline.predict(
    new_data
)
```

---

# 31. Tests — stratégie de correction

Les trois axes explicitement annoncés par le support sont :

```text
gestion des erreurs
détection de doublons
conformité au schéma
```

Le corrigé doit donc les couvrir directement.

---

# 32. `tests/test_etl.py`

```python
import pandas as pd
import pytest

from src.etl import (
    transform,
    validate_schema,
)


def valid_df():
    return pd.DataFrame(
        {
            "delivery_id": [
                1,
                2,
            ],
            "customer_id": [
                10,
                11,
            ],
            "customer_city": [
                " Paris ",
                "POISSY",
            ],
            "vehicle_type": [
                "Bike",
                "Car",
            ],
            "distance_km": [
                5.0,
                10.0,
            ],
            "traffic_level": [
                "High",
                "Low",
            ],
            "weather": [
                "Rain",
                "Clear",
            ],
            "delivery_minutes": [
                30,
                25,
            ],
            "late_delivery": [
                1,
                0,
            ],
        }
    )


def test_valid_schema():
    df = valid_df()

    validate_schema(df)


def test_missing_column_is_rejected():
    df = (
        valid_df()
        .drop(
            columns=[
                "weather"
            ]
        )
    )

    with pytest.raises(
        ValueError
    ):
        validate_schema(df)


def test_duplicate_delivery_is_removed():
    df = valid_df()

    duplicate = (
        df.iloc[[0]]
        .copy()
    )

    df = pd.concat(
        [
            df,
            duplicate,
        ],
        ignore_index=True,
    )

    result = transform(df)

    assert (
        result["delivery_id"]
        .is_unique
    )

    assert len(result) == 2


def test_city_is_normalized():
    result = transform(
        valid_df()
    )

    assert (
        result.loc[
            0,
            "customer_city",
        ]
        == "paris"
    )


def test_missing_file_is_an_error(
    tmp_path,
):
    from src.etl import (
        extract,
    )

    with pytest.raises(
        FileNotFoundError
    ):
        extract(
            tmp_path
            / "missing.json"
        )
```

---

# 33. Test des nulls

Exemple additionnel :

```python
def test_missing_distance_is_imputed():
    df = valid_df()

    df.loc[
        0,
        "distance_km",
    ] = None

    result = transform(df)

    assert not (
        result["distance_km"]
        .isna()
        .any()
    )
```

---

# 34. Test d’intégration d’ingestion

Une simulation plus complète peut vérifier la propriété d’idempotence :

```text
ingestion 1
→ 23 deliveries

ingestion 2
→ toujours 23 deliveries
```

Pseudo-test :

```python
def test_ingestion_is_idempotent():
    df = pd.read_csv(
        "data/processed/"
        "deliveries_clean.csv"
    )

    ingest(df)

    first_count = (
        session
        .query(Delivery)
        .count()
    )

    ingest(df)

    second_count = (
        session
        .query(Delivery)
        .count()
    )

    assert first_count == 23
    assert second_count == 23
```

Ce test nécessite une base de test correctement initialisée ; il s’agit donc d’un test d’intégration.

---

# 35. Lancer les tests

```bash
pytest -v
```

Minimum attendu pour l’examen blanc :

```text
schéma
doublon
erreur
happy path
```

---

# 36. Impact écologique — correction proposée

Le support DataScientest mentionne une estimation de consommation énergétique, mais la page de préparation ne fournit pas de méthode officielle.

Une réponse prudente peut distinguer :

```text
mesure réelle
et
ordre de grandeur
```

---

# 37. Principaux postes de consommation

Pour cette architecture :

```text
ordinateur / VM
base MariaDB
phpMyAdmin
Python ETL
entraînement ML
stockage
Docker
```

Le modèle ML est très petit ; l’entraînement est donc ici probablement marginal par rapport au fait de maintenir l’environnement informatique actif.

---

# 38. Formule d’ordre de grandeur

Une approximation énergétique simple est :

```text
Énergie (kWh)
=
Puissance moyenne (kW)
×
Durée (h)
```

Exemple purement illustratif :

```text
50 W
pendant
10 minutes
```

donne :

```text
0,050 kW
×
10 / 60 h
≈
0,0083 kWh
```

Cette valeur **n’est pas une mesure du projet blanc**.

Elle montre uniquement la méthode de calcul.

Une estimation sérieuse nécessiterait une puissance ou une consommation réellement mesurée / documentée.

---

# 39. Leviers de réduction possibles

```text
arrêter les containers inutilisés
réduire la durée d’exécution
éviter les recalculs inutiles
traiter uniquement les nouvelles données
limiter les duplications de données
dimensionner les ressources au besoin
```

---

# 40. Limites de l’estimation écologique

À mentionner :

```text
pas de mesure matérielle directe
puissance machine inconnue
coût énergétique du stockage non mesuré
facteur carbone de l’électricité non estimé
durée d’exécution très courte
```

---

# 41. Exemple de `ARCHITECTURE.md`

```markdown
# GreenDelivery — Architecture

## 1. Contexte

Le projet transforme des événements JSON de livraison,
les charge dans une base relationnelle et entraîne
un modèle de classification du retard.

## 2. Pipeline

deliveries.json
→ pandas
→ nettoyage
→ deliveries_clean.csv
→ SQLAlchemy
→ MariaDB

En parallèle :

deliveries_clean.csv
→ preprocessing
→ LogisticRegression
→ model.joblib

## 3. Modèle relationnel

Customer 1 → N Delivery

## 4. Docker

MariaDB et phpMyAdmin sont lancés via Docker Compose.
Un volume nommé assure la persistance.

## 5. Machine Learning

Target : late_delivery.

Features retenues :
customer_city, vehicle_type, distance_km,
traffic_level, weather.

delivery_minutes est exclu dans cette solution
pour éviter une fuite potentielle d’information
si la prédiction doit avoir lieu avant la livraison.

## 6. Tests

Les tests couvrent :
- schéma ;
- erreurs ;
- doublons ;
- transformation nominale.

## 7. Limites

Le dataset est très petit.
Les métriques ML ne permettent donc pas
de conclure sur la performance réelle.

## 8. Pistes d’amélioration

- collecter davantage de données ;
- ajouter des variables temporelles ;
- ajouter heure / jour / zone ;
- comparer plusieurs modèles ;
- renforcer les tests d’intégration ;
- mesurer réellement la consommation énergétique.
```

---

# 42. Ordre d’exécution complet

Une séquence de correction cohérente :

```bash
python -m venv .venv
```

Puis activer l’environnement et installer :

```bash
pip install -r requirements.txt
```

Démarrer la base :

```bash
docker compose up -d
```

Vérifier :

```bash
docker compose ps
```

Exécuter l’ETL :

```bash
python -m src.etl
```

Créer les tables :

```bash
python -m src.create_database
```

Ingérer :

```bash
python -m src.ingest
```

Entraîner :

```bash
python -m src.train_model
```

Tester :

```bash
pytest -v
```

---

# 43. Résultats finaux attendus

À la fin de la correction de référence :

```text
deliveries_clean.csv
→ 23 lignes

customers
→ 22 lignes

deliveries
→ 23 lignes

model.joblib
→ présent

tests
→ exécutables

documentation
→ présente
```

---

# 44. Arborescence finale possible

```text
green_delivery/
│
├── data/
│   ├── raw/
│   │   └── deliveries.json
│   └── processed/
│       └── deliveries_clean.csv
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
│   ├── create_database.py
│   ├── ingest.py
│   └── train_model.py
│
├── tests/
│   └── test_etl.py
│
├── models/
│   └── model.joblib
│
├── docker-compose.yml
├── .env
├── .env.example
├── requirements.txt
└── ARCHITECTURE.md
```

---

# 45. Barème d’entraînement proposé

> **Non officiel.**
>
> Ce barème sert uniquement à corriger ses propres simulations.

```text
Exploration / notebook               10
ETL / qualité Python                 15
Modèle relationnel                   10
Docker / variables / persistance     10
SQLAlchemy / ORM                     15
Ingestion                            10
Machine Learning                     15
Tests                                10
Documentation / impact                5
────────────────────────────────────────
TOTAL                               100
```

---

# 46. Interprétation du score d’entraînement

```text
90–100
→ chaîne très maîtrisée

75–89
→ bon niveau, quelques fragilités

60–74
→ pipeline global compris,
  mais plusieurs automatismes à renforcer

< 60
→ refaire le blanc après révision ciblée
```

Ce classement est lui aussi uniquement un outil de préparation.

---

# 47. Ce qui vaut plus qu’un code sophistiqué

Pendant une simulation de 4 heures, privilégier :

```text
code simple
+
livrables complets
+
résultats vérifiés
```

à :

```text
architecture complexe
+
livrables manquants
```

---

# 48. Erreurs fréquentes — exploration

```text
explorer pendant 1 h 30
sans passer au script

ne pas détecter le doublon

ne pas regarder les nulls

ne pas identifier le grain
```

---

# 49. Erreurs fréquentes — ETL

```text
tout laisser dans le notebook

supprimer les nulls sans justification

supprimer les doublons sans identifier la clé

écraser le fichier raw
```

---

# 50. Erreurs fréquentes — ORM

```text
oublier la PK

mauvaise FK

oublier create_all

oublier commit

confondre relationship et ForeignKey
```

---

# 51. Erreurs fréquentes — Docker

```text
mauvais port

credentials incohérents

volume absent

confondre localhost et nom de service

ne jamais lire les logs
```

---

# 52. Erreurs fréquentes — ML

```text
target encore dans X

ID traité comme feature sans justification

fuite d’information

NaN non gérés

catégories non encodées

évaluation sur le train uniquement

pas de joblib
```

---

# 53. Erreurs fréquentes — tests

```text
aucun test de doublon

aucun test de schéma

except Exception: pass

tests dépendants entre eux

tests écrits mais jamais exécutés
```

---

# 54. Erreurs fréquentes — rendu

```text
documentation absente

archive non vérifiée

model.joblib oublié

.env requis mais non documenté

upload lancé trop tard
```

---

# 55. Questions à savoir défendre oralement

Après avoir terminé ce corrigé, être capable d’expliquer sans notes :

1. Quel est le grain du dataset ?
2. Pourquoi `delivery_id` est-il la PK ?
3. Pourquoi `customer_id` est-il une FK dans `deliveries` ?
4. Pourquoi normaliser `customer_city` ?
5. Comment avez-vous traité les nulls ?
6. Comment avez-vous traité le doublon ?
7. Pourquoi un volume Docker ?
8. Pourquoi des variables d’environnement ?
9. Quel rôle joue SQLAlchemy ?
10. Différence entre `ForeignKey` et `relationship` ?
11. Pourquoi exclure `delivery_minutes` du modèle de référence ?
12. Pourquoi les métriques ML sont-elles fragiles ?
13. Pourquoi sauvegarder le pipeline avec `joblib` ?
14. Quels tests protègent l’ingestion ?
15. Quelles améliorations feriez-vous avec davantage de temps ?

---

# 56. Auto-correction chronométrique

Après le blanc, remplir :

```text
Lecture / cadrage     : ____ min
Exploration           : ____ min
ETL                   : ____ min
Docker / ORM          : ____ min
Ingestion             : ____ min
ML                    : ____ min
Tests                 : ____ min
Documentation         : ____ min
ZIP / upload          : ____ min
```

Puis :

```text
Temps total           : ____ min / 240
```

---

# 57. Diagnostic personnel

Compléter :

```text
Bloc le plus lent :
________________________________

Bug le plus coûteux :
________________________________

Syntaxe oubliée :
________________________________

Livrable commencé trop tard :
________________________________

Automatisme à travailler :
________________________________
```

---

# 58. Definition of Done du Bloc 2 blanc

Le blanc est réellement terminé lorsque :

```text
[ ] notebook présent
[ ] ETL exécutable
[ ] fichier clean produit
[ ] Compose démarre
[ ] DB accessible
[ ] modèles ORM créent les tables
[ ] ingestion fonctionne
[ ] 22 customers présents
[ ] 23 deliveries présentes
[ ] modèle ML entraîné
[ ] métrique produite
[ ] model.joblib présent
[ ] tests exécutés
[ ] documentation présente
[ ] archive vérifiée
[ ] temps ≤ 240 min
```

---

# 59. Ce que le corrigé cherche réellement à entraîner

Ce n’est pas seulement :

```text
pandas
SQLAlchemy
Docker
scikit-learn
```

C’est surtout la capacité à enchaîner :

```text
comprendre
→ décider
→ implémenter
→ vérifier
→ expliquer
→ livrer
```

sous contrainte temporelle.

---

# 60. Synthèse finale

Le corrigé de référence transforme le dataset blanc comme suit :

```text
24 lignes brutes
      ↓
détection doublon / nulls
      ↓
23 livraisons propres
      ↓
22 clients
      ↓
Customer 1 → N Delivery
      ↓
MariaDB + SQLAlchemy
      ↓
ingestion idempotente
      ↓
classification late_delivery
      ↓
joblib
      ↓
tests
      ↓
documentation
```

La compétence centrale évaluée par ce blanc n’est donc pas un algorithme particulier.

C’est la maîtrise d’une chaîne **Data Engineering + ML complète**, cohérente et livrable dans le temps imparti.

---

# 61. Fin du kit initial Bloc 2

Avec ce document, le premier kit de préparation est complet :

```text
00 Analyse complète
01 Fiche de révision
02 Mega Cheatsheet
03 Guide ETL Python
04 Guide SQLAlchemy / ORM
05 Guide Docker Compose
06 Guide Machine Learning
07 Testing Strategy
08 Template Project
09 Stratégie examen 4 h
10 Checklist Jour J
11 Examen blanc 01
12 Corrigé examen blanc 01
```

La suite logique n’est plus de produire immédiatement davantage de théorie.

Elle est de :

```text
PASSER LE BLANC
      ↓
MESURER LES LACUNES
      ↓
RÉVISER UNIQUEMENT LES POINTS FAIBLES
      ↓
REPASSER UN SECOND BLANC
```
