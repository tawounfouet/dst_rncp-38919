# LAB 06 — Guide débutant (de zéro à la solution)

> **Public** : tu n'as jamais fait de machine learning. On explique chaque notion
> (feature, cible, entraînement, encodage, métrique…) au moment où elle apparaît.
> À la fin, tu auras entraîné un modèle **et** l'auras sauvegardé dans un fichier.

Le but : prédire `late_delivery` (0 = à l'heure, 1 = en retard).

---

## Étape 0 — Le vocabulaire du machine learning

| Mot | Signification simple |
|---|---|
| **Machine learning** | Faire « apprendre » à l'ordinateur à partir d'exemples, au lieu de programmer des règles à la main. |
| **Classification** | Prédire une **catégorie** (ici : en retard ou non). |
| **Features (X)** | Les colonnes **d'entrée** qui servent à prédire (ville, distance…). |
| **Target (y)** | La colonne à **prédire** (`late_delivery`). |
| **Entraînement (fit)** | L'étape où le modèle « apprend » à partir de X et y. |
| **Train / test split** | On garde une partie des données **cachée** pour vérifier le modèle. |
| **Encodage** | Transformer du texte en nombres (le modèle ne comprend que les nombres). |
| **Pipeline** | Une chaîne : préparation → modèle, exécutée d'un bloc. |
| **joblib** | L'outil qui **sauvegarde** le modèle dans un fichier. |

---

## Étape 1 — L'environnement

```bash
cd LAB_06_MACHINE_LEARNING_JOBLIB
python3 -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt
```

Données : `data/deliveries_ml.csv` (fourni par le lab).

---

## Étape 2 — Charger les données

```python
from pathlib import Path

import joblib
import pandas as pd
# ...imports scikit-learn...

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "deliveries_ml.csv"
MODEL_PATH = BASE_DIR / "models" / "model.joblib"

df = pd.read_csv(DATA_PATH)
```

- On lit un **CSV** avec `read_csv` (comme `read_json` au LAB 01).
- `BASE_DIR` + chemins relatifs au script → exécutable **depuis n'importe où**.

---

## Étape 3 — Séparer les entrées (X) et la cible (y)

```python
numeric_features = ["distance_km"]
categorical_features = ["customer_city", "vehicle_type", "traffic_level", "weather"]

X = df[numeric_features + categorical_features]
y = df["late_delivery"]
```

- `numeric_features` → colonnes **numériques**.
- `categorical_features` → colonnes **catégorielles** (du texte : des catégories).
- `X` → le tableau des entrées (les deux listes réunies).
- `y` → la cible à prédire.

**Colonnes volontairement exclues de X :**

```text
delivery_id      → identifiant, aucune valeur prédictive
customer_id      → identifiant, beaucoup trop de valeurs pour ce petit jeu
delivery_minutes → la durée réelle : connue seulement APRÈS la livraison
```

Exclure `delivery_minutes` évite une **fuite de données** (*data leakage*) : utiliser
une information qu'on n'aurait **pas** au moment de la prédiction donne un faux
sentiment de performance.

---

## Étape 4 — Préparer les colonnes (imputation + encodage)

Deux problèmes à régler :

- les **valeurs manquantes** (imputation) ;
- les **textes** que le modèle ne sait pas lire (encodage en nombres).

### Pipeline numérique

```python
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
])
```

- `SimpleImputer(strategy="median")` → remplit les vides par la **médiane**.
- `Pipeline([...])` → une **chaîne d'étapes** appliquées dans l'ordre.

### Pipeline catégoriel

```python
from sklearn.preprocessing import OneHotEncoder

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])
```

- `strategy="most_frequent"` → pour du texte, on remplit le vide par la **valeur la plus fréquente**.
- `OneHotEncoder` → transforme chaque catégorie en colonnes de `0/1`.
  Exemple : `vehicle_type = bike` devient `vehicle_type_bike = 1`, `vehicle_type_car = 0`, etc.
- `handle_unknown="ignore"` → si une catégorie **inconnue** arrive plus tard (ex. une ville jamais vue), on ne plante pas : elle est ignorée. Indispensable en production.

### Réunir les deux

```python
from sklearn.compose import ColumnTransformer

preprocessing = ColumnTransformer(
    transformers=[
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
        ]), numeric_features),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]), categorical_features),
    ]
)
```

- `ColumnTransformer` → applique **une préparation différente selon la colonne** : le pipeline `num` aux colonnes numériques, le pipeline `cat` aux colonnes catégorielles.

**À retenir** : la préparation est **dans** la pipeline, pas avant le split.
Sinon le modèle « verrait » des informations du test pendant l'entraînement (fuite).

---

## Étape 5 — Assembler modèle + préparation

```python
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ("preprocessing", preprocessing),
    ("model", LogisticRegression(max_iter=1000)),
])
```

- La pipeline finale enchaîne : **préparation → modèle**.
- `LogisticRegression` → un modèle de classification simple, robuste et explicable (adapté à un petit jeu).
- `max_iter=1000` → nombre maximum d'itérations d'apprentissage (sinon scikit-learn s'arrête parfois trop tôt).

---

## Étape 6 — Séparer entraînement / test, puis entraîner

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

pipeline.fit(X_train, y_train)
pred = pipeline.predict(X_test)
```

- `train_test_split` → coupe en deux : **70 % pour apprendre** (`train`), **30 % pour vérifier** (`test`).
- `test_size=0.30` → la proportion de test.
- `random_state=42` → **reproductibilité** : le même tirage à chaque exécution.
- `stratify=y` → garde la **même proportion** de 0 et de 1 dans le train et le test (essentiel quand les classes sont déséquilibrées ou le jeu petit).
- `pipeline.fit(X_train, y_train)` → **entraînement** (apprentissage).
- `pipeline.predict(X_test)` → **prédictions** sur les données de test (jamais vues).

---

## Étape 7 — Mesurer la performance

```python
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

print("accuracy :", accuracy_score(y_test, pred))
print("precision:", precision_score(y_test, pred, zero_division=0))
print("recall   :", recall_score(y_test, pred, zero_division=0))
print("f1       :", f1_score(y_test, pred, zero_division=0))
```

| Métrique | Question à laquelle elle répond |
|---|---|
| **accuracy** | Sur toutes les prédictions, combien sont correctes ? |
| **precision** | Parmi celles que j'ai prédites « en retard », combien le sont vraiment ? |
| **recall** | Parmi les vraies « en retard », combien ai-je su en détecter ? |
| **f1** | Moyenne équilibrée entre precision et recall. |

- `zero_division=0` → évite une erreur de calcul si le modèle ne prédit jamais la classe 1.

Résultat attendu sur ce petit jeu :

```text
accuracy : 0.714...
precision: 1.0
recall   : 0.333...
f1       : 0.5
```

**Interprétation importante** : ces scores ne prouvent **pas** que le modèle est bon.
Le jeu est **très petit** (7 observations en test). Une différence de 1 ou 2 cas
fait beaucoup bouger les métriques. La bonne conclusion : « la chaîne fonctionne,
mais il faudrait beaucoup plus de données pour conclure ».

---

## Étape 8 — Sauvegarder le modèle

```python
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(pipeline, MODEL_PATH)
```

- `.parent.mkdir(...)` → crée le dossier `models/` s'il n'existe pas.
- `joblib.dump(pipeline, ...)` → **enregistre la pipeline complète** (préparation + modèle) dans un fichier.

**Pourquoi la pipeline entière et pas juste le modèle ?** Parce qu'en production,
il faudra **la même préparation** (mêmes imputations, même encodage) avant de
prédire. En sauvegardant tout d'un bloc, on ne peut pas se tromper.

### Recharger et prédire

```python
import joblib

pipeline = joblib.load("models/model.joblib")
pipeline.predict([[4.2, "paris", "bike", "high", "rain"]])
```

---

## Étape 9 — Lancer et vérifier

```bash
python solution/train_model.py
```

Attendu :

```text
accuracy : 0.714...
precision: 1.0
recall   : 0.333...
f1       : 0.5
modèle   : .../models/model.joblib
```

Le fichier `models/model.joblib` est créé. Lance le script **depuis n'importe où** :
les chemins sont basés sur le fichier (`Path(__file__)`).

---

## Erreurs fréquentes

| Message | Cause | Solution |
|---|---|---|
| `FileNotFoundError: data/deliveries_ml.csv` | mauvais dossier (ancien chemin relatif) | la solution utilise `Path(__file__)` ; sinon `cd` dans le dossier du lab |
| `could not convert string to float` | catégories non encodées | garder `ColumnTransformer` + `OneHotEncoder` |
| `ValueError: unknown categories` | encodeur sans `handle_unknown` | `OneHotEncoder(handle_unknown="ignore")` |
| métriques instables | pas de `random_state` | fixer `random_state=42` |

---

## Mini-glossaire final

```text
feature / X    → les entrées
target / y     → la valeur à prédire
fit            → entraîner
predict        → prédire
split          → séparer train/test
stratify       → garder les proportions de classes
imputer        → remplir les vides
encoder        → transformer du texte en nombres
pipeline       → préparation + modèle enchaînés
joblib.dump    → sauvegarder le modèle
fuite de données → utiliser une info indisponible au moment de la prédiction
```
