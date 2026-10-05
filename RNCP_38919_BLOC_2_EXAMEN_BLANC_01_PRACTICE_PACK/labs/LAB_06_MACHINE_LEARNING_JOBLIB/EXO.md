# LAB 06 — Mode examen

⏱ **40 min**. Écrivez la pipeline de `starter/train_model.py` de zéro.

## Checklist chronométrée

- [ ] 0–6 : charger le CSV, choisir `X` / `y`
- [ ] 6–16 : `ColumnTransformer` (num + cat)
- [ ] 16–22 : `train_test_split` stratifié
- [ ] 22–30 : `Pipeline` + `fit` + métriques
- [ ] 30–36 : `joblib.dump`
- [ ] 36–40 : réflexion sur la fuite de données

## Questions de contrôle

1. Pourquoi mettre l'imputer **dans** la pipeline et pas avant le split ?
2. Quel est le risque d'utiliser `delivery_minutes` comme feature ?
3. À quoi sert `stratify=y` sur une cible déséquilibrée ?
4. Que contient concrètement `model.joblib` ?

## Solution

<details>
<summary>Pipeline complète</summary>

```python
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE_DIR / "data" / "deliveries_ml.csv")

numeric_features = ["distance_km"]
categorical_features = ["customer_city", "vehicle_type", "traffic_level", "weather"]

X = df[numeric_features + categorical_features]
y = df["late_delivery"]

preprocessing = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), numeric_features),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]), categorical_features),
])

pipeline = Pipeline([
    ("preprocessing", preprocessing),
    ("model", LogisticRegression(max_iter=1000)),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
pipeline.fit(X_train, y_train)
pred = pipeline.predict(X_test)

print("accuracy :", accuracy_score(y_test, pred))
print("precision:", precision_score(y_test, pred, zero_division=0))
print("recall   :", recall_score(y_test, pred, zero_division=0))
print("f1       :", f1_score(y_test, pred, zero_division=0))

(BASE_DIR / "models").mkdir(exist_ok=True)
joblib.dump(pipeline, BASE_DIR / "models" / "model.joblib")
```
</details>

## Pièges

- Imputer/encoder **avant** le split → fuite de données.
- Oublier `handle_unknown="ignore"` → crash en production sur une ville inconnue.
- `joblib.dump` du **modèle seul** au lieu de la pipeline → reprocessing manuel.
- Pas de `random_state` → résultats non reproductibles à l'oral.

## Auto-évaluation

| Point | OK ? |
|---|---|
| Je construis un `ColumnTransformer` num/cat | |
| Je sais pourquoi la pipeline englobe le preprocessing | |
| J'explique la fuite de `delivery_minutes` | |
| Je sérialise et recharge le modèle | |
| Mes résultats sont reproductibles | |
