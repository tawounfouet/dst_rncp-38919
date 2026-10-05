# LAB 06 — scikit-learn + joblib

**Temps cible : 40 min** · Difficulté : ⭐⭐⭐ · Prérequis : LAB 01

## Objectifs

- définir `X` / `y` (cible `late_delivery`) ;
- gérer colonnes numériques **et** catégorielles dans une pipeline ;
- faire un `train_test_split` stratifié ;
- entraîner une classification ;
- afficher accuracy / precision / recall / F1 ;
- sérialiser la **pipeline complète** avec `joblib`.

## Contenu

```text
LAB_06_MACHINE_LEARNING_JOBLIB/
├── data/deliveries_ml.csv
├── starter/train_model.py   # plan en commentaires
├── solution/train_model.py  # pipeline complète
├── EXO.md
└── README.md
```

## Lancement

```bash
cd LAB_06_MACHINE_LEARNING_JOBLIB
python solution/train_model.py
```

Les chemins (`data/`, `models/`) sont résolus relativement au fichier :
le script est lançable **depuis n'importe quel dossier**.

Sortie attendue (dataset fourni, `random_state=42`) :

```text
accuracy : 0.7142857142857143
precision: 1.0
recall   : 0.3333333333333333
f1       : 0.5
modèle   : .../models/model.joblib
```

## Critères de réussite

- [ ] le script produit les 4 métriques sans erreur ;
- [ ] `models/model.joblib` est créé ;
- [ ] le preprocessing est **dans** la pipeline (pas de fuite train/test) ;
- [ ] `OneHotEncoder(handle_unknown="ignore")` protège l'inférence future ;
- [ ] le script fonctionne lancé depuis `/tmp` (chemins robustes).

## Recharger le modèle

```python
import joblib
pipeline = joblib.load("models/model.joblib")
pipeline.predict([[4.2, "paris", "bike", "high", "rain"]])
```

## Point de réflexion (important)

`delivery_minutes` doit-il être une feature si la prédiction a lieu **avant**
la fin de la livraison ? Non : c'est une **fuite de données** (le temps réel
n'est connu qu'après). Il est donc **volontairement exclu** de `X`.
C'est le type de question posée à l'oral du Bloc 2.

## Dépannage

| Symptôme | Cause | Correctif |
|---|---|---|
| `FileNotFoundError: data/deliveries_ml.csv` | ancien chemin relatif, lancé ailleurs | la solution utilise `Path(__file__)` ; sinon `cd` dans le dossier du lab |
| `could not convert string to float` | catégories non encodées | garder `ColumnTransformer` + `OneHotEncoder` |
| `ValueError: ... unknown categories` | encodeur sans `handle_unknown` | `OneHotEncoder(handle_unknown="ignore")` |
| `stratify=y` échoue | classe trop peu peuplée | réduire la taille de test ou retirer `stratify` |
| métriques instables | pas de `random_state` | fixer `random_state=42` |

## Pour aller plus loin

- Comparer `LogisticRegression` et `RandomForestClassifier` (`classification_report`).
- Ajouter une validation croisée `cross_val_score`.
- Sauvegarder aussi les métriques dans un `metrics.json` à côté du modèle.
