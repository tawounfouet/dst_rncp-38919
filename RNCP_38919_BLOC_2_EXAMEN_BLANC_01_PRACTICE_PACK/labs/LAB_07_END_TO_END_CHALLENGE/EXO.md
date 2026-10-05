# LAB 07 — Mode examen (sans filet)

⏱ **60 min**, chrono lancé, **aucune** consultation des labs 01→06.

## Règle d'or

> Bloqué > 3 min sur un point → note-le et **passe au suivant**. Tu reviendras.

## Checklist de contrôle par bloc

- [ ] **Exploration (10 min)** : `shape`, `dtypes`, nulls, doublons, valeurs de `customer_city`
- [ ] **ETL (10 min)** : `extract / validate_schema / transform / save_processed`
- [ ] **DB/ORM/ingestion (15 min)** : compose up, modèles 1‑N, ingestion idempotente
- [ ] **ML (13 min)** : pipeline num/cat, split stratifié, métriques, `joblib`
- [ ] **Tests (7 min)** : 3 tests (schéma, doublon, happy path)
- [ ] **Doc (5 min)** : architecture ASCII

## Commandes de survie (à retrouver de mémoire)

```bash
# DB
cp .env.example .env && docker compose up -d
docker compose exec db mariadb -u<user> -p<pass> <db> -e "SHOW TABLES;"

# tests
pytest -q

# ML
python src/train_model.py
```

## Corrigés condensés (à n'ouvrir qu'APRÈS le chrono)

<details>
<summary>ETL (extrait)</summary>

```python
def transform(df):
    validate_schema(df)
    r = df.drop_duplicates(subset=["delivery_id"], keep="first").copy()
    for c in ["customer_city", "vehicle_type"]:
        r[c] = r[c].astype("string").str.strip().str.lower()
    for c in ["traffic_level", "weather"]:
        r[c] = r[c].astype("string").str.strip().str.lower().fillna("unknown")
    r["distance_km"] = pd.to_numeric(r["distance_km"], errors="coerce")
    r["distance_km"] = r["distance_km"].fillna(r["distance_km"].median())
    return r
```
</details>

<details>
<summary>ORM 1‑N (extrait)</summary>

```python
class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True)
    customer_city = Column(String(100), nullable=False)
    deliveries = relationship("Delivery", back_populates="customer")

class Delivery(Base):
    __tablename__ = "deliveries"
    delivery_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    customer = relationship("Customer", back_populates="deliveries")
```
</details>

<details>
<summary>Ingestion idempotente (extrait)</summary>

```python
def ingest(df, engine):
    validate_dataframe(df)
    ensure_table(engine)
    known = existing_ids(engine)
    new = df[~df["delivery_id"].isin(known)]
    if not new.empty:
        new.to_sql("deliveries", engine, if_exists="append", index=False)
    return len(new)   # 0 à la 2e passe
```
</details>

<details>
<summary>ML (extrait)</summary>

```python
preprocessing = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), ["distance_km"]),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]), ["customer_city", "vehicle_type", "traffic_level", "weather"]),
])
pipeline = Pipeline([("preprocessing", preprocessing),
                     ("model", LogisticRegression(max_iter=1000))])
```
</details>

## Post-mortem

Remplir [`POST_MORTEM_TEMPLATE.md`](POST_MORTEM_TEMPLATE.md) **immédiatement**
après le chrono, à chaud.

| Bloc | Temps réel | Objectif | Écart |
|---|---:|---:|---:|
| Exploration | | 10 | |
| ETL | | 10 | |
| DB/ORM/ingestion | | 15 | |
| ML | | 13 | |
| Tests | | 7 | |
| Doc | | 5 | |

## Auto-évaluation

| Point | OK ? |
|---|---|
| J'ai tenu le chrono | |
| J'ai un rendu fonctionnel en 60 min | |
| J'ai identifié mon bloc le plus lent | |
| J'ai un plan d'automatisation avant l'examen 4 h | |
