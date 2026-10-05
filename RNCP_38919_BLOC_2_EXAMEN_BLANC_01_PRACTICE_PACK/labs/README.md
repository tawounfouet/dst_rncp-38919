# Practice Labs — Bloc 2 (ETL, ORM, ML)

Parcours de mise en pratique, du chargement d'un JSON jusqu'à un pipeline ML
complet, pour préparer l'examen blanc du Bloc 2.

Chaque lab existe en deux versions :

- `starter/` — à compléter (les `TODO`) ;
- `solution/` — la référence, à ne consulter qu'après avoir essayé.

> Chaque dossier de lab contient aussi :
> - `README.md` — guide de prise en main détaillé (prérequis, lancement, critères de réussite, dépannage) ;
> - `EXO.md` — version « mode examen » avec checklist chronométrée et solutions repliées.

---

## 1. Prérequis

| Outil | Version | Pour les labs |
|---|---|---|
| Python | 3.11+ (testé 3.13) | 01, 02, 04, 05, 06 |
| pip | récent | tous |
| Docker + Docker Compose | Docker Desktop récent | 03, 04 |
| Jupyter (optionnel) | — | 01 |

Vérification rapide :

```bash
python3 --version        # >= 3.11
docker --version         # Docker version ...
docker compose version   # Docker Compose version v2...
```

---

## 2. Installation (une seule fois)

Depuis le dossier `labs/` :

```bash
cd labs
python3 -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Test d'installation :

```bash
python -c "import pandas, sqlalchemy, sklearn, pytest, matplotlib; print('deps OK')"
```

> Si `pip` échoue avec `Can not perform a '--user' install`, voir le dépannage
> du [`README` du LAB 01](LAB_01_JSON_JUPYTER_PANDAS/README.md#dépannage).

---

## 3. Roadmap

| Lab | Sujet | Temps | Prérequis | README | EXO | Guide zéro |
|---|---|---:|---|---|---|---|
| 01 | JSON / Jupyter / pandas | 30 min | Python | [lien](LAB_01_JSON_JUPYTER_PANDAS/README.md) | [lien](LAB_01_JSON_JUPYTER_PANDAS/EXO.md) | [lien](LAB_01_JSON_JUPYTER_PANDAS/solution/GUIDE_DEBUTANT.md) |
| 02 | ETL Python | 35 min | 01 | [lien](LAB_02_ETL_PYTHON/README.md) | [lien](LAB_02_ETL_PYTHON/EXO.md) | [lien](LAB_02_ETL_PYTHON/solution/GUIDE_DEBUTANT.md) |
| 03 | Docker Compose / MariaDB | 30 min | Docker | [lien](LAB_03_DOCKER_COMPOSE_DB/README.md) | [lien](LAB_03_DOCKER_COMPOSE_DB/EXO.md) | [lien](LAB_03_DOCKER_COMPOSE_DB/solution/GUIDE_DEBUTANT.md) |
| 04 | SQLAlchemy ORM | 35 min | 03 | [lien](LAB_04_SQLALCHEMY_ORM/README.md) | [lien](LAB_04_SQLALCHEMY_ORM/EXO.md) | [lien](LAB_04_SQLALCHEMY_ORM/solution/GUIDE_DEBUTANT.md) |
| 05 | Ingestion + pytest | 35 min | 02 | [lien](LAB_05_INGESTION_AND_TESTS/README.md) | [lien](LAB_05_INGESTION_AND_TESTS/EXO.md) | [lien](LAB_05_INGESTION_AND_TESTS/solution/GUIDE_DEBUTANT.md) |
| 06 | scikit-learn + joblib | 40 min | 01 | [lien](LAB_06_MACHINE_LEARNING_JOBLIB/README.md) | [lien](LAB_06_MACHINE_LEARNING_JOBLIB/EXO.md) | [lien](LAB_06_MACHINE_LEARNING_JOBLIB/solution/GUIDE_DEBUTANT.md) |
| 07 | End-to-End Challenge | 60 min | 01→06 | [lien](LAB_07_END_TO_END_CHALLENGE/README.md) | [lien](LAB_07_END_TO_END_CHALLENGE/EXO.md) | [lien](LAB_07_END_TO_END_CHALLENGE/GUIDE_DEBUTANT.md) |

> **Guide zéro** = explication pas-à-pas pour quelqu'un qui part de zéro :
> chaque concept (DataFrame, ORM, pipeline ML…) est défini au moment où il apparaît.

Temps cumulé conseillé :

```text
≈ 4 h 25 de practice ciblée  +  4 h d'examen blanc
```

---

## 4. Ordre recommandé

```text
01  Explorer les données (pandas)
 └─ 02  Transformer (ETL)
     ├─ 03  Stocker (Docker + MariaDB)
     │   └─ 04  Modéliser (SQLAlchemy ORM)
     └─ 05  Fiabiliser (validation + tests)
06  Prédire (ML + joblib)
07  Tout assembler en 60 min, sans regarder les solutions
```

Les labs 03 et 04 vont ensemble : **lancez la base du LAB 03 avant le LAB 04.**
Le LAB 06 réutilise le dataset du LAB 01.

---

## 5. Données

| Fichier | Utilisé par |
|---|---|
| `LAB_01_JSON_JUPYTER_PANDAS/data/deliveries_lab.json` | LAB 01, LAB 02 |
| `LAB_06_MACHINE_LEARNING_JOBLIB/data/deliveries_ml.csv` | LAB 06 |
| `../exam/sujet/data/raw/deliveries.json` | LAB 07 |

Aucun de ces fichiers n'a besoin d'être téléchargé : tout est fourni.

---

## 6. Diagnostic général

| Symptôme | Cause probable | Correctif |
|---|---|---|
| `ModuleNotFoundError` | venv non activé | `source .venv/bin/activate` puis `pip install -r requirements.txt` |
| `Can not perform a '--user' install` | `user = true` dans `~/.config/pip/pip.conf` | `pip install --user` interdit en venv → retirer la ligne, ou `PIP_USER=0 pip install ...` |
| `python3` pointe sur conda | conda base en tête de `PATH` | utiliser `python3.13` ou désactiver `conda config --set auto_activate_base false` |
| `address already in use` (port) | un service occupe déjà le port | changer le port dans `.env` (`DB_PORT`, `PMA_PORT`) |
| `Access denied for user` | credentials/port différents de LAB 03 | aligner `.env` du LAB 04 sur celui du LAB 03 |
| `FileNotFoundError: data/...` | script lancé depuis le mauvais dossier | les solutions embarquent des chemins robustes ; sinon `cd` dans le dossier du lab |
| `docker compose` « no configuration file » | lancé hors du dossier | `cd LAB_03_DOCKER_COMPOSE_DB/solution` d'abord |

---

## 7. Critères de réussite globaux

À la fin du parcours, vous devez être capable de :

- [ ] charger et inspecter un JSON avec pandas ;
- [ ] écrire un ETL `extract / validate / transform / save` testable ;
- [ ] monter une MariaDB + phpMyAdmin avec Docker Compose et un `.env` ;
- [ ] modéliser une relation 1‑N avec SQLAlchemy et persister via une session ;
- [ ] valider des données et écrire des tests pytest (dont les cas d'erreur) ;
- [ ] entraîner et sérialiser une pipeline scikit-learn avec `joblib` ;
- [ ] enchaîner tout cela sous contrainte de temps (LAB 07).
