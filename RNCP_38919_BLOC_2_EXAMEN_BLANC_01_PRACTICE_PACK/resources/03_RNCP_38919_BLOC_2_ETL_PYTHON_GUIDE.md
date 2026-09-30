# 03 — RNCP 38919 — Bloc 2
# Guide ETL Python — JSON → Jupyter → pandas → Scripts

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Durée officielle :** 4 heures

**Sources principales :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`
- `Consignes surveillance évaluation.pdf`

> **Important**
>
> Ce document distingue :
>
> - **Attendu source** : ce qui apparaît dans le support DataScientest ;
> - **Guide pratique** : méthodes, exemples et patterns de préparation proposés pour s’entraîner.
>
> Le support annonce l’exploration JSON, Jupyter, Python structuré, `pandas`, `matplotlib`,
> la gestion des valeurs manquantes et des colonnes catégorielles.
> Il ne fournit pas, dans la page source disponible, une architecture ETL unique ni des fonctions
> imposées. Les patterns ci-dessous servent donc de préparation.

---

# 1. Périmètre ETL du Bloc 2

## Attendu source

Le support de préparation annonce notamment :

```text
1. Exploration de données au format JSON à l'aide de notebooks Jupyter
2. Développement de scripts Python structurés et réutilisables
3. Manipulation de données avec pandas et matplotlib
4. Gestion des valeurs manquantes et des colonnes catégorielles
```

Il demande également, dans le rendu :

```text
- un notebook d'exploration de données ;
- un script Python reprenant les étapes d'extraction et transformation.
```

Le cœur de cette partie peut donc être résumé ainsi :

```text
JSON
  ↓
Jupyter
  ↓
Comprendre
  ↓
pandas
  ↓
Nettoyer
  ↓
Transformer
  ↓
Script Python réutilisable
```

---

# 2. Objectif de préparation

## Guide pratique

À la fin de cette partie, il faut être capable de produire rapidement :

```text
data.json
   │
   ▼
01_exploration.ipynb
   │
   ▼
transform.py
   │
   ▼
dataset propre
```

avec une séparation claire :

```text
Notebook
=
comprendre / expérimenter

Script
=
rejouer / structurer / réutiliser
```

---

# 3. Étape 1 — Lire un fichier JSON

## Guide pratique

### Cas simple avec pandas

```python
import pandas as pd

df = pd.read_json("data.json")
```

### Cas avec `json`

```python
import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

Puis :

```python
df = pd.DataFrame(data)
```

### Réflexe

Toujours vérifier d’abord :

```python
type(data)
```

car un JSON peut représenter :

```text
list
dict
nested dict
records
```

---

# 4. Étape 2 — Comprendre la structure

## Guide pratique

Premières commandes :

```python
df.head()
df.shape
df.columns
df.info()
```

Puis :

```python
df.describe(include="all")
```

Checklist :

```text
[ ] nombre de lignes
[ ] nombre de colonnes
[ ] types
[ ] valeurs manquantes
[ ] doublons
[ ] colonnes catégorielles
[ ] target éventuelle
```

---

# 5. Étape 3 — Valeurs manquantes

## Attendu source

Le support annonce explicitement :

```text
gestion des valeurs manquantes
```

## Guide pratique

### Compter

```python
df.isna().sum()
```

### Taux de nulls

```python
null_rate = df.isna().mean().sort_values(ascending=False)
```

### Supprimer

```python
df = df.dropna()
```

ou :

```python
df = df.dropna(subset=["important_column"])
```

### Imputer une valeur fixe

```python
df["status"] = df["status"].fillna("unknown")
```

### Imputer par médiane

```python
df["age"] = df["age"].fillna(df["age"].median())
```

### Règle

Ne pas appliquer automatiquement :

```text
fillna(0)
```

partout.

Toujours demander :

```text
Que signifie l'absence ?
```

---

# 6. Étape 4 — Colonnes catégorielles

## Attendu source

Le support mentionne :

```text
gestion des colonnes catégorielles
```

## Guide pratique

Identifier :

```python
categorical_columns = df.select_dtypes(
    include=["object", "category"]
).columns
```

Inspecter :

```python
for col in categorical_columns:
    print(col, df[col].value_counts(dropna=False).head())
```

Normaliser :

```python
df["city"] = (
    df["city"]
    .astype("string")
    .str.strip()
    .str.lower()
)
```

Encodage simple pour ML :

```python
encoded = pd.get_dummies(
    df,
    columns=["category"],
    drop_first=True,
)
```

> Le support ne fixe pas une méthode d’encodage particulière.
> `get_dummies()` est ici un pattern de préparation.

---

# 7. Étape 5 — Doublons

## Guide pratique

### Détecter

```python
df.duplicated().sum()
```

### Voir les doublons

```python
df[df.duplicated(keep=False)]
```

### Selon une clé métier

```python
df[df.duplicated(subset=["id"], keep=False)]
```

### Supprimer

```python
df = df.drop_duplicates(subset=["id"])
```

Question à se poser :

```text
Le doublon est-il technique
ou
métier ?
```

---

# 8. Étape 6 — Types

## Guide pratique

### Numérique

```python
df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce",
)
```

### Date

```python
df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce",
)
```

### Booléen

```python
df["active"] = df["active"].astype("boolean")
```

### Texte

```python
df["name"] = df["name"].astype("string")
```

---

# 9. Étape 7 — Nettoyage de chaînes

## Guide pratique

```python
df["name"] = (
    df["name"]
    .astype("string")
    .str.strip()
)
```

Casse :

```python
df["email"] = (
    df["email"]
    .astype("string")
    .str.strip()
    .str.lower()
)
```

Remplacement :

```python
df["status"] = df["status"].replace({
    "A": "active",
    "I": "inactive",
})
```

---

# 10. Étape 8 — Sélection et renommage

## Guide pratique

### Sélection

```python
df = df[
    [
        "id",
        "name",
        "category",
        "amount",
    ]
]
```

### Renommage

```python
df = df.rename(
    columns={
        "User ID": "user_id",
        "Full Name": "full_name",
    }
)
```

---

# 11. Étape 9 — Filtres

## Guide pratique

```python
active = df[df["status"] == "active"]
```

Plusieurs conditions :

```python
filtered = df[
    (df["amount"] > 0)
    & (df["status"] == "active")
]
```

---

# 12. Étape 10 — Agrégations

## Guide pratique

```python
summary = (
    df.groupby("category")["amount"]
    .agg(["count", "mean", "sum"])
)
```

Comptage :

```python
df["category"].value_counts()
```

---

# 13. Étape 11 — Visualisation minimale avec matplotlib

## Attendu source

Le support mentionne :

```text
matplotlib
```

## Guide pratique

### Histogramme

```python
import matplotlib.pyplot as plt

df["amount"].hist()
plt.title("Distribution des montants")
plt.show()
```

### Bar chart

```python
df["category"].value_counts().plot(kind="bar")
plt.title("Répartition par catégorie")
plt.show()
```

### Objectif

Pendant l’épreuve :

```text
visualiser
pour comprendre
```

pas produire un dashboard complet.

---

# 14. Étape 12 — Séparer exploration et transformation

## Guide pratique

Dans le notebook :

```python
df = pd.read_json("data.json")

df.head()
df.info()

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce",
)

df = df.dropna(subset=["id"])
```

Puis transformer cette logique en fonction :

```python
def transform(df):
    df = df.copy()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    df = df.dropna(subset=["id"])

    return df
```

---

# 15. Pattern ETL minimal

## Guide pratique

```python
from pathlib import Path
import pandas as pd


def extract(path: str | Path) -> pd.DataFrame:
    return pd.read_json(path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result = result.drop_duplicates()

    return result


def load(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    df.to_csv(
        output_path,
        index=False,
    )


def main() -> None:
    df = extract("data/raw/data.json")
    df = transform(df)
    load(df, "data/processed/data.csv")


if __name__ == "__main__":
    main()
```

---

# 16. Pattern ETL un peu plus robuste

## Guide pratique

```python
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "id",
    "name",
    "category",
}


def extract(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)

    return pd.read_json(path)


def validate_schema(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )


def transform(df: pd.DataFrame) -> pd.DataFrame:
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

    result = result.drop_duplicates(
        subset=["id"]
    )

    return result


def load(
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        index=False,
    )


def main() -> None:
    input_path = Path(
        "data/raw/data.json"
    )
    output_path = Path(
        "data/processed/data.csv"
    )

    df = extract(input_path)
    df = transform(df)
    load(df, output_path)


if __name__ == "__main__":
    main()
```

---

# 17. Validation de schéma

## Guide pratique

Pattern simple :

```python
REQUIRED_COLUMNS = {
    "id",
    "name",
    "category",
}
```

Puis :

```python
missing = REQUIRED_COLUMNS - set(df.columns)

if missing:
    raise ValueError(
        f"Missing columns: {missing}"
    )
```

---

# 18. Validation de clé

## Guide pratique

```python
if df["id"].isna().any():
    raise ValueError(
        "Null primary key detected"
    )
```

Doublon :

```python
if df["id"].duplicated().any():
    raise ValueError(
        "Duplicate id detected"
    )
```

---

# 19. Validation de domaine

## Guide pratique

```python
allowed = {
    "active",
    "inactive",
}

invalid = ~df["status"].isin(allowed)

if invalid.any():
    raise ValueError(
        "Invalid status detected"
    )
```

---

# 20. Journalisation minimale

## Guide pratique

Même si le support ne mentionne pas explicitement le module `logging`, un script de préparation peut utiliser :

```python
import logging

logger = logging.getLogger(__name__)
```

Puis :

```python
logger.info(
    "Loaded %s rows",
    len(df),
)
```

Pendant un examen très contraint, rester simple.

---

# 21. Structure de fichiers conseillée pour révision

## Guide pratique

```text
project/
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
│   └── transform.py
│
└── requirements.txt
```

---

# 22. Notebook d’exploration — squelette

## Guide pratique

```text
# 1. Imports
# 2. Load data
# 3. Shape / columns
# 4. Types
# 5. Missing values
# 6. Duplicates
# 7. Categorical variables
# 8. Numeric distributions
# 9. Cleaning decisions
# 10. Conclusion
```

---

# 23. Exemple de cellule d’audit

```python
audit = pd.DataFrame({
    "dtype": df.dtypes.astype(str),
    "nulls": df.isna().sum(),
    "null_rate": df.isna().mean(),
    "unique": df.nunique(),
})

audit
```

---

# 24. Checklist de transformation

## Guide pratique

```text
[ ] noms de colonnes propres
[ ] types corrects
[ ] clés non nulles
[ ] doublons contrôlés
[ ] catégories normalisées
[ ] valeurs manquantes traitées
[ ] dates converties
[ ] colonnes inutiles supprimées
[ ] output reproductible
```

---

# 25. Anti-patterns à éviter

## Guide pratique

### 1. Transformer directement le DataFrame original

À éviter :

```python
df["x"] = ...
```

partout.

Préférer :

```python
result = df.copy()
```

---

### 2. Fonctions gigantesques

À éviter :

```text
extract_transform_clean_validate_save_everything()
```

Préférer :

```text
extract
validate
transform
load
```

---

### 3. Valeurs codées en dur partout

À éviter :

```python
"/home/user/project/data.json"
```

Préférer :

```python
Path("data/raw/data.json")
```

---

### 4. Nulls supprimés sans justification

À éviter :

```python
df.dropna()
```

par réflexe systématique.

---

### 5. Doublons supprimés sans clé métier

À éviter :

```python
df.drop_duplicates()
```

sans comprendre ce qui définit l’unicité.

---

# 26. Mini-exercice 1 — Exploration

Créer un JSON contenant :

```json
[
  {
    "id": 1,
    "name": "Alice",
    "category": "A",
    "amount": 100
  },
  {
    "id": 2,
    "name": "Bob",
    "category": "B",
    "amount": null
  }
]
```

Faire :

```text
1. charger
2. afficher shape
3. afficher types
4. compter nulls
5. afficher catégories
```

---

# 27. Mini-exercice 2 — Nettoyage

À partir du même dataset :

```text
1. remplir amount manquant
2. normaliser category
3. détecter doublons
4. exporter CSV
```

---

# 28. Mini-exercice 3 — Passage Notebook → Script

Prendre le notebook précédent et créer :

```text
src/transform.py
```

avec :

```python
extract()
transform()
load()
main()
```

Objectif :

```bash
python src/transform.py
```

doit produire :

```text
data/processed/data.csv
```

---

# 29. Mini-exercice 4 — Schéma invalide

Supprimer une colonne obligatoire.

Le script doit produire une erreur explicite :

```text
Missing columns: [...]
```

---

# 30. Mini-exercice 5 — Doublons

Ajouter deux lignes avec le même `id`.

Créer deux variantes :

```text
A. rejet du dataset
B. déduplication contrôlée
```

Être capable d’expliquer le choix.

---

# 31. Mini-exercice 6 — Colonnes catégorielles

Dataset :

```text
city
Paris
PARIS
 paris
Poissy
POISSY
```

Résultat cible :

```text
paris
paris
paris
poissy
poissy
```

Pattern :

```python
df["city"] = (
    df["city"]
    .astype("string")
    .str.strip()
    .str.lower()
)
```

---

# 32. Mini-exercice 7 — Préparation ML

Depuis un dataset transformé :

```text
1. choisir une target
2. séparer X / y
3. identifier catégories
4. encoder
5. vérifier nulls
```

Ne pas encore entraîner le modèle.

L’objectif est de préparer correctement les données.

---

# 33. Réflexes de performance pendant l’examen

## Guide pratique

Éviter :

```text
boucles Python inutiles
```

quand pandas suffit.

Préférer :

```python
df["x"] = df["a"] + df["b"]
```

à :

```python
for row in ...:
    ...
```

sauf besoin spécifique.

---

# 34. Réflexes de lisibilité

## Guide pratique

Préférer :

```python
def clean_categories(df):
    ...
```

à :

```python
def f(d):
    ...
```

Préférer :

```python
customer_id
```

à :

```python
cid
```

si aucune contrainte ne l’impose.

---

# 35. Réflexe d’idempotence

## Guide pratique

Un script de transformation devrait idéalement produire le même résultat lorsque :

```text
même input
+
même code
=
même output
```

Cela évite les transformations dépendantes d’un état caché.

---

# 36. Réflexe de séparation

## Guide pratique

```text
RAW
↓
TRANSFORM
↓
PROCESSED
```

Ne jamais écraser immédiatement la source brute pendant l’entraînement.

---

# 37. Vérification avant passage à l’ORM

Avant de commencer la partie base de données :

```text
[ ] DataFrame final propre
[ ] schéma compris
[ ] clé primaire candidate identifiée
[ ] doublons contrôlés
[ ] nulls contrôlés
[ ] types maîtrisés
```

---

# 38. Temps cible de préparation

## Guide pratique

Lors d’un entraînement chronométré :

```text
Exploration : 20–30 min
Transformation : 20–30 min
Validation : 10 min
```

Objectif :

```text
≈ 45–60 min
```

pour être prêt à passer à la base / ORM.

> Cette répartition est une stratégie de préparation, pas une consigne officielle.

---

# 39. Checkpoint ETL

Avant de continuer l’épreuve :

```text
JSON
  ✅ lu

Notebook
  ✅ exploitable

Nulls
  ✅ traités

Doublons
  ✅ contrôlés

Catégories
  ✅ normalisées

Script
  ✅ exécutable

Output
  ✅ généré
```

---

# 40. Résumé à mémoriser

```text
READ
 ↓
INSPECT
 ↓
CLEAN
 ↓
VALIDATE
 ↓
TRANSFORM
 ↓
EXPORT
```

En Python :

```text
extract()
validate()
transform()
load()
```

---

# 41. Questions flash

1. Comment charger un JSON avec pandas ?
2. Comment afficher les types ?
3. Comment compter les nulls ?
4. Comment détecter les doublons ?
5. Comment convertir une colonne en numérique ?
6. Comment convertir une date ?
7. Comment normaliser une chaîne ?
8. Comment faire un groupby ?
9. Pourquoi séparer notebook et script ?
10. Pourquoi ne pas écraser le raw ?
11. Comment vérifier qu’une colonne obligatoire existe ?
12. Comment contrôler une clé primaire candidate ?

---

# 42. Réponses flash

```python
pd.read_json(...)
```

```python
df.info()
```

```python
df.isna().sum()
```

```python
df.duplicated().sum()
```

```python
pd.to_numeric(...)
```

```python
pd.to_datetime(...)
```

```python
.str.strip().str.lower()
```

```python
df.groupby(...)
```

Notebook :

```text
exploration
```

Script :

```text
réutilisation / reproductibilité
```

---

# 43. Document suivant

```text
04_RNCP_38919_BLOC_2_SQLALCHEMY_ORM_GUIDE.md
```

Objectif :

> approfondir la partie base relationnelle et ORM réellement mise en avant par le support dédié :
> `create_engine`, base déclarative, modèles, PK/FK, sessions, insertions, requêtes et relations.
