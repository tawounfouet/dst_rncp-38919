# LAB 02 — Guide débutant (de zéro à la solution)

> **Public** : tu sais ouvrir un fichier avec pandas (LAB 01) mais tu n'as jamais
> écrit un « vrai » script Python organisé. On explique chaque notion dès qu'elle
> apparaît. À la fin, tu auras compris et exécuté la solution complète.

Ce lab transforme le fichier brut du LAB 01 en un fichier **propre**.
C'est ce qu'on appelle un **ETL**.

---

## Étape 0 — Le vocabulaire

| Mot | Signification simple |
|---|---|
| **ETL** | **E**xtract (lire) → **T**ransform (nettoyer) → **L**oad (écrire). |
| **Extract** | Lire la source (ici le JSON). |
| **Transform** | Corriger : doublons, casse, valeurs manquantes, types. |
| **Load** | Sauvegarder le résultat (ici un CSV). |
| **Fonction** | Un bloc de code réutilisable, avec un nom (`extract`, `transform`…). |
| **Exception** | Une erreur volontairement déclenchée pour signaler un problème. |
| **CSV** | Fichier texte en tableau, séparé par des virgules. |

Le source est le JSON du LAB 01 : 13 lignes. Objectif : **12 lignes propres**, 0 valeur vide.

---

## Étape 1 — L'environnement

```bash
cd LAB_02_ETL_PYTHON
python3 -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt
```

(Rappel : `venv` = Python isolé ; `activate` l'active.)

---

## Étape 2 — Les constantes en haut du fichier

Ouvre `solution/etl.py`. On commence par déclarer ce qui ne change pas :

```python
from pathlib import Path
import sys

import pandas as pd

REQUIRED_COLUMNS = {
    "delivery_id", "customer_id", "customer_city",
    "vehicle_type", "distance_km", "traffic_level",
    "weather", "delivery_minutes", "late_delivery",
}
```

- `REQUIRED_COLUMNS` est un **ensemble** (`{...}`) : la liste des colonnes **obligatoires**.
  Comparer un ensemble à une autre liste est immédiat en Python.
- Les mettre en haut, en MAJUSCULES, signifie « constante de configuration ».

Puis les chemins par défaut :

```python
LABS_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = LABS_DIR / "LAB_01_JSON_JUPYTER_PANDAS" / "data" / "deliveries_lab.json"
DEFAULT_TARGET = Path(__file__).resolve().parent / "deliveries_clean.csv"
```

- `Path(__file__)` = chemin de `etl.py`. `.parents[2]` remonte deux dossiers plus haut (de `solution/` → `LAB_02/` → `labs/`).
- On construit des chemins **relatifs au script** : le code marchera depuis n'importe quel dossier.

---

## Étape 3 — `extract` : lire, ou échouer clairement

```python
def extract(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_json(path)
```

- `def extract(...)` → on **définit une fonction** nommée `extract`.
- `path: str | Path` → **annotation de type** : le paramètre peut être une chaîne ou un `Path`. Ce n'est pas obligatoire, mais ça documente et aide l'éditeur.
- `-> pd.DataFrame` → la fonction **renvoie** un DataFrame.
- `Path(path)` → convertit en objet `Path` (utile si on a passé une chaîne).
- `if not path.exists(): raise FileNotFoundError(path)` → si le fichier n'existe pas, on **arrête net** avec une erreur explicite. Principe d'or : *échouer fort et tôt*, plutôt que continuer avec des données fantômes.
- `return pd.read_json(path)` → lit et renvoie le tableau.

**Notion clé — `raise`** : lever une exception stoppe le programme et affiche un message clair. C'est mieux qu'un résultat faux en silence.

---

## Étape 4 — `validate_schema` : vérifier les colonnes

```python
def validate_schema(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
```

- `set(df.columns)` → l'ensemble des colonnes **présentes**.
- `REQUIRED_COLUMNS - set(...)` → opération d'**ensembles** : ce qui est requis **mais absent**.
- `if missing:` → si la différence n'est pas vide, il manque des colonnes.
- `raise ValueError(...)` → autre type d'erreur (« la valeur est invalide »), ici pour signaler un **problème de données**.
- `f"..."` → **f-string** : texte où `{...}` est remplacé par la valeur. `sorted(missing)` range les noms manquants.

**Pourquoi deux types d'erreur ?** `FileNotFoundError` = problème de fichier ;
`ValueError` = problème de contenu. On distingue les deux pour diagnostiquer vite.

---

## Étape 5 — `transform` : le cœur du nettoyage

```python
def transform(df: pd.DataFrame) -> pd.DataFrame:
    validate_schema(df)
    result = df.copy()
    result = result.drop_duplicates(subset=["delivery_id"], keep="first").copy()
```

- `validate_schema(df)` → on vérifie d'abord que tout est là.
- `df.copy()` → on travaille sur une **copie** pour ne pas modifier l'original.
- `.drop_duplicates(subset=["delivery_id"], keep="first")` → supprime les doublons **selon la clé `delivery_id`**, en **gardant la première** occurrence. `.copy()` évite un avertissement pandas (`SettingWithCopyWarning`).

Nettoyer les colonnes texte :

```python
    for col in ["customer_city", "vehicle_type"]:
        result[col] = result[col].astype("string").str.strip().str.lower()
```

- `for col in [...]` → **boucle** : on fait la même chose pour chaque colonne de la liste.
- `astype("string")` → type texte robuste ; `.str.strip()` enlève les espaces ; `.str.lower()` met en minuscules.

Remplir les vides des colonnes « catégorielles » :

```python
    for col in ["traffic_level", "weather"]:
        result[col] = (
            result[col].astype("string").str.strip().str.lower().fillna("unknown")
        )
```

- `.fillna("unknown")` → remplace les cases vides par le texte `"unknown"`.
  **Décision explicite** : on préfère une catégorie « inconnue » à une case vide.

Traiter la colonne numérique :

```python
    result["distance_km"] = pd.to_numeric(result["distance_km"], errors="coerce")
    result["distance_km"] = result["distance_km"].fillna(result["distance_km"].median())
```

- `pd.to_numeric(..., errors="coerce")` → convertit en nombre ; ce qui n'est pas convertible devient `NaN` (`coerce` = « force »), sans faire planter le programme.
- `.median()` → la **médiane** (valeur du milieu) des distances. On remplit les vides par la médiane : c'est robuste aux valeurs extrêmes.
  **Décision explicite** : numérique manquant → médiane.

Dernière vérification :

```python
    if not result["delivery_id"].is_unique:
        raise ValueError("Duplicate delivery_id detected")

    return result
```

- `.is_unique` → `True` si toutes les valeurs sont uniques. Si ce n'est pas le cas, on lève une erreur (preuve que la déduplication a bien marché).
- `return result` → renvoie le tableau propre.

---

## Étape 6 — `save_processed` : écrire le résultat

```python
def save_processed(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
```

- `path.parent.mkdir(parents=True, exist_ok=True)` → crée le dossier de destination s'il n'existe pas (`parents=True` crée toute l'arborescence, `exist_ok=True` évite une erreur s'il existe déjà).
- `df.to_csv(path, index=False)` → écrit le CSV. `index=False` évite d'ajouter la colonne numérotée automatique de pandas.

---

## Étape 7 — `main` : assembler et lancer

```python
def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_TARGET

    raw = extract(source)
    clean = transform(raw)
    save_processed(clean, target)

    print(f"source      : {source}")
    print(f"lignes brutes : {len(raw)}")
    print(f"lignes clean  : {len(clean)}")
    print(f"nulls restants: {int(clean[list(REQUIRED_COLUMNS)].isna().sum().sum())}")
    print(f"écrit         : {target}")


if __name__ == "__main__":
    main()
```

- `sys.argv` → la liste des **arguments** passés en ligne de commande. `sys.argv[0]` = le script ; `[1]` = 1er argument, etc. Ici : si tu donnes un chemin en argument, il est utilisé ; sinon on prend le défaut.
- `len(raw)` / `len(clean)` → nombre de lignes.
- `clean[list(REQUIRED_COLUMNS)].isna().sum().sum()` → double `.sum()` : la 1re compte les vides par colonne, la 2e additionne tout → nombre total de vides restants (doit être 0).
- `if __name__ == "__main__":` → **garde classique Python** : `main()` ne se lance que si tu exécutes ce fichier directement (pas si un autre script l'importe).

---

## Étape 8 — Exécuter et vérifier

```bash
python etl.py
```

Attendu :

```text
lignes brutes : 13
lignes clean  : 12
nulls restants: 0
```

Le fichier `deliveries_clean.csv` est créé dans `solution/`.
Tu peux aussi choisir les chemins :

```bash
python etl.py ../LAB_01_JSON_JUPYTER_PANDAS/data/deliveries_lab.json /tmp/out.csv
```

---

## Récapitulatif des décisions de nettoyage

| Problème | Décision | Code |
|---|---|---|
| Doublon `delivery_id` | garder la 1re occurrence | `drop_duplicates(..., keep="first")` |
| Ville mal écrite | majuscules/espaces retirés | `.str.strip().str.lower()` |
| `traffic_level` / `weather` vides | remplacer par `"unknown"` | `.fillna("unknown")` |
| `distance_km` vide | remplacer par la médiane | `.fillna(.median())` |

---

## Erreurs fréquentes

| Message | Cause | Solution |
|---|---|---|
| `FileNotFoundError` | mauvais chemin | utilise `main()` (chemins par défaut) ou passe le bon chemin |
| `KeyError: 'delivery_id'` | JSON différent | vérifie la source passée en argument |
| `TypeError: 'ellipsis' object` | `df = ...` non remplacé dans le starter | implémente `extract` |
| `ValueError: Missing columns` | tu testes `transform` sur un tableau incomplet | c'est voulu : le schéma est protégé |

---

## Mini-glossaire final

```text
ETL         → Extract, Transform, Load
fonction    → bloc de code nommé, réutilisable
raise       → déclencher volontairement une erreur
FileNotFoundError / ValueError → types d'erreurs
drop_duplicates → supprimer les doublons
fillna      → remplir les cases vides
median()    → valeur du milieu (robuste)
is_unique   → "toutes les valeurs sont-elles uniques ?"
__main__    → "ce fichier est-il exécuté directement ?"
```
