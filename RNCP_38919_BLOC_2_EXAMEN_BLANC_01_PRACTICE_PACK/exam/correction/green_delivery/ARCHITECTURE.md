# GreenDelivery — Architecture

Corrigé complet de l'examen blanc 01 (RNCP 38919 — Bloc 2).

## 1. Contexte

GreenDelivery collecte des événements de livraison urbaine au format JSON.
Le projet transforme ces événements, les charge dans une base relationnelle
et entraîne un modèle de classification du retard.

Chaîne couverte :

```text
JSON → ETL → DB ORM → ingestion → ML → tests → documentation
```

## 2. Architecture

```text
deliveries.json
      │
      ▼
Jupyter / pandas          (notebooks/01_exploration.ipynb)
      │
      ▼
ETL Python                (src/etl.py)
      │
      ▼
deliveries_clean.csv      (data/processed/)
      │
      ├───────────────┐
      │               │
      ▼               ▼
SQLAlchemy ORM    scikit-learn
(src/models.py)   (src/train_model.py)
      │               │
      ▼               ▼
MariaDB (Docker)  model.joblib
      │
      ▼
phpMyAdmin
      │
      ▼
Tests / contrôle          (tests/)
```

## 3. Pipeline ETL

`src/etl.py` expose quatre fonctions :

| Fonction | Rôle |
|---|---|
| `extract(path)` | lit le JSON, `FileNotFoundError` si absent |
| `validate_schema(df)` | `ValueError` si une colonne requise manque |
| `transform(df)` | nettoie et renvoie un DataFrame propre |
| `save_processed(df, path)` | écrit le CSV |

Décisions de nettoyage (explicites et reproductibles) :

```text
delivery_id dupliqué   → conserver la première occurrence
distance_km manquant   → imputation par la médiane (8.45 km)
traffic_level manquant → "unknown"
weather manquant       → "unknown"
customer_city          → strip() + lower()
vehicle_type           → strip() + lower()
```

Résultat : **24 lignes brutes → 23 livraisons propres, 0 doublon, 0 null.**

## 4. Modèle relationnel

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
customer_id      FK → customers.customer_id
vehicle_type
distance_km
traffic_level
weather
delivery_minutes
late_delivery
```

- `customer_id` est la PK de `customers` : il identifie un client.
- `delivery_id` est la PK de `deliveries` : le grain est la livraison.
- La FK est portée par `deliveries.customer_id` (côté N).
- Cardinalité : **1 Customer → N Deliveries**.

## 5. Docker / Compose

`docker-compose.yml` déclare :

- un service `db` (`mariadb:11`) avec volume nommé `db_data` (persistance) ;
- un service `phpmyadmin` ;
- des variables d'environnement injectées depuis `.env`.

```bash
docker compose up -d
docker compose ps
docker compose logs db
```

## 6. ORM et création des tables

- `src/database.py` : `engine` + `Session` construits depuis `DATABASE_URL`.
- `src/models.py` : `Customer` et `Delivery` (PK, FK, `relationship`).
- `src/create_database.py` : `Base.metadata.create_all(engine, checkfirst=True)`.

Les credentials ne sont **pas** dupliqués dans le code : `src/config.py`
les lit depuis `.env` (`python-dotenv`).

## 7. Ingestion

`src/ingest.py` insère d'abord les `customers`, puis les `deliveries`
(pour respecter la FK). L'ingestion est **idempotente** : chaque ID déjà
présent est ignoré.

```text
1re ingestion : customers → 22, deliveries → 23
2e  ingestion : customers → 22, deliveries → 23  (0 ajout)
```

## 8. Machine Learning

- Cible : `late_delivery`.
- Features : `customer_city`, `vehicle_type`, `distance_km`, `traffic_level`, `weather`.
- Exclusions justifiées :
  - `delivery_id` : identifiant technique ;
  - `customer_id` : forte cardinalité, peu utile ici ;
  - `delivery_minutes` : **fuite d'information** si la prédiction a lieu avant la livraison.
- Preprocessing dans la pipeline : imputation + `OneHotEncoder(handle_unknown="ignore")`.
- Modèle : `LogisticRegression(max_iter=1000)`.
- Split : `test_size=0.30`, `random_state=42`, `stratify=y`.
- Sauvegarde : pipeline complète via `joblib.dump` → `models/model.joblib`.

Résultats de référence : accuracy ≈ 0.7143, precision ≈ 1.0, recall ≈ 0.3333, f1 ≈ 0.5.

**Interprétation** : le pipeline fonctionne techniquement, mais 7 observations
en test ne permettent aucune conclusion sur la performance réelle.

## 9. Tests

- `tests/test_etl.py` : schéma, colonne manquante, doublon, normalisation,
  imputation, fichier absent.
- `tests/test_ingest_idempotent.py` : test d'intégration (nécessite la DB,
  activé par `RUN_DB_TESTS=1`).

```bash
pytest -v
```

## 10. Impact écologique

Postes de consommation :

```text
ordinateur / VM, base MariaDB, phpMyAdmin, Python ETL,
entraînement ML (marginal ici), stockage, Docker
```

Ordre de grandeur : `Énergie (kWh) = Puissance (kW) × Durée (h)`.
Exemple illustratif : 50 W pendant 10 min ≈ 0,0083 kWh (pas une mesure réelle).

Leviers de réduction :

1. arrêter les containers inutilisés (`docker compose down`) ;
2. ne traiter que les nouvelles données (ingestion incrémentale) ;
3. dimensionner les ressources au besoin / éviter les recalculs.

Limites : pas de mesure matérielle directe, puissance machine inconnue,
coût du stockage et facteur carbone non estimés.

## 11. Limites

- Dataset volontairement très petit → métriques ML instables.
- Pas de tests automatisés sur la base en CI.
- Preprocessing ML non versionné (`model.joblib` uniquement).

## 12. Pistes d'amélioration

- collecter davantage de données ;
- ajouter des variables temporelles (heure, jour, zone) ;
- comparer plusieurs modèles (`RandomForest`, `GradientBoosting`) ;
- ingestion incrémentale et tests d'intégration en CI ;
- mesurer réellement la consommation énergétique.
