# 06 — RNCP 38919 — Bloc 2
# Guide Machine Learning — scikit-learn, évaluation et joblib

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`

> **Règle de lecture**
>
> - **Attendu source** : élément explicitement annoncé dans le support DataScientest.
> - **Guide pratique** : patterns, exemples et exercices proposés pour préparer l’épreuve.
>
> Le support fourni annonce :
>
> ```text
> - l’entraînement d’un modèle de machine learning avec scikit-learn ;
> - l’évaluation d’un modèle ;
> - la sauvegarde du modèle avec joblib.
> ```
>
> La page source disponible **ne fixe pas** :
>
> ```text
> un algorithme précis
> une métrique précise
> une target précise
> un type de problème précis
> ```
>
> Il faut donc savoir adapter la démarche au dataset et au sujet réel.

---

# 1. Position de la partie ML dans le Bloc 2

## Attendu source

Le Machine Learning intervient après plusieurs étapes de préparation des données.

Chaîne logique :

```text
JSON
  ↓
Jupyter
  ↓
pandas
  ↓
Nettoyage
  ↓
Base / ingestion
  ↓
Machine Learning
  ↓
Évaluation
  ↓
joblib
```

Le ML n’est donc pas isolé du pipeline Data Engineering.

---

# 2. Objectif de préparation

## Guide pratique

À la fin de cette partie, il faut être capable de produire rapidement :

```text
dataset propre
    ↓
features X
target y
    ↓
train_test_split
    ↓
model.fit()
    ↓
model.predict()
    ↓
metric
    ↓
joblib.dump()
```

---

# 3. Première question : quel est le problème ML ?

## Guide pratique

Avant d’écrire du code :

```text
Que cherche-t-on à prédire ?
```

Puis :

```text
La target est-elle :
- numérique ?
- catégorielle ?
```

Modèle mental :

```text
target numérique
→ régression

target catégorielle
→ classification
```

> Cette distinction relève des connaissances générales nécessaires pour utiliser scikit-learn ; la page source fournie ne précise pas quel type de problème sera utilisé le jour de l’épreuve.

---

# 4. Identifier X et y

## Guide pratique

Supposons :

```text
target = "label"
```

Alors :

```python
X = df.drop(columns=["label"])
y = df["label"]
```

À retenir :

```text
X
=
features

y
=
target
```

---

# 5. Vérifier les features avant entraînement

## Guide pratique

Avant le split :

```python
X.info()
```

Puis vérifier :

```text
[ ] nulls
[ ] catégories
[ ] types
[ ] colonnes inutiles
[ ] identifiants techniques
[ ] fuite de target
```

---

# 6. Éviter la fuite de données

## Guide pratique

Erreur classique :

```text
une colonne contient directement
ou indirectement la réponse à prédire
```

Exemple conceptuel :

```text
target = churn
feature = churn_status_final
```

Ce type de colonne ne doit pas rester dans `X`.

---

# 7. Colonnes catégorielles

## Attendu source

Le support annonce explicitement la gestion des colonnes catégorielles dans la partie préparation des données.

## Guide pratique

Approche simple de préparation :

```python
X = pd.get_dummies(
    X,
    drop_first=True,
)
```

Ou, si besoin ciblé :

```python
X = pd.get_dummies(
    X,
    columns=["category"],
    drop_first=True,
)
```

> Le support ne prescrit pas `get_dummies()` ; c’est un pattern de révision simple.

---

# 8. Valeurs manquantes

## Attendu source

Le support annonce explicitement la gestion des valeurs manquantes.

## Guide pratique

Avant l’entraînement :

```python
X.isna().sum()
```

Il faut éviter d’arriver à :

```python
model.fit(...)
```

avec des données incompatibles avec le modèle choisi.

---

# 9. Séparer train et test

## Guide pratique

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)
```

Modèle mental :

```text
DATA
 ├── TRAIN
 │    ↓
 │   fit
 │
 └── TEST
      ↓
     evaluate
```

---

# 10. Pourquoi séparer train et test ?

## Guide pratique

```text
TRAIN
=
apprentissage

TEST
=
évaluation sur des données
non utilisées pour entraîner
```

Objectif :

```text
éviter d’évaluer
sur les mêmes données
que celles utilisées pour apprendre
```

---

# 11. `random_state`

## Guide pratique

```python
random_state=42
```

permet de rendre le split reproductible.

Ce n’est pas une exigence explicitement citée dans le support, mais c’est un bon réflexe d’entraînement.

---

# 12. Entraîner un modèle

## Attendu source

Le support demande :

```text
entraînement d’un modèle de machine learning
avec scikit-learn
```

## Guide pratique

Pattern universel :

```python
model.fit(
    X_train,
    y_train,
)
```

À retenir :

```text
fit
=
apprendre
```

---

# 13. Faire des prédictions

## Guide pratique

```python
predictions = model.predict(
    X_test
)
```

À retenir :

```text
predict
=
produire une sortie
à partir des features
```

---

# 14. Évaluer le modèle

## Attendu source

Le support annonce :

```text
évaluation d’un modèle
```

Mais ne fixe pas la métrique dans la page fournie.

Donc :

```text
classification
→ métrique adaptée

régression
→ métrique adaptée
```

---

# 15. Classification — exemple de métrique

## Guide pratique

Exemple simple :

```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(
    y_test,
    predictions,
)

print(accuracy)
```

> `accuracy_score` est un exemple de préparation, pas une métrique imposée par le support.

---

# 16. Classification — autres métriques utiles à connaître

## Guide pratique

```python
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)
```

Conceptuellement :

```text
precision
→ qualité des positifs prédits

recall
→ capacité à retrouver les positifs

f1
→ compromis precision / recall
```

Ces métriques relèvent de la culture ML générale ; elles ne sont pas détaillées dans la page source.

---

# 17. Régression — exemple de métrique

## Guide pratique

```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(
    y_test,
    predictions,
)

print(mse)
```

Autre possibilité :

```python
from sklearn.metrics import mean_absolute_error
```

Là encore, la métrique exacte dépend du sujet réel.

---

# 18. Modèle simple pour classification

## Guide pratique

Exemple possible :

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    max_iter=1000
)
```

Puis :

```python
model.fit(
    X_train,
    y_train,
)
```

> Le support ne demande pas spécifiquement `LogisticRegression`.
> L’objectif est d’avoir un modèle simple, rapide et fonctionnel pour s’entraîner.

---

# 19. Modèle simple pour régression

## Guide pratique

Exemple possible :

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
```

Puis :

```python
model.fit(
    X_train,
    y_train,
)
```

---

# 20. Modèle arbre — exemple alternatif

## Guide pratique

Classification :

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    random_state=42
)
```

Régression :

```python
from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(
    random_state=42
)
```

> À connaître comme option d’entraînement, pas comme exigence source.

---

# 21. Choix du modèle pendant l’épreuve

## Guide pratique

Priorité :

```text
fonctionnel
>
sophistiqué
```

Réflexe :

```text
1. choisir un modèle simple
2. obtenir un fit
3. obtenir une prédiction
4. obtenir une métrique
5. sauvegarder
```

Ne pas commencer par :

```text
hyperparameter tuning
cross-validation complexe
ensemble sophistiqué
```

si cela compromet le rendu complet.

---

# 22. Pipeline minimal de classification

## Guide pratique

```python
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


X = df.drop(
    columns=["target"]
)

y = df["target"]


X = pd.get_dummies(
    X,
    drop_first=True,
)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)


model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train,
    y_train,
)


predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions,
)

print(
    f"Accuracy: {accuracy:.4f}"
)
```

---

# 23. Pipeline minimal de régression

## Guide pratique

```python
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


X = df.drop(
    columns=["target"]
)

y = df["target"]


X = pd.get_dummies(
    X,
    drop_first=True,
)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)


model = LinearRegression()

model.fit(
    X_train,
    y_train,
)


predictions = model.predict(
    X_test
)


mae = mean_absolute_error(
    y_test,
    predictions,
)

print(
    f"MAE: {mae:.4f}"
)
```

---

# 24. Sauvegarde avec `joblib`

## Attendu source

Le support annonce explicitement :

```text
sauvegarde d’un modèle ML avec joblib
```

## Guide pratique

```python
import joblib

joblib.dump(
    model,
    "model.joblib",
)
```

---

# 25. Recharger le modèle

## Guide pratique

```python
model = joblib.load(
    "model.joblib"
)
```

Puis :

```python
predictions = model.predict(
    X_new
)
```

---

# 26. Réflexe important : sauvegarder les transformations utiles

## Guide pratique

Si la préparation des features dépend de transformations spécifiques, il faut garder la cohérence entre :

```text
train
et
future inference
```

Exemple conceptuel :

```text
encodage train
=
encodage futur
```

La page source n’exige pas un pipeline scikit-learn complet, mais il faut éviter d’enregistrer un modèle impossible à réutiliser correctement.

---

# 27. `Pipeline` scikit-learn — option de préparation

## Guide pratique

Exemple conceptuel :

```python
from sklearn.pipeline import Pipeline
```

Un pipeline peut chaîner :

```text
préparation
→ modèle
```

Mais :

```text
ce n'est pas exigé
dans la page source fournie
```

Pendant l’épreuve, utiliser uniquement ce que l’on maîtrise réellement.

---

# 28. Script `train_model.py` — structure minimale

## Guide pratique

```python
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def load_data(path):
    return pd.read_csv(path)


def prepare_features(df):
    X = df.drop(
        columns=["target"]
    )
    y = df["target"]

    X = pd.get_dummies(
        X,
        drop_first=True,
    )

    return X, y


def train_model(
    X_train,
    y_train,
):
    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(
        X_train,
        y_train,
    )

    return model


def evaluate_model(
    model,
    X_test,
    y_test,
):
    predictions = model.predict(
        X_test
    )

    return accuracy_score(
        y_test,
        predictions,
    )


def main():
    df = load_data(
        "data/processed/data.csv"
    )

    X, y = prepare_features(df)

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = train_model(
        X_train,
        y_train,
    )

    score = evaluate_model(
        model,
        X_test,
        y_test,
    )

    print(
        f"Score: {score:.4f}"
    )

    joblib.dump(
        model,
        "models/model.joblib",
    )


if __name__ == "__main__":
    main()
```

---

# 29. Vérifier que le fichier modèle existe

## Guide pratique

```python
from pathlib import Path

model_path = Path(
    "models/model.joblib"
)

print(
    model_path.exists()
)
```

---

# 30. Créer le dossier `models`

## Guide pratique

```python
from pathlib import Path

Path("models").mkdir(
    parents=True,
    exist_ok=True,
)
```

Puis :

```python
joblib.dump(
    model,
    "models/model.joblib",
)
```

---

# 31. Risque : données train/test incohérentes

## Guide pratique

Avec :

```python
pd.get_dummies(...)
```

appliqué séparément à train et test, les colonnes peuvent diverger.

Préférer préparer l’ensemble `X` avant split dans un exercice simple :

```text
X
→ encodage
→ split
```

ou utiliser un pipeline maîtrisé.

---

# 32. Risque : colonne ID comme feature

## Guide pratique

Exemple :

```text
customer_id
```

peut être un identifiant technique sans valeur prédictive réelle.

Réflexe :

```python
X = X.drop(
    columns=["customer_id"]
)
```

si le contexte le justifie.

---

# 33. Risque : target manquante

## Guide pratique

Vérifier :

```python
if "target" not in df.columns:
    raise ValueError(
        "Missing target column"
    )
```

---

# 34. Risque : nulls avant `fit`

## Guide pratique

```python
print(
    X.isna().sum().sum()
)
```

Si non nul :

```text
traiter avant entraînement
```

---

# 35. Risque : mauvaise target

## Guide pratique

Avant de coder :

```python
print(
    y.value_counts(
        dropna=False
    )
)
```

pour classification.

Ou :

```python
print(
    y.describe()
)
```

pour régression.

---

# 36. Déséquilibre de classes

## Guide pratique

Pour classification :

```python
y.value_counts(
    normalize=True
)
```

permet d’identifier un déséquilibre.

La page source ne demande pas explicitement de traiter ce problème, mais il peut aider à interpréter une accuracy trompeuse.

---

# 37. Interprétation minimale d’un score

## Guide pratique

Ne pas écrire uniquement :

```text
Accuracy = 0.82
```

Ajouter une phrase :

```text
Le modèle obtient une accuracy de 0,82
sur le jeu de test.
```

Puis, si pertinent :

```text
Cette métrique doit être interprétée
au regard de la distribution des classes.
```

---

# 38. Documentation du choix du modèle

## Attendu source

Le rendu principal demande un fichier synthétique expliquant les choix techniques.

## Guide pratique

Pour le ML :

```text
Modèle choisi
Pourquoi ce modèle
Variables utilisées
Méthode de split
Métrique
Résultat
Limites
Pistes d’amélioration
```

---

# 39. Exemple de justification courte

## Guide pratique

```text
Un modèle simple a été privilégié afin de disposer
d’une baseline rapide à entraîner et facile à interpréter
dans la contrainte temporelle de l’exercice.
```

Cette formulation est un exemple, pas une consigne officielle.

---

# 40. Limites à pouvoir citer

## Guide pratique

```text
peu de données
classes déséquilibrées
features limitées
pas de tuning
pas de cross-validation
temps d’examen limité
```

Ne citer que les limites réellement applicables à son travail.

---

# 41. Pistes d’amélioration possibles

## Guide pratique

```text
feature engineering
validation croisée
hyperparameter tuning
comparaison de plusieurs modèles
meilleure gestion des catégories
meilleure gestion des nulls
monitoring du modèle
```

---

# 42. Mini-exercice 1 — Classification

Créer un petit dataset :

```text
age
income
city
target
```

Objectif :

```text
1. gérer nulls
2. encoder city
3. split
4. entraîner
5. prédire
6. accuracy
7. joblib.dump
```

---

# 43. Mini-exercice 2 — Régression

Dataset :

```text
surface
rooms
city
price
```

Objectif :

```text
target = price
```

Puis :

```text
split
LinearRegression
predict
MAE
joblib
```

---

# 44. Mini-exercice 3 — Modèle rechargé

Étapes :

```text
1. entraîner
2. joblib.dump
3. supprimer la variable model
4. joblib.load
5. prédire à nouveau
```

Objectif :

```text
vérifier que l’artefact est réellement utilisable
```

---

# 45. Mini-exercice 4 — Dataset imparfait

Ajouter :

```text
nulls
catégorie inconnue
ID technique
doublons
```

Objectif :

```text
préparer correctement le dataset
avant fit
```

---

# 46. Mini-exercice 5 — Mauvaise métrique

Pour une classification très déséquilibrée :

```text
95 % classe 0
5 % classe 1
```

Comparer :

```text
accuracy
et
recall / f1
```

Objectif :

```text
comprendre que la métrique
doit être adaptée au problème
```

---

# 47. Mini-exercice 6 — Script autonome

Créer :

```text
src/train_model.py
```

qui doit fonctionner avec :

```bash
python src/train_model.py
```

et produire :

```text
models/model.joblib
```

---

# 48. Anti-patterns

## 1. Entraîner avant de nettoyer

```text
raw dataset
→ fit
```

À éviter.

---

## 2. Mettre la target dans X

```python
X = df
```

si `df` contient la target.

---

## 3. Évaluer sur le train

À éviter :

```python
model.predict(
    X_train
)
```

comme seule évaluation.

---

## 4. Utiliser un modèle complexe sans besoin

```text
complexité
≠
qualité
```

---

## 5. Oublier `joblib`

La sauvegarde est explicitement annoncée dans le support.

---

## 6. Ne pas documenter la métrique

Toujours indiquer :

```text
quelle métrique
et
pourquoi elle est utilisée
```

si le sujet le permet.

---

# 49. Checklist ML avant rendu

```text
[ ] target identifiée
[ ] X défini
[ ] nulls gérés
[ ] catégories gérées
[ ] train/test split
[ ] modèle entraîné
[ ] prédictions produites
[ ] métrique calculée
[ ] résultat affiché
[ ] modèle sauvegardé avec joblib
[ ] fichier présent
[ ] choix documenté
```

---

# 50. Debug rapide — `fit` échoue

Checklist :

```text
X contient-il des strings ?
X contient-il des NaN ?
y contient-elle des NaN ?
X et y ont-ils même nombre de lignes ?
target encore dans X ?
modèle adapté au problème ?
```

---

# 51. Debug rapide — `predict` échoue

Checklist :

```text
mêmes colonnes ?
même ordre ?
mêmes transformations ?
mêmes types ?
modèle bien entraîné ?
```

---

# 52. Debug rapide — joblib

Checklist :

```text
dossier models existe ?
chemin correct ?
droits d’écriture ?
objet model existe ?
joblib importé ?
```

---

# 53. Réflexe 30 secondes

```python
X = df.drop(columns=["target"])
y = df["target"]

X = pd.get_dummies(
    X,
    drop_first=True,
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model.fit(
    X_train,
    y_train,
)

pred = model.predict(
    X_test
)

joblib.dump(
    model,
    "models/model.joblib",
)
```

---

# 54. Questions flash

1. Que représentent X et y ?
2. Pourquoi séparer train et test ?
3. À quoi sert `fit()` ?
4. À quoi sert `predict()` ?
5. Pourquoi vérifier les nulls avant `fit()` ?
6. Pourquoi encoder les catégories ?
7. Quelle différence entre classification et régression ?
8. Le support impose-t-il un algorithme précis ?
9. Le support impose-t-il une métrique précise ?
10. Comment sauvegarder un modèle ?
11. Comment recharger un modèle ?
12. Que faut-il documenter dans le fichier synthétique ?

---

# 55. Réponses flash

```text
1. X = features ; y = target.
2. Évaluer sur des données non utilisées pour l’apprentissage.
3. Entraîner le modèle.
4. Produire des prédictions.
5. Certains modèles n’acceptent pas les NaN.
6. Transformer les catégories en représentation exploitable par le modèle choisi.
7. Classification = target catégorielle ; régression = target numérique.
8. Non, pas dans la page source fournie.
9. Non, pas dans la page source fournie.
10. joblib.dump(...).
11. joblib.load(...).
12. architecture, choix techniques, résultat, limites, pistes d’amélioration selon le travail réalisé.
```

---

# 56. Temps cible d’entraînement

## Guide pratique

Pendant une simulation Bloc 2 :

```text
Préparation X/y : 5–10 min
Split : 2 min
Train : 5–10 min
Évaluation : 5 min
joblib : 2 min
Documentation : 5 min
```

Objectif :

```text
≈ 20–30 minutes
```

pour un modèle simple lorsque les données sont déjà prêtes.

> Cette répartition est une stratégie d’entraînement, pas un timing officiel.

---

# 57. Niveau à viser

```text
NIVEAU 1
X / y
split

    ↓

NIVEAU 2
fit
predict
metric

    ↓

NIVEAU 3
categorical handling
null handling

    ↓

NIVEAU 4
joblib
script autonome
documentation
```

---

# 58. Résumé final

Le support du Bloc 2 demande une chaîne simple mais complète :

```text
DATASET PROPRE
      ↓
      X / y
      ↓
train_test_split
      ↓
model.fit
      ↓
model.predict
      ↓
évaluation
      ↓
joblib.dump
```

Le support ne fournit pas dans la page disponible :

```text
un modèle obligatoire
une métrique obligatoire
une stratégie de tuning obligatoire
```

La préparation doit donc viser :

```text
adaptation
+
simplicité
+
exécution rapide
+
résultat documenté
```

---

# 59. Document suivant

```text
07_RNCP_38919_BLOC_2_TESTING_STRATEGY.md
```

Objectif :

> approfondir les contrôles explicitement annoncés dans le support :
> gestion des erreurs, détection des doublons et conformité au schéma,
> puis les transformer en stratégie de tests praticable pendant une épreuve de 4 heures.
