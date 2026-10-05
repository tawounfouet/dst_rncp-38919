# LAB 05 — Ingestion fiable + pytest

**Temps cible : 35 min** · Difficulté : ⭐⭐⭐ · Prérequis : LAB 02

## Objectifs

- valider la conformité d'un DataFrame (`validate_dataframe`) ;
- ingérer des données de façon **idempotente** (`ingest`) ;
- écrire des tests pytest couvrant : erreurs, doublons, schéma, happy path.

## Contenu

```text
LAB_05_INGESTION_AND_TESTS/
├── starter/
│   ├── validation.py        # validate_dataframe à compléter
│   ├── ingest.py            # ingest à compléter
│   └── test_validation.py   # 3 tests marqués TODO (rouges au départ)
├── solution/
│   ├── validation.py
│   ├── ingest.py            # SQLite, idempotent
│   ├── test_validation.py   # 3 tests (validation)
│   └── test_ingest.py       # 4 tests (idempotence)
├── EXO.md
└── README.md
```

## Lancement

```bash
cd LAB_05_INGESTION_AND_TESTS/solution
pytest -v
python ingest.py
```

Attendu :

```text
7 passed
1re ingestion : 12 ligne(s) insérée(s)
2e  ingestion : 0 ligne(s) insérée(s)  <- doit valoir 0
total en base : 12
```

## Comportements à implémenter

`validate_dataframe(df)` doit lever une `ValueError` si :

| Cas | Message indicatif |
|---|---|
| colonne requise absente | `Missing columns: [...]` |
| `delivery_id` nul | `Null delivery_id detected` |
| `delivery_id` dupliqué | `Duplicate delivery_id detected` |

`ingest(df, engine) -> int` doit :

- valider via `validate_dataframe` ;
- créer la table si besoin ;
- n'insérer que les `delivery_id` **inconnus** ;
- retourner le nombre de lignes **réellement insérées** (0 à la ré-ingestion).

## Critères de réussite

- [ ] les 7 tests passent (`pytest -q`) ;
- [ ] le starter affiche **3 failed** (pas de faux vert) ;
- [ ] `python ingest.py` affiche `0` à la seconde ingestion ;
- [ ] `validate_dataframe` traite les 3 cas d'erreur ;
- [ ] les tests utilisent une DB **isolée** (`tmp_path`), pas de fichier partagé.

## Dépannage

| Symptôme | Cause | Correctif |
|---|---|---|
| starter `3 passed` | tests vides sans assertion (ancienne version) | les tests starter utilisent désormais `pytest.fail(...)` → **3 failed** attendu |
| `ValueError: Duplicate delivery_id` | donnée non dédupliquée en amont | dédupliquer avec l'ETL du LAB 02 avant d'ingérer |
| `sqlite3.OperationalError: table deliveries already exists` | table pré-existante | `CREATE TABLE IF NOT EXISTS` (déjà utilisé) ; supprimer `deliveries.sqlite` pour repartir |
| `ModuleNotFoundError: validation` | mauvaise racine de test | lancer `pytest` depuis `solution/` |
| tests qui passent en local mais pas en in-memory | connexions SQLite distinctes | utiliser une DB fichier via `tmp_path` (fait dans la solution) |

> **Correctif apporté :** le starter passait `3 passed` avec des tests vides
> (`pass`), donnant l'illusion de réussite. Les tests starter échouent désormais
> explicitement. L'`ingest()` promis par le README (absent auparavant) est fourni.

## Pour aller plus loin

- Remplacer SQLite par la MariaDB du LAB 03/04 (`DATABASE_URL`).
- Ajouter un `@pytest.mark.parametrize` pour tester plusieurs colonnes manquantes.
- Mesurer la couverture : `pytest --cov=. --cov-report=term-missing`.
