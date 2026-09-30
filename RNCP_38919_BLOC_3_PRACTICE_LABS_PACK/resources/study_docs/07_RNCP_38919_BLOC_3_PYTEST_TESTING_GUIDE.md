# 07 — RNCP 38919 — Bloc 3
# Guide Pytest et stratégie de tests

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Attendu source** : notion explicitement annoncée dans le support DataScientest.
> - **Guide pratique** : exemples, patterns et mini-labs proposés pour la préparation.
>
> Le support annonce explicitement :
>
> ```text
> Pytest
> ```
>
> Il ne précise pas, dans la page fournie :
>
> ```text
> le nombre exact de tests
> leur structure
> les fixtures obligatoires
> les plugins à utiliser
> un taux de couverture
> ```
>
> Les exemples ci-dessous sont donc des **patterns de préparation**.

---

# 1. Position de Pytest dans le Bloc 3

## Attendu source

Le support cite :

```text
Pytest
```

dans le périmètre officiel.

## Modèle mental

```text
CODE
 ↓
TESTS
 ↓
PYTEST
 ↓
PASS / FAIL
 ↓
GITLAB CI
```

Dans le Bloc 3, Pytest doit surtout être compris comme un maillon de :

```text
validation locale
+
validation CI
```

---

# 2. Lancer les tests

## Guide pratique

Commande minimale :

```bash
pytest
```

Mode verbeux :

```bash
pytest -v
```

---

# 3. Convention de nommage

## Guide pratique

Structure courante :

```text
tests/
├── test_api.py
├── test_model.py
└── test_utils.py
```

Convention :

```text
test_*.py
```

et fonctions :

```text
test_*
```

---

# 4. Premier test

```python
def test_sum():
    assert 2 + 2 == 4
```

Exécuter :

```bash
pytest -v
```

---

# 5. Assertions

## Guide pratique

```python
assert value == expected
```

Exemple :

```python
def test_status():
    status = "ok"

    assert status == "ok"
```

---

# 6. Tester un booléen

```python
def test_positive():
    value = 10

    assert value > 0
```

---

# 7. Tester une collection

```python
def test_items():
    items = [
        "a",
        "b",
    ]

    assert len(items) == 2
```

---

# 8. Tester une exception

## Guide pratique

```python
import pytest


def validate(
    value: int,
) -> None:
    if value < 0:
        raise ValueError(
            "negative value"
        )


def test_negative_value():
    with pytest.raises(
        ValueError
    ):
        validate(
            -1
        )
```

---

# 9. Pourquoi tester les erreurs

Même si la page source ne détaille pas les cas de test, la logique de préparation est :

```text
happy path
+
error path
```

Exemple :

```text
entrée valide
→ succès

entrée invalide
→ erreur contrôlée
```

---

# 10. Tester une fonction pure

```python
def double(
    value: int,
) -> int:
    return value * 2


def test_double():
    assert double(
        3
    ) == 6
```

---

# 11. Organisation simple

```text
project/
│
├── app/
│   └── ...
│
├── tests/
│   ├── test_api.py
│   └── test_logic.py
│
└── requirements.txt
```

---

# 12. Tester FastAPI avec Pytest

## Guide pratique

Le support annonce :

```text
FastAPI
```

et :

```text
Pytest
```

Il est donc cohérent de pratiquer leur combinaison.

Pattern :

```python
from fastapi.testclient import (
    TestClient,
)

from app.main import (
    app,
)


client = TestClient(
    app
)
```

> `TestClient` n’est pas cité explicitement dans la page source ; il s’agit d’un outil de pratique utile.

---

# 13. Test d’un endpoint GET

```python
def test_health():
    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )
```

---

# 14. Tester le JSON de réponse

```python
def test_health_body():
    response = client.get(
        "/health"
    )

    assert response.json() == {
        "status": "ok"
    }
```

---

# 15. Test d’un endpoint POST

```python
def test_predict():
    response = client.post(
        "/predict",
        json={
            "value": 42
        },
    )

    assert (
        response.status_code
        == 200
    )
```

---

# 16. Tester le payload retourné

```python
def test_predict_body():
    response = client.post(
        "/predict",
        json={
            "value": 42
        },
    )

    body = response.json()

    assert (
        "prediction"
        in body
    )
```

---

# 17. Tester une validation Pydantic

Payload invalide :

```python
def test_predict_invalid_type():
    response = client.post(
        "/predict",
        json={
            "value": "abc"
        },
    )

    assert (
        response.status_code
        != 200
    )
```

---

# 18. Test métier

Exemple :

```python
def test_negative_value():
    response = client.post(
        "/predict",
        json={
            "value": -1
        },
    )

    assert (
        response.status_code
        == 400
    )
```

---

# 19. Tester un endpoint absent

```python
def test_unknown_route():
    response = client.get(
        "/unknown"
    )

    assert (
        response.status_code
        == 404
    )
```

---

# 20. FastAPI — matrice de tests minimale

## Guide pratique

```text
GET /health
→ 200

POST /predict payload valide
→ 200

POST /predict payload invalide
→ erreur

route inconnue
→ 404
```

---

# 21. Tests et `joblib`

Le support annonce également :

```text
joblib
```

Pattern de practice :

```text
sauvegarde
→ fichier créé

chargement
→ objet lisible
```

---

# 22. Tester un artefact joblib

```python
from pathlib import Path

import joblib


def test_joblib_roundtrip(
    tmp_path,
):
    path = (
        tmp_path
        / "artifact.joblib"
    )

    artifact = {
        "name": "bloc3"
    }

    joblib.dump(
        artifact,
        path,
    )

    loaded = joblib.load(
        path
    )

    assert (
        loaded
        == artifact
    )
```

---

# 23. `tmp_path`

## Guide pratique

`tmp_path` est une fixture Pytest courante permettant d’utiliser un dossier temporaire.

> `tmp_path` n’est pas cité dans la page source ; il s’agit d’un outil de pratique.

---

# 24. Fixtures

## Guide pratique

Pattern :

```python
import pytest


@pytest.fixture
def payload():
    return {
        "value": 42
    }
```

Puis :

```python
def test_payload(
    payload,
):
    assert (
        payload["value"]
        == 42
    )
```

---

# 25. Pourquoi utiliser une fixture

Pattern mental :

```text
setup réutilisable
↓
fixture
↓
plusieurs tests
```

---

# 26. Fixture client FastAPI

```python
import pytest

from fastapi.testclient import (
    TestClient,
)

from app.main import (
    app,
)


@pytest.fixture
def client():
    return TestClient(
        app
    )
```

Puis :

```python
def test_health(
    client,
):
    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )
```

---

# 27. Paramétrisation

## Guide pratique

Pattern :

```python
import pytest


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, 2),
        (2, 4),
        (3, 6),
    ],
)
def test_double(
    value,
    expected,
):
    assert (
        value * 2
        == expected
    )
```

> La paramétrisation n’est pas citée dans la source ; elle est ajoutée comme pratique utile.

---

# 28. Tester les variables d’environnement

```python
def test_env_var(
    monkeypatch,
):
    monkeypatch.setenv(
        "APP_ENV",
        "test",
    )

    import os

    assert (
        os.getenv(
            "APP_ENV"
        )
        == "test"
    )
```

> `monkeypatch` est une fixture Pytest de pratique, non explicitement mentionnée dans le support.

---

# 29. Pourquoi tester la configuration

Le Bloc 3 annonce :

```text
variables d’environnement
```

et :

```text
Pytest
```

Un bon lab peut donc vérifier :

```text
config présente
config absente
valeur par défaut
```

---

# 30. Exemple de fonction config

```python
import os


def get_api_port() -> int:
    return int(
        os.getenv(
            "API_PORT",
            "8000",
        )
    )
```

Test :

```python
def test_default_port(
    monkeypatch,
):
    monkeypatch.delenv(
        "API_PORT",
        raising=False,
    )

    assert (
        get_api_port()
        == 8000
    )
```

---

# 31. Tester une URL configurée

```python
def get_api_url():
    import os

    return os.getenv(
        "API_URL",
        "http://localhost:8000",
    )
```

Puis :

```python
def test_api_url_default(
    monkeypatch,
):
    monkeypatch.delenv(
        "API_URL",
        raising=False,
    )

    assert (
        get_api_url()
        == "http://localhost:8000"
    )
```

---

# 32. Tests unitaires vs intégration

## Guide pratique

### Unit test

```text
fonction isolée
```

Exemple :

```text
validation Pydantic
fonction métier
config
```

### Integration test

```text
plusieurs briques ensemble
```

Exemple :

```text
FastAPI
+
joblib
+
HTTP
```

Le support ne demande pas explicitement cette classification, mais elle aide à structurer la préparation.

---

# 33. Test d’intégration API

Pattern :

```text
request HTTP
↓
FastAPI
↓
Pydantic
↓
logic
↓
response
```

---

# 34. Tests et Docker

Le support annonce également :

```text
Docker
```

Une stratégie de practice consiste à vérifier d’abord :

```text
tests locaux
```

avant :

```text
docker build
```

Chaîne :

```text
pytest
↓
docker build
```

---

# 35. Pytest dans GitLab CI

## Guide pratique

Le support annonce :

```text
GitLab
```

et :

```text
Pytest
```

Pattern :

```yaml
stages:
  - test

tests:
  stage: test
  script:
    - pytest -v
```

---

# 36. Pourquoi tester avant build

Pipeline logique :

```text
TEST KO
→ stop

TEST OK
→ build Docker
```

Cela évite de construire une image contenant un code déjà connu comme défaillant.

---

# 37. Pipeline test + build

```yaml
stages:
  - test
  - build

tests:
  stage: test
  script:
    - pytest -v

build:
  stage: build
  script:
    - docker build -t app .
```

---

# 38. Runner shell + Pytest

Avec un Runner `shell`, vérifier :

```bash
which python
which pytest
```

si un job échoue avec :

```text
command not found
```

---

# 39. Installer les dépendances dans le job

Pattern de practice :

```yaml
tests:
  stage: test
  script:
    - python -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt
    - pytest -v
```

> Le support n’impose pas ce pattern ; il est proposé pour les labs.

---

# 40. Lire une erreur Pytest

Toujours identifier :

```text
nom du test
type d’exception
ligne
valeur attendue
valeur obtenue
```

---

# 41. Test qui échoue volontairement

```python
def test_failure():
    assert 1 == 2
```

But :

```text
observer la sortie Pytest
```

puis corriger.

---

# 42. Mode stop au premier échec

Pattern utile :

```bash
pytest \
  -x
```

> `-x` n’est pas cité dans le support ; option de pratique.

---

# 43. Mode silencieux

```bash
pytest \
  -q
```

> Option de pratique.

---

# 44. Filtrer par nom

```bash
pytest \
  -k health
```

> Option de pratique.

---

# 45. Un seul fichier

```bash
pytest \
  tests/test_api.py
```

---

# 46. Un seul test

```bash
pytest \
  tests/test_api.py::test_health
```

---

# 47. Tester rapidement pendant l’examen

## Stratégie proposée

Au lieu de relancer toute la suite après chaque petit changement :

```text
test ciblé
↓
fichier
↓
suite complète
```

Exemple :

```bash
pytest \
  tests/test_api.py::test_health
```

puis :

```bash
pytest -v
```

---

# 48. Matrice de tests Bloc 3

## Guide pratique

### Configuration

```text
env var présente
env var absente
```

### API

```text
GET valide
POST valide
payload invalide
route absente
```

### Artefact

```text
joblib load
fichier absent
```

### Observabilité

```text
/metrics accessible
```

### Pipeline

```text
pytest passe dans GitLab CI
```

---

# 49. Tester `/metrics`

Pattern :

```python
def test_metrics(
    client,
):
    response = client.get(
        "/metrics"
    )

    assert (
        response.status_code
        == 200
    )
```

Ce test devient pertinent si l’Instrumentator a été activé.

---

# 50. Tester un modèle absent

Pattern :

```python
import pytest


def load_model(
    path,
):
    if not path.exists():
        raise FileNotFoundError(
            path
        )


def test_model_missing(
    tmp_path,
):
    path = (
        tmp_path
        / "missing.joblib"
    )

    with pytest.raises(
        FileNotFoundError
    ):
        load_model(
            path
        )
```

---

# 51. Tester sans vrai modèle ML

## Guide pratique

Pour un examen de DevOps, il peut être utile de ne pas dépendre d’un vrai entraînement lourd dans les tests.

Pattern :

```text
fake / stub simple
```

afin de tester :

```text
API
plomberie
format des réponses
```

> Les doubles de test ne sont pas annoncés dans la source ; il s’agit d’une stratégie pratique.

---

# 52. Test de contrat simple

```python
def test_predict_contract(
    client,
):
    response = client.post(
        "/predict",
        json={
            "value": 1
        },
    )

    body = response.json()

    assert (
        "prediction"
        in body
    )
```

---

# 53. Test de type

```python
def test_prediction_type(
    client,
):
    response = client.post(
        "/predict",
        json={
            "value": 1
        },
    )

    body = response.json()

    assert isinstance(
        body["prediction"],
        int,
    )
```

---

# 54. Test de status

```python
def test_health_status(
    client,
):
    assert (
        client
        .get(
            "/health"
        )
        .status_code
        == 200
    )
```

---

# 55. Anti-pattern — test trop large

Éviter un test unique qui fait :

```text
FastAPI
+
Docker
+
GitLab
+
Kubernetes
+
Prometheus
+
Grafana
```

dans une seule fonction Pytest.

Pour le practice :

```text
petits tests ciblés
+
quelques tests d’intégration
```

---

# 56. Anti-pattern — dépendance à l’ordre

Éviter :

```text
test_1 crée une donnée
test_2 suppose que test_1 a déjà tourné
```

Les tests doivent autant que possible être indépendants.

---

# 57. Anti-pattern — `try/except` silencieux

Éviter :

```python
try:
    ...
except Exception:
    pass
```

dans les tests.

Cela peut masquer une vraie erreur.

---

# 58. Anti-pattern — assertion vide

Éviter :

```python
def test_api():
    client.get(
        "/health"
    )
```

sans vérifier :

```text
status
body
ou comportement
```

---

# 59. Anti-pattern — tester uniquement le happy path

Il faut au moins penser :

```text
valide
+
invalide
```

---

# 60. Mini-lab 1 — fonction pure

Créer :

```python
def add(a, b):
    return a + b
```

Écrire trois tests.

---

# 61. Mini-lab 2 — exception

Créer :

```python
def divide(a, b):
    ...
```

Tester :

```text
division normale
division par zéro
```

---

# 62. Mini-lab 3 — env vars

Créer :

```python
get_app_mode()
```

Tester :

```text
APP_MODE présent
APP_MODE absent
```

---

# 63. Mini-lab 4 — FastAPI health

Créer :

```text
GET /health
```

Puis test :

```text
status = 200
body = {"status":"ok"}
```

---

# 64. Mini-lab 5 — Pydantic invalid

Envoyer :

```json
{
  "value": "abc"
}
```

et vérifier que la requête n’est pas acceptée comme un cas valide.

---

# 65. Mini-lab 6 — `/predict`

Tester :

```text
payload valide
réponse contient prediction
```

---

# 66. Mini-lab 7 — `/metrics`

Activer :

```text
prometheus-fastapi-instrumentator
```

Puis tester :

```text
GET /metrics
→ 200
```

---

# 67. Mini-lab 8 — joblib

Sauvegarder un objet simple dans :

```text
tmp_path
```

puis le recharger et comparer.

---

# 68. Mini-lab 9 — CI

Créer :

```text
.gitlab-ci.yml
```

avec :

```text
pytest -v
```

Faire échouer volontairement un test.

Observer :

```text
pipeline rouge
```

Puis corriger.

---

# 69. Mini-lab 10 — test + build

Pipeline :

```text
pytest
↓
docker build
```

Objectif :

```text
build seulement si tests OK
```

---

# 70. Checklist examen — Pytest

```text
[ ] tests/ existe
[ ] fichiers test_*.py
[ ] fonctions test_*
[ ] happy path
[ ] erreur
[ ] API testée
[ ] payload invalide testé
[ ] pytest -v passe
[ ] CI lance pytest
```

---

# 71. Debug 60 secondes

```text
Test découvert ?
      ↓
Import OK ?
      ↓
Fixture OK ?
      ↓
Endpoint correct ?
      ↓
Status attendu ?
      ↓
Body attendu ?
```

---

# 72. Questions flash

1. Quel framework de test est explicitement annoncé ?
2. Quelle commande lance les tests ?
3. Quelle convention de fichier est courante ?
4. Comment tester une exception ?
5. Pourquoi tester un payload invalide ?
6. Comment relier Pytest à FastAPI ?
7. Comment relier Pytest à GitLab CI ?
8. Pourquoi faire passer les tests avant Docker build ?
9. Que vérifier si `pytest` n’est pas trouvé dans le Runner ?
10. Quels sont les quatre tests API minimums utiles ?

---

# 73. Réponses flash

```text
1. Pytest.
2. pytest / pytest -v.
3. test_*.py.
4. pytest.raises(...).
5. vérifier la validation et les erreurs.
6. TestClient + endpoints.
7. job CI exécutant pytest.
8. éviter de builder un code déjà défaillant.
9. PATH, venv, installation, contexte utilisateur.
10. health, POST valide, payload invalide, route inconnue.
```

---

# 74. Cheatsheet 30 secondes

```python
import pytest


def test_value():
    assert 2 + 2 == 4


def test_error():
    with pytest.raises(
        ValueError
    ):
        raise ValueError
```

FastAPI :

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )
```

CI :

```yaml
tests:
  stage: test
  script:
    - pytest -v
```

---

# 75. Fil rouge à retenir

```text
CODE
 ↓
PYTEST
 ↓
VALIDATION
 ↓
GITLAB CI
 ↓
BUILD
```

---

# 76. Document suivant

```text
08_RNCP_38919_BLOC_3_KUBERNETES_GUIDE.md
```

Objectif :

> approfondir les six objets Kubernetes explicitement annoncés :
> `Namespace`, `PersistentVolume`, `PersistentVolumeClaim`,
> `ConfigMap`, `Service` et `Deployment`,
> avec manifests YAML, relations entre objets et stratégie de debug.
