# LAB 02 — ETL Python

**Temps cible : 35 min** · Difficulté : ⭐⭐ · Prérequis : LAB 01

## Objectifs

Écrire un ETL en 4 fonctions pures, testables, sans dépendre du dossier courant :

```python
extract(path)          -> pd.DataFrame
validate_schema(df)    -> None        # lève ValueError si une colonne manque
transform(df)          -> pd.DataFrame
save_processed(df, path) -> None
```

## Contenu

```text
LAB_02_ETL_PYTHON/
├── starter/etl.py       # signatures + NotImplementedError
├── solution/etl.py      # implémentation + main()
├── EXO.md
└── README.md
```

Le jeu de données est celui du **LAB 01** :
`LAB_01_JSON_JUPYTER_PANDAS/data/deliveries_lab.json`.

## Lancement

```bash
cd LAB_02_ETL_PYTHON
python solution/etl.py                          # source et cible par défaut
python solution/etl.py chemin/source.json out.csv   # explicite
```

Sortie attendue :

```text
source      : .../LAB_01_JSON_JUPYTER_PANDAS/data/deliveries_lab.json
lignes brutes : 13
lignes clean  : 12
nulls restants: 0
écrit         : .../LAB_02_ETL_PYTHON/solution/deliveries_clean.csv
```

## Contraintes à respecter

| Contrainte | Erreur attendue |
|---|---|
| fichier absent | `FileNotFoundError` |
| colonne requise absente | `ValueError` |
| dédupliquer sur `delivery_id` | `keep="first"` |
| normaliser `customer_city` | `strip()` + `lower()` |
| `distance_km` manquant | imputation par la **médiane** |
| `traffic_level` / `weather` manquants | imputation par `"unknown"` |

## Critères de réussite

- [ ] `extract` lève `FileNotFoundError` sur un fichier inexistant ;
- [ ] `validate_schema` lève `ValueError` si une colonne manque ;
- [ ] 13 lignes brutes → **12 lignes** après dédoublonnage ;
- [ ] `distance_km` et `traffic_level` n'ont plus de null (0 null au total) ;
- [ ] un CSV `deliveries_clean.csv` est écrit.

## Dépannage

| Symptôme | Cause | Correctif |
|---|---|---|
| `FileNotFoundError: data/...` | lancé avec un chemin relatif | utiliser `main()` de la solution (chemins basés sur `Path(__file__)`) ou passer le chemin en argument |
| `KeyError: 'delivery_id'` | JSON différent de celui du LAB 01 | vérifier la source passée en argument |
| `TypeError: 'ellipsis' object` | `df = ...` non remplacé (starter) | implémenter `extract` |
| `ValueError: Missing columns` | vous testez `transform` sur un DataFrame incomplet | normal, c'est le comportement voulu |

## Pour aller plus loin

- Ajouter une fonction `report(df)` qui retourne un dict de statistiques.
- Rendre `transform` idempotent : `transform(transform(df)) == transform(df)`.
- C'est le cœur du **LAB 05** (validations + tests) et du **LAB 07**.
