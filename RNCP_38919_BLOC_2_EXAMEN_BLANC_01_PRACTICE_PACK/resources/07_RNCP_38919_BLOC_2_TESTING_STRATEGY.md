# 07 — RNCP 38919 — Bloc 2
# Testing Strategy — Ingestion, erreurs, doublons et conformité au schéma

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 2 — Projet ETL & ML  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 2 - Projet ETL & ML.pdf`

> **Règle de lecture**
>
> - **Attendu source** : ce qui apparaît explicitement dans le support DataScientest.
> - **Guide pratique** : stratégie et exemples proposés pour préparer l’épreuve.
>
> Le support annonce explicitement :
>
> ```text
> l’écriture de tests robustes pour garantir la fiabilité de l’ingestion
> ```
>
> avec trois axes précis :
>
> ```text
> gestion des erreurs
> détection de doublons
> conformité au schéma
> ```
>
> La page source disponible ne fixe pas :
>
> ```text
> un framework de test obligatoire
> une arborescence de tests obligatoire
> un nombre minimal de tests
> une bibliothèque de validation de schéma spécifique
> ```
>
> Les exemples `pytest` ci-dessous constituent donc une stratégie de préparation.

---

# 1. Pourquoi les tests font partie du Bloc 2

## Attendu source

Le support ne s’arrête pas à :

```text
collecter
transformer
ingérer
```

Il demande aussi de vérifier que l’ingestion est fiable.

Le rôle des tests peut être résumé ainsi :

```text
Données entrantes
      ↓
Validation
      ↓
Ingestion
      ↓
Tests
      ↓
Confiance dans le pipeline
```

---

# 2. Les trois axes explicitement annoncés

## Attendu source

```text
1. gestion des erreurs
2. détection de doublons
3. conformité au schéma
```

Toute stratégie de test pour le Bloc 2 doit donc au minimum couvrir ces trois dimensions.

---

# 3. Modèle mental global

## Guide pratique

```text
INPUT
  ↓
VALIDATE
  ↓
TRANSFORM
  ↓
INGEST
  ↓
VERIFY
```

À chaque étape :

```text
happy path
+
failure path
```

---

# 4. Le happy path

## Guide pratique

Un premier test doit vérifier le scénario nominal :

```text
donnée valide
→ transformation valide
→ ingestion réussie
```

Exemple conceptuel :

```python
def test_valid_record_is_ingested():
    ...
```

Objectif :

```text
prouver que le système fonctionne
quand les données sont correctes
```

---

# 5. Gestion des erreurs

## Attendu source

Le support cite explicitement :

```text
gestion des erreurs
```

## Guide pratique

Exemples d’erreurs utiles à simuler :

```text
fichier absent
JSON invalide
colonne absente
type incorrect
connexion DB impossible
clé étrangère invalide
valeur obligatoire manquante
```

---

# 6. Test — fichier absent

## Guide pratique

Si l’extraction vérifie l’existence du fichier :

```python
from pathlib import Path

def extract(path: Path):
    if not path.exists():
        raise FileNotFoundError(path)
```

Test :

```python
import pytest


def test_missing_file_raises():
    with pytest.raises(
        FileNotFoundError
    ):
        extract(
            Path("missing.json")
        )
```

---

# 7. Test — schéma incomplet

## Attendu source

La conformité au schéma est explicitement annoncée.

## Guide pratique

Validation simple :

```python
REQUIRED_COLUMNS = {
    "id",
    "name",
    "category",
}
```

Puis :

```python
def validate_schema(df):
    missing = (
        REQUIRED_COLUMNS
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )
```

Test :

```python
import pandas as pd
import pytest


def test_missing_required_column():
    df = pd.DataFrame(
        {
            "id": [1],
            "name": ["Alice"],
        }
    )

    with pytest.raises(
        ValueError
    ):
        validate_schema(df)
```

---

# 8. Test — clé primaire manquante

## Guide pratique

Validation :

```python
def validate_primary_key(df):
    if df["id"].isna().any():
        raise ValueError(
            "Null primary key"
        )
```

Test :

```python
def test_null_primary_key_is_rejected():
    df = pd.DataFrame(
        {
            "id": [1, None],
            "name": ["Alice", "Bob"],
        }
    )

    with pytest.raises(
        ValueError
    ):
        validate_primary_key(df)
```

---

# 9. Détection de doublons

## Attendu source

Le support cite explicitement :

```text
détection de doublons
```

## Guide pratique

Deux approches possibles :

```text
A. rejeter les doublons
B. les dédupliquer selon une règle explicite
```

Le choix dépend du sujet et du sens métier.

---

# 10. Détecter les doublons

## Guide pratique

```python
duplicates = df[
    df.duplicated(
        subset=["id"],
        keep=False,
    )
]
```

Ou :

```python
has_duplicates = (
    df["id"]
    .duplicated()
    .any()
)
```

---

# 11. Test — doublon détecté

## Guide pratique

```python
def validate_duplicates(df):
    if df["id"].duplicated().any():
        raise ValueError(
            "Duplicate id detected"
        )
```

Test :

```python
def test_duplicate_id_is_rejected():
    df = pd.DataFrame(
        {
            "id": [1, 1],
            "name": ["Alice", "Alice"],
        }
    )

    with pytest.raises(
        ValueError
    ):
        validate_duplicates(df)
```

---

# 12. Test — dataset sans doublon

## Guide pratique

```python
def test_unique_ids_are_valid():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Alice", "Bob"],
        }
    )

    validate_duplicates(df)
```

Le test réussit si aucune exception n’est levée.

---

# 13. Conformité au schéma

## Attendu source

Le support demande explicitement :

```text
conformité au schéma
```

## Guide pratique

Cela peut couvrir :

```text
colonnes attendues
colonnes obligatoires
types
nullabilité
unicité
domaines de valeurs
```

---

# 14. Test — colonnes exactes

## Guide pratique

```python
EXPECTED_COLUMNS = {
    "id",
    "name",
    "category",
}
```

Test :

```python
def test_expected_columns_present():
    df = pd.DataFrame(
        columns=[
            "id",
            "name",
            "category",
        ]
    )

    assert EXPECTED_COLUMNS.issubset(
        set(df.columns)
    )
```

---

# 15. Test — type numérique

## Guide pratique

```python
from pandas.api.types import (
    is_numeric_dtype,
)


def test_amount_is_numeric():
    df = pd.DataFrame(
        {
            "amount": [10.0, 20.0]
        }
    )

    assert is_numeric_dtype(
        df["amount"]
    )
```

---

# 16. Test — catégorie autorisée

## Guide pratique

```python
ALLOWED_STATUS = {
    "active",
    "inactive",
}
```

Test :

```python
def test_status_domain():
    df = pd.DataFrame(
        {
            "status": [
                "active",
                "inactive",
            ]
        }
    )

    assert df["status"].isin(
        ALLOWED_STATUS
    ).all()
```

---

# 17. Test — valeur catégorielle invalide

## Guide pratique

```python
def test_invalid_status_is_rejected():
    df = pd.DataFrame(
        {
            "status": [
                "active",
                "unknown_value",
            ]
        }
    )

    assert not df["status"].isin(
        ALLOWED_STATUS
    ).all()
```

---

# 18. Tests d’ingestion vers la base

## Guide pratique

La source demande des tests garantissant la fiabilité de l’ingestion.

À vérifier après insertion :

```text
nombre de lignes
clé primaire
doublons
relations
valeurs critiques
```

---

# 19. Vérifier le nombre de lignes

## Guide pratique

Après ingestion :

```text
lignes attendues
=
lignes réellement présentes
```

Exemple conceptuel :

```python
def test_row_count_after_ingestion():
    expected = 10

    actual = (
        session
        .query(User)
        .count()
    )

    assert actual == expected
```

---

# 20. Vérifier une ligne insérée

## Guide pratique

```python
def test_user_is_inserted():
    user = (
        session
        .query(User)
        .filter_by(id=1)
        .first()
    )

    assert user is not None
```

---

# 21. Vérifier une relation

## Guide pratique

Pour :

```text
User
1
│
N
Address
```

Test conceptuel :

```python
def test_address_references_user():
    address = (
        session
        .query(Address)
        .first()
    )

    assert address.user_id is not None
```

---

# 22. Tester une ingestion idempotente

## Guide pratique

Le support cite la détection de doublons.

Un bon scénario de révision est :

```text
ingestion 1
→ OK

ingestion 2 du même dataset
→ pas de duplication non contrôlée
```

Ce comportement exact dépend du code choisi.

---

# 23. Exemple d’idempotence stricte

## Guide pratique

Si les doublons doivent être refusés :

```text
premier passage
→ insert

deuxième passage
→ erreur contrôlée
```

Test conceptuel :

```python
def test_second_ingestion_does_not_duplicate():
    ...
```

---

# 24. Tester la transformation

## Guide pratique

Exemple :

```python
def clean_city(value):
    return (
        value
        .strip()
        .lower()
    )
```

Test :

```python
def test_city_is_normalized():
    assert clean_city(
        " Paris "
    ) == "paris"
```

---

# 25. Tester les valeurs manquantes

## Guide pratique

Si la règle métier dit :

```text
amount manquant
→ médiane
```

alors le test doit vérifier cette règle.

Exemple conceptuel :

```python
def test_missing_amount_is_imputed():
    ...
```

---

# 26. Tester les sorties

## Guide pratique

Si le script ETL produit :

```text
data/processed/data.csv
```

le test peut vérifier :

```python
def test_output_file_is_created(
    tmp_path,
):
    ...
```

---

# 27. Pourquoi `tmp_path` est utile

## Guide pratique

Avec pytest :

```python
def test_export(tmp_path):
    output = (
        tmp_path
        / "output.csv"
    )
```

Cela permet de tester les fichiers sans polluer le projet.

> `tmp_path` n’est pas mentionné dans la page source ; il s’agit d’un outil pratique de préparation.

---

# 28. `pytest` — minimum à connaître

## Guide pratique

Installer :

```bash
pip install pytest
```

Lancer :

```bash
pytest
```

Mode verbeux :

```bash
pytest -v
```

Un fichier :

```bash
pytest tests/test_ingestion.py
```

Un test :

```bash
pytest \
  tests/test_ingestion.py::test_duplicate_id_is_rejected
```

---

# 29. Convention de noms

## Guide pratique

Fichiers :

```text
test_*.py
```

Fonctions :

```text
test_*
```

Exemple :

```text
tests/
└── test_ingestion.py
```

---

# 30. Assertions essentielles

## Guide pratique

```python
assert value == expected
```

```python
assert value is not None
```

```python
assert condition
```

Avec erreur attendue :

```python
with pytest.raises(
    ValueError
):
    ...
```

---

# 31. Structure de tests recommandée

## Guide pratique

```text
tests/
│
├── test_extract.py
├── test_transform.py
├── test_schema.py
└── test_ingestion.py
```

Pour une épreuve courte, un seul fichier peut suffire si cela reste lisible.

Le support ne fixe pas cette arborescence.

---

# 32. Test Matrix minimale

## Guide pratique

| Cas | Input | Résultat attendu |
|---|---|---|
| Nominal | dataset valide | ingestion réussie |
| Fichier absent | chemin invalide | erreur contrôlée |
| Colonne absente | schéma incomplet | rejet |
| PK nulle | `id=None` | rejet |
| Doublon | même `id` | détection / rejet |
| Mauvais type | texte dans numérique | erreur ou coercition prévue |
| Valeur invalide | statut hors domaine | rejet |
| Réingestion | même dataset | pas de duplication non contrôlée |

---

# 33. Priorité des tests en contexte 4 h

## Guide pratique

Si le temps est limité :

```text
P0 — indispensable
───────────────
happy path
schéma manquant
doublon
erreur critique

P1 — utile
─────────
type invalide
valeur domaine
relation FK

P2 — amélioration
────────────────
cas limites additionnels
performance
tests très fins
```

> Cette priorisation est une stratégie de préparation, pas une classification officielle DataScientest.

---

# 34. Tests et exceptions

## Guide pratique

Préférer :

```python
raise ValueError(
    "Duplicate id detected"
)
```

à :

```python
print(
    "error"
)
```

si le comportement attendu est réellement un échec.

Pourquoi :

```text
exception
→ testable

simple print
→ beaucoup moins robuste
```

---

# 35. Erreur explicite

## Guide pratique

À éviter :

```python
raise Exception()
```

Préférer :

```python
raise ValueError(
    "Missing required column: id"
)
```

---

# 36. Ne pas masquer les erreurs

## Guide pratique

Anti-pattern :

```python
try:
    ...
except Exception:
    pass
```

Cela peut produire :

```text
pipeline silencieusement incorrect
```

---

# 37. Test de fonction pure

## Guide pratique

Les fonctions faciles à tester sont souvent celles qui :

```text
input
→ output
```

sans dépendre directement de :

```text
fichier réel
base réelle
réseau
```

Exemple :

```python
def normalize_name(value):
    return (
        value
        .strip()
        .lower()
    )
```

Test :

```python
def test_normalize_name():
    assert (
        normalize_name(
            " Alice "
        )
        == "alice"
    )
```

---

# 38. Test d’intégration

## Guide pratique

Un test d’intégration couvre plusieurs briques :

```text
DataFrame
→ transformation
→ ORM
→ DB
```

Exemple conceptuel :

```text
input valide
→ ingestion
→ query DB
→ vérification
```

---

# 39. Unit test vs integration test

## Guide pratique

```text
UNIT
→ une petite unité de logique

INTEGRATION
→ plusieurs composants ensemble
```

Pendant l’épreuve :

```text
quelques tests unitaires ciblés
+
au moins une vérification end-to-end
```

est une stratégie raisonnable si le temps le permet.

---

# 40. Fixture pytest — option utile

## Guide pratique

```python
import pytest


@pytest.fixture
def valid_df():
    return pd.DataFrame(
        {
            "id": [1, 2],
            "name": [
                "Alice",
                "Bob",
            ],
        }
    )
```

Puis :

```python
def test_no_duplicates(
    valid_df,
):
    assert not (
        valid_df["id"]
        .duplicated()
        .any()
    )
```

> Les fixtures ne sont pas imposées par le support ; elles servent à éviter la duplication dans les tests.

---

# 41. Test d’unicité

## Guide pratique

```python
def test_id_is_unique(
    valid_df,
):
    assert (
        valid_df["id"]
        .is_unique
    )
```

---

# 42. Test de non-nullité

## Guide pratique

```python
def test_id_is_not_null(
    valid_df,
):
    assert not (
        valid_df["id"]
        .isna()
        .any()
    )
```

---

# 43. Test de cardinalité minimale

## Guide pratique

Exemple :

```python
def test_dataset_not_empty(
    valid_df,
):
    assert len(valid_df) > 0
```

---

# 44. Test de colonnes inattendues

## Guide pratique

Selon le besoin :

```python
EXPECTED_COLUMNS = {
    "id",
    "name",
}
```

Test strict :

```python
def test_exact_schema(
    valid_df,
):
    assert (
        set(valid_df.columns)
        == EXPECTED_COLUMNS
    )
```

Ou souple :

```python
assert EXPECTED_COLUMNS.issubset(
    valid_df.columns
)
```

---

# 45. Strict vs permissif

## Guide pratique

```text
strict
→ aucune colonne supplémentaire

permissif
→ colonnes minimales requises
```

Le choix dépend du sujet.

---

# 46. Tester le comportement plutôt que l’implémentation

## Guide pratique

Préférer vérifier :

```text
doublon rejeté
```

plutôt que :

```text
la fonction interne X a été appelée
```

Objectif :

```text
tester ce que le système garantit
```

---

# 47. Test d’ingestion avec base réelle

## Guide pratique

Dans une simulation complète, on peut utiliser la base Docker du projet.

Pattern :

```text
docker compose up -d
pytest
docker compose down
```

Attention au nettoyage des données entre tests.

---

# 48. Isolation des tests

## Guide pratique

Deux tests ne devraient pas dépendre l’un de l’autre.

À éviter :

```text
test_2 suppose
que test_1 a inséré une ligne
```

Préférer :

```text
chaque test prépare
son propre état
```

---

# 49. Nettoyage de session DB

## Guide pratique

Selon l’architecture :

```text
rollback
truncate
fixture dédiée
base de test
```

Le support ne prescrit aucune de ces méthodes ; elles sont des options de préparation.

---

# 50. Risque de tester trop de choses

## Guide pratique

En 4 heures :

```text
20 tests sophistiqués
```

peuvent être moins utiles que :

```text
4–6 tests
bien ciblés
```

sur les critères explicitement annoncés.

---

# 51. Le minimum viable de tests

## Guide pratique

Si le temps est extrêmement contraint :

```python
def test_valid_ingestion():
    ...
```

```python
def test_missing_column_is_rejected():
    ...
```

```python
def test_duplicate_is_detected():
    ...
```

```python
def test_invalid_input_raises():
    ...
```

Cela couvre directement :

```text
nominal
schéma
doublon
erreur
```

---

# 52. Pattern complet `validate_dataframe`

## Guide pratique

```python
REQUIRED_COLUMNS = {
    "id",
    "name",
    "category",
}


def validate_dataframe(df):
    missing = (
        REQUIRED_COLUMNS
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            f"Missing columns: "
            f"{sorted(missing)}"
        )

    if df["id"].isna().any():
        raise ValueError(
            "Null id detected"
        )

    if df["id"].duplicated().any():
        raise ValueError(
            "Duplicate id detected"
        )
```

---

# 53. Tests associés

## Guide pratique

```python
def test_valid_dataframe():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "name": [
                "Alice",
                "Bob",
            ],
            "category": [
                "a",
                "b",
            ],
        }
    )

    validate_dataframe(df)
```

```python
def test_missing_column():
    df = pd.DataFrame(
        {
            "id": [1],
            "name": ["Alice"],
        }
    )

    with pytest.raises(
        ValueError
    ):
        validate_dataframe(df)
```

```python
def test_duplicate_id():
    df = pd.DataFrame(
        {
            "id": [1, 1],
            "name": [
                "Alice",
                "Alice",
            ],
            "category": [
                "a",
                "a",
            ],
        }
    )

    with pytest.raises(
        ValueError
    ):
        validate_dataframe(df)
```

---

# 54. Mini-exercice 1 — Schéma

Créer :

```text
required = id, name, category
```

Puis tester :

```text
dataset complet
dataset sans category
```

---

# 55. Mini-exercice 2 — Doublons

Créer :

```text
id = [1, 2, 2]
```

Le test doit échouer.

---

# 56. Mini-exercice 3 — Null PK

Créer :

```text
id = [1, None]
```

Le test doit échouer.

---

# 57. Mini-exercice 4 — Domaine

Créer :

```text
status = active / inactive
```

puis tester :

```text
status = unknown
```

---

# 58. Mini-exercice 5 — ETL complet

Pipeline :

```text
JSON
→ extract
→ validate
→ transform
→ output
```

Créer des tests pour :

```text
fichier manquant
colonne manquante
doublon
output valide
```

---

# 59. Mini-exercice 6 — ORM / ingestion

Pipeline :

```text
DataFrame
→ User(...)
→ session.add
→ commit
```

Tester :

```text
ligne présente après commit
```

Puis tester :

```text
réingestion du même ID
```

selon la stratégie retenue.

---

# 60. Checklist avant lancement de `pytest`

```text
[ ] dépendance installée
[ ] fichiers test_*.py
[ ] imports corrects
[ ] fonctions test_*
[ ] données de test minimales
[ ] exceptions explicites
[ ] base de test prête si nécessaire
```

---

# 61. Checklist après lancement

```text
[ ] tous les tests attendus exécutés
[ ] aucun ERROR d’import
[ ] aucun FAILED non compris
[ ] messages d’erreur lisibles
[ ] comportement cohérent avec le sujet
```

---

# 62. Debug pytest — import error

## Guide pratique

Vérifier :

```text
working directory
PYTHONPATH
structure du projet
__init__.py si nécessaire
nom du module
```

Dans une épreuve courte, éviter une structure de packaging inutilement complexe.

---

# 63. Debug — test passe alors qu’il devrait échouer

## Guide pratique

Questions :

```text
le bon code est-il appelé ?
l’assertion est-elle correcte ?
l’exception est-elle réellement levée ?
le jeu de données de test contient-il bien l’anomalie ?
```

---

# 64. Debug — test dépendant d’un autre

## Guide pratique

Symptôme :

```text
test seul
→ KO

suite complète
→ OK
```

ou inversement.

Cause probable :

```text
état partagé
```

---

# 65. Documentation des tests

## Attendu source

Le fichier synthétique doit expliquer les choix techniques et les pistes d’amélioration.

## Guide pratique

Pour les tests, documenter brièvement :

```text
Tests réalisés
- schéma
- doublons
- erreurs

Objectif
- sécuriser l’ingestion

Limites
- cas couverts / non couverts
```

---

# 66. Exemple de synthèse courte

## Guide pratique

```text
Les tests se concentrent sur les trois risques annoncés
dans le sujet : erreurs d’entrée, doublons et conformité
du schéma. Un test nominal vérifie également que
l’ingestion aboutit sur un dataset valide.
```

---

# 67. Temps cible de préparation

## Guide pratique

Pendant un examen blanc :

```text
5 min
→ écrire les 3–4 tests prioritaires

5 min
→ exécuter et corriger

5 min
→ ajouter un cas si temps disponible
```

Objectif :

```text
≈ 10–15 min
```

pour le minimum de tests ciblés.

> Cette estimation est une stratégie de préparation, pas un timing officiel.

---

# 68. Priorité absolue

## Guide pratique

Si le temps manque :

```text
1. conformité au schéma
2. doublons
3. erreur critique
4. happy path
```

car ces points correspondent directement au périmètre explicite du support.

---

# 69. Questions flash

1. Quels sont les trois axes de test explicitement annoncés ?
2. Comment vérifier une colonne manquante ?
3. Comment détecter un doublon sur `id` ?
4. Comment vérifier qu’une PK n’est pas nulle ?
5. À quoi sert `pytest.raises` ?
6. Comment lancer tous les tests ?
7. Comment lancer un seul fichier ?
8. Quelle différence entre test unitaire et test d’intégration ?
9. Pourquoi éviter `except Exception: pass` ?
10. Quel est le minimum viable de tests pour cette épreuve ?

---

# 70. Réponses flash

```text
1. erreurs, doublons, conformité au schéma.
2. required_columns - set(df.columns).
3. df["id"].duplicated().any().
4. df["id"].isna().any().
5. vérifier qu’une exception attendue est levée.
6. pytest.
7. pytest tests/test_ingestion.py.
8. unitaire = logique isolée ; intégration = plusieurs briques ensemble.
9. masque les erreurs et rend le comportement difficile à tester.
10. nominal + schéma + doublon + erreur critique.
```

---

# 71. Cheatsheet 30 secondes

```python
REQUIRED = {
    "id",
    "name",
}


def validate(df):
    missing = (
        REQUIRED
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            f"Missing: {missing}"
        )

    if df["id"].isna().any():
        raise ValueError(
            "Null id"
        )

    if df["id"].duplicated().any():
        raise ValueError(
            "Duplicate id"
        )
```

Tests :

```python
def test_valid():
    validate(valid_df)
```

```python
def test_duplicate():
    with pytest.raises(
        ValueError
    ):
        validate(duplicate_df)
```

---

# 72. Niveau à viser

```text
NIVEAU 1
assert
pytest
raises

    ↓

NIVEAU 2
schéma
nulls
doublons

    ↓

NIVEAU 3
tests ingestion
DB / ORM

    ↓

NIVEAU 4
scénario end-to-end
```

---

# 73. Checkpoint avant le template projet

Être capable de produire rapidement :

```text
[ ] test nominal
[ ] test colonne manquante
[ ] test doublon
[ ] test erreur
[ ] pytest vert
```

Puis seulement ajouter :

```text
types
domaines
relations
cas supplémentaires
```

si le temps le permet.

---

# 74. Résumé final

Le support ne demande pas une usine à tests.

Il demande explicitement de fiabiliser l’ingestion sur :

```text
ERREURS
  +
DOUBLONS
  +
SCHÉMA
```

La stratégie la plus adaptée à une épreuve de 4 heures est donc :

```text
tester peu
mais tester les risques annoncés
```

avec une chaîne simple :

```text
validate
→ ingest
→ verify
```

---

# 75. Document suivant

```text
08_RNCP_38919_BLOC_2_TEMPLATE_PROJECT.md
```

Objectif :

> assembler toutes les briques déjà travaillées — ETL Python, SQLAlchemy/ORM,
> Docker Compose, Machine Learning et tests — dans un squelette de projet
> cohérent et réutilisable pour les entraînements Bloc 2.
