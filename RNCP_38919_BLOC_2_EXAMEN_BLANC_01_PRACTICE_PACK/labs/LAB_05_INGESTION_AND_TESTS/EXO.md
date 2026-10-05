# LAB 05 — Mode examen

⏱ **35 min**. Objectif : `pytest -q` → **7 passed**, et `ingest.py` → **0** à la 2e passe.

## Checklist chronométrée

- [ ] 0–8 : `validate_dataframe` (3 cas)
- [ ] 8–18 : `ingest` (table + filtre des IDs connus)
- [ ] 18–28 : tests validation + idempotence
- [ ] 28–35 : `main()` deux passes

## Questions de contrôle

1. Pourquoi une DB **fichier** (`tmp_path`) plutôt que `:memory:` en test ?
2. Que doit retourner `ingest` pour prouver l'idempotence ?
3. `isna()` vs `duplicated()` : quel cas couvre chacun ?
4. Un test qui ne fait que `pass` est-il un test ?

## Solution

<details>
<summary>validation.py</summary>

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
</details>

<details>
<summary>ingest.py</summary>

```python
from sqlalchemy import create_engine, text

def ingest(df, engine) -> int:
    validate_dataframe(df)
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS deliveries (
                delivery_id INTEGER PRIMARY KEY, customer_id INTEGER,
                customer_city TEXT, vehicle_type TEXT, distance_km REAL,
                traffic_level TEXT, weather TEXT, delivery_minutes INTEGER,
                late_delivery INTEGER
            )
        """))
    with engine.connect() as conn:
        known = {r[0] for r in conn.execute(text("SELECT delivery_id FROM deliveries"))}
    new = df[~df["delivery_id"].isin(known)]
    if not new.empty:
        new.to_sql("deliveries", engine, if_exists="append", index=False)
    return len(new)
```
</details>

<details>
<summary>test_ingest.py (idempotence)</summary>

```python
@pytest.fixture
def engine(tmp_path):
    return create_engine(f"sqlite:///{tmp_path / 'deliveries.sqlite'}")

def test_reingestion_does_not_duplicate(engine):
    ingest(sample_df(), engine)
    assert ingest(sample_df(), engine) == 0
```
</details>

## Pièges

- `:memory:` crée une base **par connexion** → utiliser un fichier (`tmp_path`).
- `df["delivery_id"].isna()` avant `duplicated()` : un `NaN` dupliqué compte deux fois.
- `to_sql(..., if_exists="append")` **ne dédoublonne pas** tout seul.
- Ne jamais tester contre une DB réelle partagée : tests non isolés = tests flaky.

## Auto-évaluation

| Point | OK ? |
|---|---|
| J'écris des tests des cas d'erreur | |
| Je comprends l'idempotence d'ingestion | |
| J'isole mes tests (fixtures `tmp_path`) | |
| Je ne laisse pas de tests vides « verts » | |
