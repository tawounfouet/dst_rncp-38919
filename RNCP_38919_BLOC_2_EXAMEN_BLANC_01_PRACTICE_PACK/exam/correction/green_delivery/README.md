# GreenDelivery — Corrigé complet (Examen blanc 01)

Solution de référence complète du `starter_project`, alignée sur le corrigé
`../12_RNCP_38919_BLOC_2_CORRIGE_EXAMEN_BLANC_01.md`.

> Contrairement au document `.md` (qui montre le code), ce dossier est un
> **projet réellement exécutable**, testé de bout en bout.

## Arborescence

```text
green_delivery/
├── data/
│   ├── raw/deliveries.json
│   └── processed/deliveries_clean.csv   # généré par l'ETL
├── notebooks/01_exploration.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py            # DATABASE_URL depuis .env
│   ├── etl.py
│   ├── database.py
│   ├── models.py
│   ├── create_database.py
│   ├── ingest.py
│   └── train_model.py
├── tests/
│   ├── test_etl.py
│   └── test_ingest_idempotent.py        # intégration (opt-in)
├── models/model.joblib                  # généré par l'entraînement
├── docker-compose.yml
├── .env.example
├── conftest.py                          # rend `src` importable sous pytest
├── requirements.txt
├── ARCHITECTURE.md
└── README.md
```

## Démarrage rapide

```bash
cd green_delivery
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

docker compose up -d
docker compose ps
```

> Si le port `3306` est déjà occupé, changez `DB_PORT` dans `.env`
> **et** dans `docker-compose.yml` (le même `.env` est utilisé pour les deux).

## Exécution du pipeline

```bash
python -m src.etl              # 24 → 23 lignes, écrit data/processed/deliveries_clean.csv
python -m src.create_database  # crée customers + deliveries
python -m src.ingest           # insère 22 customers et 23 deliveries (idempotent)
python -m src.train_model      # entraîne + écrit models/model.joblib
pytest -v                      # tests unitaires
```

Test d'intégration (base démarrée) :

```bash
RUN_DB_TESTS=1 pytest -v
```

## Résultats attendus

```text
deliveries_clean.csv : 23 lignes, 0 doublon, 0 null
customers            : 22
deliveries           : 23
model.joblib         : présent
accuracy ≈ 0.7143 · precision ≈ 1.0 · recall ≈ 0.3333 · f1 ≈ 0.5
```

## Corrections apportées par rapport au `.md`

1. **`conftest.py`** ajouté : sans lui, `pytest` échoue avec
   `ModuleNotFoundError: No module named 'src'` selon la façon d'invoquer pytest.
2. **Chemins robustes** (`Path(__file__)`) dans `etl.py`, `ingest.py`,
   `train_model.py` : exécutables depuis n'importe quel dossier.
3. **`load_dotenv(PROJECT_ROOT / ".env")`** : charge le `.env` du projet même
   si on lance depuis un sous-dossier.
4. **`ingest()` retourne les compteurs** d'insertion → vérification immédiate
   de l'idempotence (`(22, 23)` puis `(0, 0)`).
5. **Matrice de confusion** affichée par `train_model.py`.

Le reste du code suit fidèlement les choix du corrigé écrit.

## Détails

Voir [`ARCHITECTURE.md`](ARCHITECTURE.md) pour le schéma complet, les choix
techniques, l'impact écologique et les limites.
