# 06 — RNCP 38919 — Bloc 3
# Guide FastAPI, Pydantic et exposition d’API

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Attendu source** : élément explicitement annoncé dans le support DataScientest.
> - **Guide pratique** : exemples de code et mini-labs proposés pour préparer l’épreuve.
>
> Le support annonce explicitement :
>
> ```text
> FastAPI
> pydantic.BaseModel
> curl
> prometheus-fastapi-instrumentator
> ```
>
> Il n’impose pas, dans la page fournie, une liste précise d’endpoints ni un modèle métier spécifique.
> Les exemples ci-dessous servent donc de **patterns de préparation**.

---

# 1. Position de FastAPI dans le Bloc 3

## Attendu source

Le support cite :

```text
FastAPI
```

ainsi que :

```text
pydantic.BaseModel
```

et :

```text
prometheus-fastapi-instrumentator
```

## Modèle mental

```text
Client
  ↓
HTTP
  ↓
FastAPI endpoint
  ↓
Pydantic validation
  ↓
Business logic
  ↓
Response JSON
```

---

# 2. Application FastAPI minimale

## Guide pratique

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "ok"
    }
```

---

# 3. Lancer l’application

Pattern de pratique :

```bash
uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000
```

> `uvicorn` n’est pas cité explicitement dans la page source, mais il constitue un moyen courant de lancer une application FastAPI pour les entraînements.

---

# 4. Tester avec `curl`

## Attendu source

Le support cite explicitement :

```text
curl
```

## Guide pratique

```bash
curl \
  http://localhost:8000/
```

Réponse attendue :

```json
{
  "status": "ok"
}
```

---

# 5. Endpoint `/health`

## Guide pratique

```python
@app.get("/health")
def health():
    return {
        "status": "ok"
    }
```

Tester :

```bash
curl \
  http://localhost:8000/health
```

---

# 6. Pydantic `BaseModel`

## Attendu source

Le support annonce :

```text
la définition de classe Python
à l’aide de pydantic.BaseModel
```

## Guide pratique

```python
from pydantic import BaseModel


class PredictionRequest(
    BaseModel
):
    value: float
```

---

# 7. Rôle de `BaseModel`

Modèle mental :

```text
JSON
 ↓
BaseModel
 ↓
validation
 ↓
objet Python
```

Exemple :

```json
{
  "value": 42.0
}
```

devient un objet de type :

```python
PredictionRequest
```

---

# 8. Endpoint POST

```python
@app.post("/predict")
def predict(
    payload: PredictionRequest,
):
    return {
        "prediction": 0,
        "value": payload.value,
    }
```

---

# 9. Tester un POST avec `curl`

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 42}' \
  http://localhost:8000/predict
```

---

# 10. Validation Pydantic

## Guide pratique

Si :

```python
class PredictionRequest(
    BaseModel
):
    value: float
```

et que le client envoie un payload incompatible,
FastAPI s’appuie sur Pydantic pour valider l’entrée.

---

# 11. Plusieurs champs

```python
class PredictionRequest(
    BaseModel
):
    feature_1: float
    feature_2: float
    category: str
```

Payload :

```json
{
  "feature_1": 1.2,
  "feature_2": 3.4,
  "category": "A"
}
```

---

# 12. Valeur optionnelle

Pattern de pratique :

```python
class PredictionRequest(
    BaseModel
):
    value: float
    comment: str | None = None
```

---

# 13. Réponse structurée

Pattern :

```python
class PredictionResponse(
    BaseModel
):
    prediction: int
```

Puis :

```python
@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    payload: PredictionRequest,
):
    return PredictionResponse(
        prediction=0
    )
```

> `response_model` n’est pas mentionné dans la page source ; cet exemple est ajouté comme pratique FastAPI.

---

# 14. Variables d’environnement + FastAPI

Le support annonce séparément :

```text
variables d’environnement
```

et :

```text
FastAPI
```

Un pattern cohérent de practice est :

```python
import os

api_mode = os.getenv(
    "API_MODE",
    "development",
)
```

Puis :

```python
@app.get("/config")
def config():
    return {
        "mode": api_mode
    }
```

---

# 15. FastAPI + `joblib`

Le support annonce également :

```text
joblib
```

Un pattern d’entraînement utile est :

```text
FastAPI
↓
joblib.load
↓
model.predict
```

---

# 16. Chargement d’un artefact

```python
import os
import joblib

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/model.joblib",
)

model = joblib.load(
    MODEL_PATH
)
```

---

# 17. Endpoint de prédiction

```python
@app.post("/predict")
def predict(
    payload: PredictionRequest,
):
    prediction = model.predict(
        [[payload.value]]
    )

    return {
        "prediction":
        prediction[0]
    }
```

> Le support n’impose pas ce format de modèle ni cet endpoint précis.

---

# 18. Gérer un modèle absent

Pattern :

```python
from pathlib import Path

model_path = Path(
    MODEL_PATH
)

if not model_path.exists():
    raise RuntimeError(
        f"Model not found: "
        f"{model_path}"
    )
```

---

# 19. Séparer configuration et code

Pattern mental :

```text
MODEL_PATH
API_MODE
API_PORT
```

dans :

```text
environnement
```

et non codés en dur.

---

# 20. Structure de projet de pratique

```text
app/
├── __init__.py
├── main.py
├── schemas.py
└── model.py

models/
└── model.joblib

tests/
└── test_api.py

requirements.txt
Dockerfile
```

> Structure proposée pour les labs, non imposée par la source.

---

# 21. `schemas.py`

```python
from pydantic import BaseModel


class PredictionRequest(
    BaseModel
):
    value: float


class PredictionResponse(
    BaseModel
):
    prediction: int
```

---

# 22. `main.py`

```python
from fastapi import FastAPI

from app.schemas import (
    PredictionRequest,
)

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/predict")
def predict(
    payload: PredictionRequest,
):
    return {
        "prediction": 0
    }
```

---

# 23. Documentation automatique

## Guide pratique

FastAPI expose généralement une documentation interactive.

Pattern à connaître en entraînement :

```text
/docs
```

et :

```text
/openapi.json
```

> La page source ne cite pas explicitement ces endpoints ; ils sont inclus comme repères utiles de pratique.

---

# 24. `curl` — vérifier `/docs`

La documentation HTML n’est pas idéale à lire avec `curl`, mais on peut vérifier sa disponibilité :

```bash
curl \
  -I \
  http://localhost:8000/docs
```

---

# 25. Tester le status HTTP

```bash
curl \
  -i \
  http://localhost:8000/health
```

---

# 26. Voir les détails de connexion

```bash
curl \
  -v \
  http://localhost:8000/health
```

---

# 27. Erreur de route

Tester :

```bash
curl \
  -i \
  http://localhost:8000/unknown
```

Permet de vérifier le comportement sur une route inexistante.

---

# 28. Erreur de validation

Payload invalide :

```bash
curl \
  -i \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value":"not-a-number"}' \
  http://localhost:8000/predict
```

Objectif :

```text
observer la validation FastAPI / Pydantic
```

---

# 29. FastAPI et exceptions

Pattern :

```python
from fastapi import (
    HTTPException,
)
```

Exemple :

```python
if payload.value < 0:
    raise HTTPException(
        status_code=400,
        detail="value must be positive",
    )
```

> `HTTPException` n’est pas cité dans la page source ; exemple de pratique.

---

# 30. Endpoint root vs health

Pattern de révision :

```text
/
→ information générale

/health
→ statut applicatif

/predict
→ logique métier

/metrics
→ observabilité
```

---

# 31. FastAPI + Prometheus Instrumentator

## Attendu source

Le support cite :

```text
prometheus-fastapi-instrumentator
```

## Guide pratique

Pattern :

```python
from prometheus_fastapi_instrumentator import (
    Instrumentator,
)


Instrumentator().instrument(
    app
).expose(
    app
)
```

---

# 32. Chaîne d’observabilité

```text
FastAPI request
      ↓
instrumentator
      ↓
metrics
      ↓
Prometheus
      ↓
PromQL
      ↓
Grafana
```

---

# 33. Endpoint `/metrics`

Dans un setup de practice avec Instrumentator :

```bash
curl \
  http://localhost:8000/metrics
```

Objectif :

```text
voir des métriques exploitables par Prometheus
```

---

# 34. App complète de practice

```python
import os
from pathlib import Path

import joblib

from fastapi import (
    FastAPI,
    HTTPException,
)

from pydantic import (
    BaseModel,
)

from prometheus_fastapi_instrumentator import (
    Instrumentator,
)


app = FastAPI()


MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/model.joblib",
)


class PredictionRequest(
    BaseModel
):
    value: float


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/predict")
def predict(
    payload: PredictionRequest,
):
    if payload.value < 0:
        raise HTTPException(
            status_code=400,
            detail="value must be positive",
        )

    return {
        "prediction": 0
    }


Instrumentator().instrument(
    app
).expose(
    app
)
```

---

# 35. `requirements.txt` de practice

```text
fastapi
uvicorn
pydantic
joblib
pytest
prometheus-fastapi-instrumentator
```

> Liste de pratique dérivée des thèmes annoncés ; le support ne donne pas un `requirements.txt` officiel.

---

# 36. Dockeriser FastAPI

Pattern :

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY . .

CMD [
  "uvicorn",
  "app.main:app",
  "--host",
  "0.0.0.0",
  "--port",
  "8000"
]
```

---

# 37. Construire

```bash
docker build \
  -t bloc3-api .
```

---

# 38. Lancer

```bash
docker run \
  --rm \
  -p 8000:8000 \
  bloc3-api
```

---

# 39. Tester le container

```bash
curl \
  http://localhost:8000/health
```

Puis :

```bash
curl \
  http://localhost:8000/metrics
```

---

# 40. FastAPI dans Docker — piège d’écoute

Si l’application écoute uniquement sur :

```text
127.0.0.1
```

dans le container, elle peut être inaccessible depuis l’hôte.

Pattern de practice :

```text
--host 0.0.0.0
```

---

# 41. Port

```text
container
8000

host
8000
```

Publication :

```bash
-p 8000:8000
```

---

# 42. Tester depuis Python

## Guide pratique

Le support annonce aussi des requêtes HTTP via Python.

Pattern standard-library :

```python
from urllib.request import (
    urlopen,
)


with urlopen(
    "http://localhost:8000/health"
) as response:
    print(
        response.status
    )
    print(
        response.read()
    )
```

---

# 43. Client Python POST

```python
import json

from urllib.request import (
    Request,
    urlopen,
)


payload = {
    "value": 42
}


request = Request(
    "http://localhost:8000/predict",
    data=json.dumps(
        payload
    ).encode(),
    headers={
        "Content-Type":
        "application/json"
    },
    method="POST",
)


with urlopen(
    request
) as response:
    print(
        response.read()
    )
```

---

# 44. Pytest + FastAPI

Le support annonce :

```text
Pytest
```

et :

```text
FastAPI
```

Un pattern cohérent de practice consiste à les relier.

---

# 45. Test d’un endpoint

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


def test_health():
    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )
```

> `TestClient` n’est pas cité dans la page source ; il est utilisé ici uniquement comme support de pratique.

---

# 46. Test du body

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

# 47. Test POST

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

# 48. Test de validation

```python
def test_predict_invalid_payload():
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

# 49. Test d’erreur métier

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

# 50. Chaîne complète de validation

```text
FastAPI
↓
curl
↓
Pytest
↓
Docker
↓
Prometheus metrics
```

---

# 51. Debug FastAPI — checklist

```text
process lancé ?
module correct ?
objet app correct ?
host correct ?
port correct ?
route correcte ?
payload valide ?
```

---

# 52. Erreur — connexion refusée

Symptôme :

```text
connection refused
```

Vérifier :

```text
serveur démarré ?
bon port ?
bon host ?
container actif ?
```

---

# 53. Erreur — 404

Signifie généralement :

```text
route absente
ou
URL incorrecte
```

---

# 54. Erreur — validation

Vérifier :

```text
noms des champs
types Pydantic
JSON
Content-Type
```

---

# 55. Erreur — modèle introuvable

Vérifier :

```text
MODEL_PATH
pwd
volume Docker
fichier joblib
```

---

# 56. Erreur — métriques absentes

Vérifier :

```text
Instrumentator importé ?
instrument(app) appelé ?
expose(app) appelé ?
/metrics accessible ?
```

---

# 57. Mini-lab 1 — Hello FastAPI

Créer :

```text
GET /
```

Retour :

```json
{
  "message": "Bloc 3"
}
```

Tester avec :

```bash
curl
```

---

# 58. Mini-lab 2 — Health

Ajouter :

```text
GET /health
```

et tester :

```bash
curl -i
```

---

# 59. Mini-lab 3 — Pydantic

Créer :

```python
class Item(BaseModel):
    value: float
```

Puis :

```text
POST /items
```

---

# 60. Mini-lab 4 — erreur de validation

Tester :

```json
{
  "value": "abc"
}
```

Observer le comportement.

---

# 61. Mini-lab 5 — variable d’environnement

Créer :

```bash
export APP_MODE=exam
```

Puis un endpoint :

```text
GET /config
```

qui retourne :

```text
APP_MODE
```

---

# 62. Mini-lab 6 — joblib

Créer un artefact simple :

```python
{
    "model_name":
    "demo"
}
```

Le sauvegarder puis le charger dans l’application.

---

# 63. Mini-lab 7 — prediction mock

Créer :

```text
POST /predict
```

qui :

```text
reçoit un BaseModel
charge ou utilise un artefact
renvoie une prediction
```

---

# 64. Mini-lab 8 — metrics

Ajouter :

```text
prometheus-fastapi-instrumentator
```

Puis :

```bash
curl \
  http://localhost:8000/metrics
```

---

# 65. Mini-lab 9 — Docker

Containeriser l’application.

Objectif :

```text
docker build
↓
docker run
↓
curl /health
↓
curl /metrics
```

---

# 66. Mini-lab 10 — CI

Dans GitLab CI :

```text
pytest
↓
docker build
```

Objectif :

```text
pipeline vert
```

---

# 67. Checklist de maîtrise

```text
[ ] créer FastAPI()
[ ] créer GET
[ ] créer POST
[ ] définir BaseModel
[ ] lire payload
[ ] tester avec curl
[ ] charger joblib
[ ] lire env var
[ ] exposer /metrics
[ ] containeriser
[ ] tester avec Pytest
```

---

# 68. Questions flash

1. Quel framework API est explicitement annoncé ?
2. Quelle classe Pydantic est explicitement annoncée ?
3. Quel rôle joue `BaseModel` ?
4. Comment créer un endpoint GET ?
5. Comment créer un endpoint POST ?
6. Comment tester manuellement l’API ?
7. Quel outil permet d’exposer les métriques FastAPI dans le support ?
8. Comment relier `joblib` et FastAPI ?
9. Pourquoi utiliser des env vars pour `MODEL_PATH` ?
10. Quelle chaîne relie FastAPI à Prometheus ?

---

# 69. Réponses flash

```text
1. FastAPI.
2. pydantic.BaseModel.
3. définir / valider les données structurées.
4. @app.get(...).
5. @app.post(...).
6. curl.
7. prometheus-fastapi-instrumentator.
8. joblib.load au démarrage / avant usage.
9. séparer configuration et code.
10. FastAPI → instrumentator → /metrics → Prometheus.
```

---

# 70. Cheatsheet 30 secondes

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Payload(BaseModel):
    value: float


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/predict")
def predict(
    payload: Payload,
):
    return {
        "prediction": 0
    }
```

Test :

```bash
curl \
  http://localhost:8000/health
```

POST :

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 1}' \
  http://localhost:8000/predict
```

---

# 71. Fil rouge à retenir

```text
HTTP REQUEST
    ↓
FASTAPI
    ↓
PYDANTIC
    ↓
PYTHON LOGIC
    ↓
RESPONSE
    ↓
METRICS
```

---

# 72. Document suivant

```text
07_RNCP_38919_BLOC_3_PYTEST_TESTING_GUIDE.md
```

Objectif :

> approfondir Pytest dans le contexte du Bloc 3 :
> tests unitaires, API, erreurs, intégration CI GitLab et stratégie de validation rapide.
