# LAB 01 — Guide débutant (de zéro à la solution)

> **Public** : tu n'as jamais utilisé pandas (ou tu l'as oublié). Aucun prérequis.
> On explique **chaque** concept au moment où il apparaît. À la fin, tu auras
> exécuté et compris la solution complète.

Ce lab fait une seule chose : **ouvrir un fichier de données et le regarder**.
C'est toujours la première étape d'un projet data. On appelle ça l'**exploration**.

---

## Étape 0 — Comprendre les mots du sujet

| Mot | Ce que c'est, en clair |
|---|---|
| **JSON** | Un format de fichier texte pour stocker des données. Ici `deliveries.json` contient une liste de livraisons. |
| **pandas** | Une bibliothèque Python qui transforme ces données en **tableau** que l'on peut interroger (comme Excel, mais en code). |
| **DataFrame** | Le nom du tableau pandas. Lignes = livraisons, colonnes = champs. |
| **Notebook / Jupyter** | Un document où l'on écrit du code et où l'on voit le résultat juste en dessous. |
| **venv** | Un « dossier Python isolé » pour ce projet, pour ne pas mélanger les bibliothèques. |
| **NaN / null** | Une case vide (valeur manquante). |

Le fichier utilisé : `../data/deliveries_lab.json` — **13 livraisons**, 9 colonnes.

---

## Étape 1 — Créer son environnement (une seule fois)

Un **environnement virtuel** évite de casser ton Python global.

```bash
cd LAB_01_JSON_JUPYTER_PANDAS
python3 -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r ../requirements.txt
```

- `python3 -m venv .venv` → crée un dossier `.venv/` contenant un Python isolé.
- `source .venv/bin/activate` → active cet environnement (tu vois `(.venv)` dans le prompt).
- `pip install` → installe pandas + matplotlib dans le `.venv`.

Vérifie :

```bash
python -c "import pandas; print(pandas.__version__)"
```

> Si tu vois `Can not perform a '--user' install`, retire la ligne `user = true`
> de `~/.config/pip/pip.conf` (un venv refuse les installations `--user`).

---

## Étape 2 — Charger le fichier JSON

Crée/complète le fichier `solution/01_exploration_solution.py` (ou fais-le dans un notebook).
Premier bloc :

```python
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "deliveries_lab.json"

df = pd.read_json(DATA_PATH)
print(df.head())
```

Décryptage ligne par ligne :

- `from pathlib import Path` → outil moderne pour manipuler les **chemins de fichiers**.
- `import pandas as pd` → on importe pandas et on l'appellera `pd` (convention).
- `Path(__file__)` → le chemin de **ce fichier**. `.parent.parent` remonte de `solution/` à `LAB_01.../`. On construit donc le chemin du JSON **relativement au script**, ce qui marche depuis n'importe où. **Ne jamais écrire un chemin absolu en dur** comme `/Users/ton_nom/...` : ça casse chez les autres.
- `pd.read_json(DATA_PATH)` → lit le fichier et renvoie un **DataFrame** (`df`).
- `df.head()` → affiche les 5 premières lignes (pour « voir » les données).

Exécute :

```bash
python 01_exploration_solution.py
```

Tu dois voir un petit tableau avec `delivery_id`, `customer_city`, etc.

---

## Étape 3 — Regarder la forme du tableau

```python
print(df.shape)
print(df.columns.tolist())
df.info()
```

- `df.shape` → **`(13, 9)`** : 13 lignes (livraisons) et 9 colonnes (champs).
- `df.columns.tolist()` → la liste des noms de colonnes.
- `df.info()` → le **type** de chaque colonne (`int64` = entier, `float64` = décimal, `str` = texte) et le nombre de valeurs non vides.

**Pourquoi c'est important ?** Si `distance_km` est de type `str` (texte) au lieu de `float64` (nombre), on ne pourra pas calculer de moyenne. Cette étape détecte ce genre de piège.

---

## Étape 4 — Trouver les cases vides et les doublons

```python
print(df.isna().sum())
print("Doublons:", df.duplicated().sum())
```

- `df.isna()` → un tableau de `True`/`False` (« est-ce vide ? »). `.sum()` compte les `True` par colonne.
  Résultat attendu : `distance_km` = 1 et `traffic_level` = 1 (deux cases vides).
- `df.duplicated()` → repère les lignes **entièrement identiques**. `.sum()` les compte. Ici : **1**.

Ces deux informations dictent le nettoyage du **LAB 02** (remplir les vides, supprimer le doublon).

---

## Étape 5 — Nettoyer une colonne texte (les villes)

Les villes sont écrites de plusieurs façons : `Paris`, `PARIS`, ` Paris ` (avec espaces).

```python
df["customer_city"] = (
    df["customer_city"].astype("string").str.strip().str.lower()
)
print(df["customer_city"].value_counts(dropna=False))
```

- `df["customer_city"]` → on sélectionne la colonne.
- `.astype("string")` → on force le type « texte spécial pandas » qui gère correctement les vides.
- `.str.strip()` → **enlève les espaces** au début et à la fin (`" Paris "` → `"Paris"`).
- `.str.lower()` → met en **minuscules** (`"Paris"` → `"paris"`).
- `df["customer_city"] = ...` → on remplace l'ancienne colonne par la nouvelle.

`value_counts()` compte combien de fois chaque ville apparaît. Normalement, après nettoyage :
`paris`, `poissy`, `versailles`, `nanterre`, `boulogne-billancourt` — plus de doublons de casse.

> `dropna=False` demande d'afficher aussi les valeurs vides (utile pour ne rien cacher).

---

## Étape 6 — Dessiner deux graphiques

matplotlib sert à **voir** les données.

### Graphique 1 — la cible `late_delivery`

```python
df["late_delivery"].value_counts().sort_index().plot(kind="bar")
plt.title("Distribution de late_delivery")
plt.show()
```

- `value_counts()` → compte combien de `0` (pas en retard) et de `1` (en retard).
- `.sort_index()` → range les 0 et 1 dans l'ordre.
- `.plot(kind="bar")` → dessine un **diagramme en barres**.
- `plt.title(...)` → ajoute un titre ; `plt.show()` → affiche la figure.

### Graphique 2 — la distance

```python
df["distance_km"].hist()
plt.title("Distribution de distance_km")
plt.show()
```

- `.hist()` → un **histogramme** : il regroupe les distances par tranches pour montrer leur répartition.

---

## Étape 7 — Lancer et vérifier

```bash
python 01_exploration_solution.py
```

Attendu :

```text
shape: (13, 9)
distance_km         1
traffic_level       1
Doublons: 1
paris ... poissy ... versailles ... nanterre ... boulogne-billancourt
```

Et deux fenêtres de graphiques (ou deux images dans un notebook).

**Version notebook** : ouvre `01_exploration_solution.ipynb` (même code, découpé
en cellules). Le chemin du JSON y est résolu automatiquement.

---

## Récapitulatif des questions du lab

1. Combien de lignes ? → **13**
2. Combien de doublons ? → **1**
3. Colonnes avec des vides ? → **`distance_km`, `traffic_level`**
4. Villes à normaliser ? → **`PARIS`, `Paris`, ` Paris ` (casse/espaces)**
5. Distribution de `late_delivery` ? → un bar chart 0/1

---

## Erreurs fréquentes

| Message | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: pandas` | venv non activé | `source .venv/bin/activate` puis `pip install -r ../requirements.txt` |
| `FileNotFoundError: ...json` | mauvais dossier | utilise le chemin `Path(__file__)` du guide, ou lance depuis `solution/` |
| `Can not perform a '--user' install` | `user = true` dans pip.conf | retirer cette ligne (voir Étape 1) |
| Les graphiques ne s'affichent pas | backend non interactif | en script : `python ...` ; en notebook : exécute la cellule |

---

## Mini-glossaire final

```text
DataFrame   → le tableau de données
shape       → (nombre de lignes, nombre de colonnes)
dtype       → le type d'une colonne (int, float, texte)
NaN / null  → case vide
isna()      → "est vide ?"
duplicated()-> "est un doublon ?"
value_counts() → comptage des valeurs
strip()/lower() → nettoyage de texte
```
