# LAB 02 — Mode examen

⏱ **35 min**. Implémentez les 4 fonctions, puis testez les cas d'erreur.

## Checklist chronométrée

- [ ] 0–8 : `extract`
- [ ] 8–13 : `validate_schema`
- [ ] 13–28 : `transform` (dédup, normalisation, imputation)
- [ ] 28–35 : `save_processed` + `main`

## Pièges classiques

1. `df.drop_duplicates(...)` renvoie une **copie** → attention au `SettingWithCopyWarning`.
2. La médiane doit être calculée **après** `to_numeric` avec `errors="coerce"`.
3. `fillna("unknown")` sur des colonnes catégorielles avant `.str` peut casser.
4. `validate_schema` doit être appelé **au début** de `transform`.

## Solution

<details>
<summary>extract</summary>

```python
def extract(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_json(path)
```
</details>

<details>
<summary>validate_schema</summary>

```python
def validate_schema(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
```
</details>

<details>
<summary>transform</summary>

```python
def transform(df: pd.DataFrame) -> pd.DataFrame:
    validate_schema(df)
    result = df.copy()
    result = result.drop_duplicates(subset=["delivery_id"], keep="first").copy()

    for col in ["customer_city", "vehicle_type"]:
        result[col] = result[col].astype("string").str.strip().str.lower()

    for col in ["traffic_level", "weather"]:
        result[col] = (
            result[col].astype("string").str.strip().str.lower().fillna("unknown")
        )

    result["distance_km"] = pd.to_numeric(result["distance_km"], errors="coerce")
    result["distance_km"] = result["distance_km"].fillna(result["distance_km"].median())

    if not result["delivery_id"].is_unique:
        raise ValueError("Duplicate delivery_id detected")

    return result
```
</details>

<details>
<summary>save_processed</summary>

```python
def save_processed(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
```
</details>

## Auto-évaluation

| Point | OK ? |
|---|---|
| Je code un ETL en fonctions pures | |
| Je pense aux cas d'erreur (fichier/colonne) | |
| Je dédoublonne sur la bonne clé | |
| Je sais imputer numérique vs catégoriel | |
| Je gère les chemins avec `pathlib` | |
