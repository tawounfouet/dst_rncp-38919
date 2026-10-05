# Simulation — Examen Blanc Bloc 2 (4 h)

Kit clé en main pour t'entraîner en conditions réelles, puis t'auto-corriger.

## 1. Préparer

```bash
cd simulation
./start_mock_exam.sh
```

Crée `candidate_workspace/` (copie propre du `starter_project`), installe les
dépendances dans un venv dédié, crée `.env` et démarre la base Docker.
Pour repartir de zéro : `./start_mock_exam.sh --force`.

## 2. Passer l'épreuve

Ouvre **uniquement** :

```text
exam/sujet/11_RNCP_38919_BLOC_2_EXAMEN_BLANC_01.md
```

Chrono : **4 h**, sans pause. Règles, planning et Definition of Done détaillés
dans [`PROTOCOLE_4H.md`](PROTOCOLE_4H.md).

## 3. S'auto-corriger

```bash
python grade.py candidate_workspace --with-db
```

Barème du document 12 (section 45), total /100 :

| Bloc | Points |
|---|---:|
| Exploration / notebook | 10 |
| ETL / qualité Python | 15 |
| Modèle relationnel | 10 |
| Docker / variables / persistance | 10 |
| SQLAlchemy / ORM | 15 |
| Ingestion | 10 |
| Machine Learning | 15 |
| Tests | 10 |
| Documentation / impact | 5 |

Le script mélange vérifications **statiques** (fichiers, contenu) et
**dynamiques** (exécute `extract` / `transform` / `validate_schema`, charge
`model.joblib`, lance `pytest`, et — avec `--with-db` — rejoue l'ingestion
deux fois pour vérifier l'idempotence).

Sur macOS, utiliser un Python avec les dépendances du projet (le venv du
workspace) :

```bash
candidate_workspace/.venv/bin/python grade.py candidate_workspace --with-db
```

## 4. Fichiers

```text
simulation/
├── PROTOCOLE_4H.md      # règles, timeline, DoD, questions orales, post-mortem
├── start_mock_exam.sh   # prépare le workspace candidat
├── grade.py             # auto-correction /100
├── README.md
├── candidate_workspace/ # créé par start_mock_exam.sh (ignoré par git)
└── .gitignore
```

## 5. Après

1. Remplir le post-mortem.
2. Comparer avec `exam/correction/green_delivery/`.
3. Rejouer le lab correspondant au bloc le plus faible.
