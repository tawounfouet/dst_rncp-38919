# LAB 01 — Mode examen

⏱ **30 min**. Ne dépliez les solutions qu'après avoir essayé (règle : 10 min
bloqué → on regarde l'indice, pas la solution).

## Checklist chronométrée

- [ ] 0–5 : charger le JSON dans un DataFrame
- [ ] 5–10 : `head`, `shape`, `columns`, `info`
- [ ] 10–15 : nulls + doublons
- [ ] 15–22 : normaliser `customer_city`
- [ ] 22–30 : les 2 graphiques

## Questions de contrôle (répondre de tête)

1. Différence entre `df.shape` et `len(df)` ?
2. Pourquoi `df["customer_city"].value_counts()` peut rater des valeurs ?
3. `df.duplicated()` compte-t-il la première occurrence ?

## Solution

<details>
<summary>1. Charger le JSON</summary>

```python
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = Path("../data/deliveries_lab.json")   # depuis starter/ ou solution/
df = pd.read_json(DATA_PATH)
```
</details>

<details>
<summary>2. Structure</summary>

```python
print(df.shape)                 # (13, 9)
print(df.columns.tolist())
df.info()
```
</details>

<details>
<summary>3. Nulls et doublons</summary>

```python
print(df.isna().sum())
print("Doublons:", df.duplicated().sum())   # Doublons: 1
```
</details>

<details>
<summary>4. Normaliser customer_city</summary>

```python
df["customer_city"] = (
    df["customer_city"].astype("string").str.strip().str.lower()
)
print(df["customer_city"].value_counts(dropna=False))
```
`astype("string")` évite les erreurs si la colonne contient des `NaN` ;
`strip()` + `lower()` fusionnent `PARIS`, `" Paris "` et `paris`.
</details>

<details>
<summary>5. Distribution de late_delivery</summary>

```python
df["late_delivery"].value_counts().sort_index().plot(kind="bar")
plt.title("Distribution de late_delivery")
plt.show()
```
</details>

<details>
<summary>6. Histogramme distance_km</summary>

```python
df["distance_km"].hist()
plt.title("Distribution de distance_km")
plt.show()
```
</details>

## Auto-évaluation

| Point | OK ? |
|---|---|
| Je charge un JSON en une ligne | |
| Je connais `shape` / `info` / `isna` / `duplicated` | |
| Je normalise une catégorie sans casser les `NaN` | |
| Je fais un bar chart et un histogramme sans chercher | |
