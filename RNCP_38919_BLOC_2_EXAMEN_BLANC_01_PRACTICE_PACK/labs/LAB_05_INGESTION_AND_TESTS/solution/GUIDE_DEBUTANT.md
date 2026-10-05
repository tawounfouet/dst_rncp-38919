# LAB 05 — Guide débutant (de zéro à la solution)

> **Public** : tu n'as jamais écrit de test ni manipulé une base en Python.
> On explique tout. À la fin : une validation de données, une ingestion
> **idempotente** et **7 tests qui passent**.

Ce lab répond à une question : *comment être sûr que mes données sont correctes
et que je ne les insère pas deux fois ?*

---

## Étape 0 — Le vocabulaire

| Mot | Signification simple |
|---|---|
| **Test** | Un bout de code qui **vérifie** qu'un autre code fait bien ce qu'on attend. |
| **pytest** | L'outil Python pour exécuter les tests (commande `pytest`). |
| **assertion** | Une affirmation « ceci doit être vrai » (sinon le test échoue). |
| **fixture** | Une **préparation réutilisable** avant un test (ex. créer une base temporaire). |
| **`pytest.raises`** | Vérifie qu'un morceau de code **lève bien une erreur**. |
| **ingestion** | Insérer des données dans une base. |
| **idempotent** | Refaire l'opération **ne change rien** (pas de doublon). |
| **SQLite** | Une base de données **dans un simple fichier** — parfaite pour les tests, rien à installer. |

Ici, on utilise SQLite pour être **autonome** (pas besoin de Docker).

---

## Étape 1 — L'environnement

```bash
cd LAB_05_INGESTION_AND_TESTS
python3 -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt
```

---

## Étape 2 — Valider un tableau : `validation.py`

Avant d'insérer, on **contrôle** que le tableau est conforme :

```python
REQUIRED_COLUMNS = {
    "delivery_id", "customer_id", "customer_city", "vehicle_type",
    "distance_km", "traffic_level", "weather", "delivery_minutes",
    "late_delivery",
}

def validate_dataframe(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    if df["delivery_id"].isna().any():
        raise ValueError("Null delivery_id detected")

    if df["delivery_id"].duplicated().any():
        raise ValueError("Duplicate delivery_id detected")
```

- `REQUIRED_COLUMNS - set(df.columns)` → les colonnes **manquantes** (opération d'ensembles).
- `df["delivery_id"].isna().any()` → `.isna()` marque les vides, `.any()` dit « au moins un vide ? ». Si oui → erreur.
- `df["delivery_id"].duplicated().any()` → « au moins un identifiant en double ? ». Si oui → erreur.

**Idée clé** : la validation **échoue bruyamment** (`raise`) au lieu de laisser passer des données douteuses.

---

## Étape 3 — Ingérer sans doublon : `ingest.py`

L'astuce de l'idempotence : **ne garder que les `delivery_id` inconnus**.

```python
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from validation import validate_dataframe

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = BASE_DIR.parent.parent / "LAB_01_JSON_JUPYTER_PANDAS" / "data" / "deliveries_lab.json"
DEFAULT_DB = BASE_DIR / "deliveries.sqlite"
```

- `BASE_DIR` → dossier de ce fichier. On construit les chemins **relativement au script**.
- `DEFAULT_DB` → le fichier SQLite sera créé à côté du script.

Création de la table si absente :

```python
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    customer_city TEXT,
    vehicle_type TEXT,
    distance_km REAL,
    traffic_level TEXT,
    weather TEXT,
    delivery_minutes INTEGER,
    late_delivery INTEGER
)
"""

def ensure_table(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text(CREATE_TABLE))
```

- `CREATE TABLE IF NOT EXISTS` → crée la table **seulement si elle n'existe pas** (`IF NOT EXISTS` évite une erreur au 2e passage).
- `engine.begin()` → ouvre une **transaction** (un bloc de travail), `with` la ferme automatiquement.
- `conn.execute(text(...))` → exécute du **SQL brut**. `text()` dit à SQLAlchemy « c'est du SQL, pas du Python ».

Lire les identifiants déjà présents :

```python
def existing_ids(engine: Engine) -> set[int]:
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT delivery_id FROM deliveries")).fetchall()
    return {row[0] for row in rows}
```

- `fetchall()` → récupère toutes les lignes.
- `{row[0] for row in rows}` → un **ensemble** des identifiants (rapide pour tester l'appartenance).

La fonction d'ingestion :

```python
def ingest(df: pd.DataFrame, engine: Engine) -> int:
    """Insère les lignes dont le delivery_id est inconnu. Retourne le nombre inséré."""
    validate_dataframe(df)
    ensure_table(engine)

    known = existing_ids(engine)
    new = df[~df["delivery_id"].isin(known)]

    if not new.empty:
        new.to_sql("deliveries", engine, if_exists="append", index=False)

    return len(new)
```

- `validate_dataframe(df)` → on refuse un tableau invalide.
- `known` → les identifiants déjà en base.
- `df[~df["delivery_id"].isin(known)]` :
  - `.isin(known)` → `True` si l'identifiant est **déjà présent**.
  - `~` → **négation** : on garde ceux **qui ne sont pas** présents.
  - Résultat : uniquement les **nouvelles** lignes.
- `new.to_sql("deliveries", engine, if_exists="append", index=False)` → insère les nouvelles lignes dans la table.
- `return len(new)` → renvoie le nombre inséré. C'est **la preuve** de l'idempotence : à la 2e passe, ça vaut `0`.

Et un compteur :

```python
def count_rows(engine: Engine) -> int:
    with engine.connect() as conn:
        return conn.execute(text("SELECT COUNT(*) FROM deliveries")).scalar_one()
```

- `scalar_one()` → renvoie la **valeur unique** du résultat (ici le compte).

Le point d'entrée :

```python
def main() -> None:
    engine = create_engine(f"sqlite:///{DEFAULT_DB}")
    df = pd.read_json(DEFAULT_SOURCE).drop_duplicates(subset=["delivery_id"]).copy()

    inserted = ingest(df, engine)
    again = ingest(df, engine)

    print(f"1re ingestion : {inserted} ligne(s) insérée(s)")
    print(f"2e  ingestion : {again} ligne(s) insérée(s)  <- doit valoir 0")
    print(f"total en base : {count_rows(engine)}")

if __name__ == "__main__":
    main()
```

- `create_engine(f"sqlite:///{DEFAULT_DB}")` → SQLite **dans un fichier** (pas en mémoire).
- On ingère **deux fois** exprès : la 2e doit insérer `0`.

---

## Étape 4 — Écrire des tests : `test_validation.py`

Un test est une **fonction dont le nom commence par `test_`**.

```python
import pandas as pd
import pytest

from validation import validate_dataframe

def sample_df():
    return pd.DataFrame({
        "delivery_id": [1, 2],
        "customer_id": [10, 11],
        "customer_city": ["paris", "poissy"],
        "vehicle_type": ["bike", "car"],
        "distance_km": [4.0, 12.0],
        "traffic_level": ["high", "low"],
        "weather": ["rain", "clear"],
        "delivery_minutes": [35, 30],
        "late_delivery": [1, 0],
    })
```

- `sample_df()` → un **tableau valide de test**, construit à la main. Le nom ne commence pas par `test_`, donc pytest ne le prend pas pour un test : c'est juste un utilitaire.

Le **cas nominal** (tout va bien) :

```python
def test_valid_dataframe():
    validate_dataframe(sample_df())
```

Si `validate_dataframe` ne lève rien, le test passe. Aucun `assert` n'est nécessaire ici : si une erreur était levée, le test échouerait.

Le **cas d'erreur** (colonne manquante) :

```python
def test_missing_column():
    df = sample_df().drop(columns=["weather"])
    with pytest.raises(ValueError):
        validate_dataframe(df)
```

- `sample_df().drop(columns=["weather"])` → on retire une colonne requise.
- `with pytest.raises(ValueError):` → on **attend** qu'une `ValueError` soit levée. Si aucune erreur n'est levée, **le test échoue**. C'est ainsi qu'on teste les erreurs.

Le **cas du doublon** :

```python
def test_duplicate_delivery_id():
    df = pd.concat([sample_df(), sample_df().iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError):
        validate_dataframe(df)
```

- `pd.concat([...])` → colle deux tableaux.
- `.iloc[[0]]` → la **première ligne** (copiée).
- `ignore_index=True` → renumérote les lignes.
- On a donc un doublon sur `delivery_id` → on attend une `ValueError`.

---

## Étape 5 — Tester l'ingestion : `test_ingest.py`

Ici on a besoin d'une base **isolée** par test. C'est le rôle d'une **fixture**.

```python
import pandas as pd
import pytest
from sqlalchemy import create_engine

from ingest import count_rows, ingest


@pytest.fixture
def engine(tmp_path):
    return create_engine(f"sqlite:///{tmp_path / 'deliveries.sqlite'}")
```

- `@pytest.fixture` → marque une **préparation réutilisable**.
- `tmp_path` → un **dossier temporaire unique** fourni par pytest (nettoyé automatiquement).
- La fixture crée une base SQLite **en fichier**, dans ce dossier temporaire.

Pourquoi un fichier et pas `:memory:` ? Parce qu'une base en mémoire (`:memory:`) est **recréée à chaque connexion** : les différentes étapes verraient des bases différentes. Le fichier garantit qu'on travaille sur **la même** base.

```python
def test_first_ingestion_inserts_all(engine):
    assert ingest(sample_df(), engine) == 2
    assert count_rows(engine) == 2
```

- `assert condition` → si la condition est fausse, le test échoue.
- 1re ingestion : 2 lignes insérées, 2 en base.

```python
def test_reingestion_does_not_duplicate(engine):
    ingest(sample_df(), engine)
    assert ingest(sample_df(), engine) == 0      # 0 nouvelle ligne
    assert count_rows(engine) == 2               # toujours 2
```

C'est LE test qui prouve l'idempotence.

```python
def test_partial_reingestion_inserts_only_new(engine):
    ingest(sample_df(), engine)
    extended = pd.concat([sample_df(), sample_df().iloc[[0]].assign(delivery_id=3)],
                         ignore_index=True)
    assert ingest(extended, engine) == 1
    assert count_rows(engine) == 3
```

- `.assign(delivery_id=3)` → crée une copie avec `delivery_id = 3` (nouvelle ligne).
- On ré-ingère : seule la ligne **nouvelle** est ajoutée (`1`).

```python
def test_ingest_rejects_invalid_dataframe(engine):
    invalid = sample_df().drop(columns=["weather"])
    with pytest.raises(ValueError):
        ingest(invalid, engine)
```

L'ingestion **refuse** un tableau non conforme.

---

## Étape 6 — Lancer les tests

```bash
cd solution
pytest -q
```

Attendu :

```text
7 passed
```

Et la démo :

```bash
python ingest.py
```

Attendu :

```text
1re ingestion : 12 ligne(s) insérée(s)
2e  ingestion : 0 ligne(s) insérée(s)  <- doit valoir 0
total en base : 12
```

---

## Erreurs fréquentes

| Symptôme | Cause | Solution |
|---|---|---|
| `3 passed` sur le starter | tests vides (`pass`) | c'est un faux positif : les tests starter `pytest.fail(...)` doivent être **rouges** au départ |
| `sqlite3.OperationalError: table delivers already exists` | table pré-existante | `CREATE TABLE IF NOT EXISTS` ; supprime `deliveries.sqlite` pour repartir |
| `ModuleNotFoundError: validation` | mauvais dossier | lancer `pytest` depuis `solution/` |
| tests instables | base partagée entre tests | utiliser `tmp_path` (fixture) |

---

## Mini-glossaire final

```text
test            → fonction test_* qui vérifie un comportement
assert          → "ceci doit être vrai"
pytest.raises   → "ceci doit lever une erreur"
fixture         → préparation réutilisable
tmp_path        → dossier temporaire fourni par pytest
idempotent      → refaire = aucun changement
isin()          → "appartient à la liste ?"
to_sql          → écrire un DataFrame dans une table
scalar_one()    → récupérer une valeur unique
```
