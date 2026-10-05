# LAB 01 — JSON, Jupyter et pandas

**Temps cible : 30 min** · Difficulté : ⭐ · Prérequis : Python

## Objectifs

- charger un JSON avec pandas ;
- inspecter `shape` / colonnes / types ;
- détecter les valeurs nulles et les doublons ;
- normaliser une colonne catégorielle ;
- produire 2 visualisations matplotlib.

## Contenu

```text
LAB_01_JSON_JUPYTER_PANDAS/
├── data/
│   └── deliveries_lab.json          # 13 lignes, 9 colonnes
├── starter/
│   ├── 01_exploration_starter.ipynb # à compléter (TODO 1→6)
│   └── 01_exploration_starter.py    # même énoncé en script
├── solution/
│   ├── 01_exploration_solution.ipynb
│   └── 01_exploration_solution.py
├── EXO.md
└── README.md
```

## Lancement

### Option A — script Python

```bash
cd LAB_01_JSON_JUPYTER_PANDAS/solution
python 01_exploration_solution.py
```

Le chemin du JSON est résolu relativement au fichier : lançable depuis n'importe où.

### Option B — notebook

```bash
cd LAB_01_JSON_JUPYTER_PANDAS
jupyter lab          # puis ouvrir solution/01_exploration_solution.ipynb
```

Le notebook solution résout lui-même le chemin du JSON (`../data/...`, `data/...`
ou le chemin depuis `labs/`) : il fonctionne quel que soit le dossier de lancement.

## Mission

Travaillez sur `data/deliveries_lab.json`. À la fin, vous devez pouvoir répondre :

1. combien de lignes ? → **13**
2. combien de doublons ? → **1**
3. quelles colonnes ont des nulls ? → **`distance_km` (1) et `traffic_level` (1)**
4. quelles valeurs de ville doivent être normalisées ? → **`PARIS`, espaces, casse**
5. quelle est la distribution de `late_delivery` ? → **bar chart 0/1**

## Critères de réussite

- [ ] `df.shape` affiche `(13, 9)` ;
- [ ] `df.isna().sum()` montre exactement 2 colonnes à 1 null ;
- [ ] `df.duplicated().sum()` vaut `1` ;
- [ ] `customer_city` ne contient plus que `paris`, `poissy`, `versailles`, `nanterre`, `boulogne-billancourt` ;
- [ ] les deux graphiques s'affichent.

## Dépannage

| Symptôme | Cause | Correctif |
|---|---|---|
| `Can not perform a '--user' install` | `user = true` dans `~/.config/pip/pip.conf` | retirer cette ligne (un venv ne voit pas les `--user` sitepackages), ou ponctuellement `PIP_USER=0 pip install pandas` |
| `python3.13` lance conda | conda base active | `conda deactivate`, ou `conda config --set auto_activate_base false` |
| `FileNotFoundError: ...json` | lancé depuis un autre dossier avec l'ancien chemin relatif | utiliser `Path(__file__)` (déjà fait dans la solution) ou `cd` dans le dossier |
| `ModuleNotFoundError: matplotlib` | dépendance manquante | `pip install -r ../requirements.txt` |

## Pour aller plus loin

- Transformer ce fichier en DataFrame « propre » : c'est l'objet du **LAB 02**.
- Regarder `df.dtypes` avant/après `astype("string")` pour comprendre le type `str`
  (nouveau dtype pandas) vs `object`.
