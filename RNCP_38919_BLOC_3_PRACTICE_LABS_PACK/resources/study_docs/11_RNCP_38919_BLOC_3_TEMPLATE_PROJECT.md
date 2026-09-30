# 11 — RNCP 38919 — Bloc 3
# Template de projet d’entraînement

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Important**
>
> Le support DataScientest annonce les technologies et objets à maîtriser :
>
> ```text
> Bash / export / .bashrc
> variables d’environnement Python
> environnements virtuels
> HTTP Python + Bash
> joblib
> GitLab
> .gitlab-ci.yml
> GitLab Runner
> Docker
> Dockerfile
> volumes
> docker-compose.yml
> services.depends_on
> DockerHub
> Pytest
> FastAPI
> prometheus-fastapi-instrumentator
> pydantic.BaseModel
> curl
> Kubernetes
> Namespace
> PersistentVolume
> PersistentVolumeClaim
> ConfigMap
> Service
> Deployment
> Prometheus
> config/prometheus.yml
> PromQL
> Grafana
> datasources/<source_name>.yml
> dashboard via l’UI
> ```
>
> En revanche, la page source ne fournit pas une architecture de projet finale officielle.
>
> Le projet ci-dessous est donc un **template d’entraînement proposé** qui assemble proprement l’ensemble du périmètre annoncé.

---

# 1. Objectif du template

Construire un projet compact permettant de pratiquer la chaîne :

```text
Python
 ↓
FastAPI
 ↓
Pydantic
 ↓
Pytest
 ↓
GitLab CI
 ↓
Docker
 ↓
DockerHub
 ↓
Kubernetes
 ↓
Prometheus
 ↓
Grafana
```

avec :

```text
joblib
variables d’environnement
curl
volumes
ConfigMap
PV / PVC
```

---

# 2. Nom du repository GitLab

## Attendu source

Le repository privé demandé avant l’examen est :

```text
dst_rncp38919_bloc_3
```

Le template reprend donc ce nom.

---

# 3. Arborescence proposée

```text
dst_rncp38919_bloc_3/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   └── model.py
│
├── models/
│   └── model.joblib
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_config.py
│   └── test_model.py
│
├── scripts/
│   ├── create_artifact.py
│   ├── http_client.py
│   └── smoke_test.sh
│
├── config/
│   └── prometheus.yml
│
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── prometheus.yml
│
├── k8s/
│   ├── namespace.yml
│   ├── configmap.yml
│   ├── pv.yml
│   ├── pvc.yml
│   ├── deployment.yml
│   └── service.yml
│
├── .env.example
├── .gitignore
├── .dockerignore
├── .gitlab-ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── START_HERE.md
```

---

# 4. Vue architecture

```text
                    GitLab
                      │
                      ▼
               .gitlab-ci.yml
                      │
                      ▼
                Runner shell
                      │
         ┌────────────┴─────────────┐
         │                          │
         ▼                          ▼
      Pytest                    Docker build
                                    │
                                    ▼
                               DockerHub
                                    │
                                    ▼
                              Kubernetes
                                    │
                  ┌─────────────────┼────────────────┐
                  │                 │                │
                  ▼                 ▼                ▼
               ConfigMap        Deployment         PVC
                                    │                │
                                    ▼                ▼
                                  Pods              PV
                                    │
                                    ▼
                                  Service
                                    │
                                    ▼
                                  FastAPI
                                    │
                           ┌────────┴────────┐
                           │                 │
                           ▼                 ▼
                       /predict           /metrics
                                             │
                                             ▼
                                         Prometheus
                                             │
                                             ▼
                                           Grafana
```

---

# 5. `requirements.txt`

## Template proposé

```text
fastapi
uvicorn
pydantic
joblib
pytest
prometheus-fastapi-instrumentator
```

Le support ne fournit pas de fichier `requirements.txt` officiel ; cette liste correspond uniquement aux outils Python explicitement annoncés ou nécessaires au template de practice.

---

# 6. `.env.example`

```env
APP_ENV=development
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=models/model.joblib
```

---

# 7. `app/config.py`

```python
import os


APP_ENV = os.getenv(
    "APP_ENV",
    "development",
)

API_HOST = os.getenv(
    "API_HOST",
    "0.0.0.0",
)

API_PORT = int(
    os.getenv(
        "API_PORT",
        "8000",
    )
)

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/model.joblib",
)
```

---

# 8. Objectif de `config.py`

Centraliser :

```text
APP_ENV
API_HOST
API_PORT
MODEL_PATH
```

Chaîne :

```text
Shell
→ env vars
→ config.py
→ application
```

---

# 9. `app/schemas.py`

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

# 10. `app/model.py`

```python
from pathlib import Path

import joblib


def load_artifact(
    path: str,
):
    model_path = Path(
        path
    )

    if not model_path.exists():
        raise FileNotFoundError(
            model_path
        )

    return joblib.load(
        model_path
    )
```

---

# 11. Artefact `joblib`

Pour ne pas dépendre d’un entraînement ML lourd dans le lab, créer un objet simple sérialisable.

`scripts/create_artifact.py` :

```python
from pathlib import Path

import joblib


artifact = {
    "name": "rncp-bloc3-demo",
    "version": 1,
}


Path(
    "models"
).mkdir(
    parents=True,
    exist_ok=True,
)


joblib.dump(
    artifact,
    "models/model.joblib",
)


print(
    "Artifact created"
)
```

> Ce mock d’artefact est un support d’entraînement. Le support officiel cite `joblib`, mais n’impose pas un modèle précis.

---

# 12. `app/main.py`

```python
from fastapi import (
    FastAPI,
)

from prometheus_fastapi_instrumentator import (
    Instrumentator,
)

from app.config import (
    APP_ENV,
)

from app.schemas import (
    PredictionRequest,
    PredictionResponse,
)


app = FastAPI()


@app.get("/")
def root():
    return {
        "name":
        "RNCP 38919 Bloc 3",
        "env":
        APP_ENV,
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    payload: PredictionRequest,
):
    prediction = int(
        payload.value >= 0
    )

    return PredictionResponse(
        prediction=prediction
    )


Instrumentator().instrument(
    app
).expose(
    app
)
```

---

# 13. Endpoints du template

```text
GET /
GET /health
POST /predict
GET /metrics
```

Ces endpoints sont proposés pour practice.

La source ne fournit pas une liste officielle d’endpoints à reproduire.

---

# 14. Lancer localement

```bash
python -m venv .venv
```

Puis :

```bash
source .venv/bin/activate
```

Installer :

```bash
pip install \
  -r requirements.txt
```

Lancer :

```bash
uvicorn \
  app.main:app \
  --host 0.0.0.0 \
  --port 8000
```

---

# 15. Test manuel avec `curl`

Health :

```bash
curl \
  http://localhost:8000/health
```

Prediction :

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 42}' \
  http://localhost:8000/predict
```

Metrics :

```bash
curl \
  http://localhost:8000/metrics
```

---

# 16. `scripts/http_client.py`

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
    ).encode(
        "utf-8"
    ),
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
        response.status
    )

    print(
        response.read()
    )
```

---

# 17. `scripts/smoke_test.sh`

```bash
#!/usr/bin/env bash

set -e

echo "Health:"
curl -f \
  http://localhost:8000/health

echo

echo "Prediction:"
curl -f \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 42}' \
  http://localhost:8000/predict

echo

echo "Metrics:"
curl -f \
  http://localhost:8000/metrics \
  > /dev/null

echo
echo "Smoke tests OK"
```

---

# 18. `tests/test_api.py`

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

    assert response.json() == {
        "status": "ok"
    }


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

    assert (
        "prediction"
        in response.json()
    )


def test_invalid_payload():
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


def test_metrics():
    response = client.get(
        "/metrics"
    )

    assert (
        response.status_code
        == 200
    )
```

---

# 19. `tests/test_config.py`

```python
import os


def test_environment_access():
    value = os.getenv(
        "APP_ENV",
        "development",
    )

    assert isinstance(
        value,
        str,
    )
```

---

# 20. `tests/test_model.py`

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

# 21. Lancer Pytest

```bash
pytest -v
```

---

# 22. `Dockerfile`

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

# 23. `.dockerignore`

```text
.venv/
.git/
__pycache__/
.pytest_cache/
*.pyc
```

---

# 24. Build Docker

```bash
docker build \
  -t rncp-bloc3:latest \
  .
```

---

# 25. Run Docker

```bash
docker run \
  --rm \
  -p 8000:8000 \
  rncp-bloc3:latest
```

---

# 26. `config/prometheus.yml`

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: fastapi

    static_configs:
      - targets:
          - app:8000
```

---

# 27. `grafana/provisioning/datasources/prometheus.yml`

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

---

# 28. `docker-compose.yml`

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      APP_ENV: docker
      MODEL_PATH: /models/model.joblib
    volumes:
      - app_models:/models

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
    depends_on:
      - app

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
    depends_on:
      - prometheus

volumes:
  app_models:
```

---

# 29. Démarrer la stack Compose

```bash
docker compose up \
  -d \
  --build
```

---

# 30. Vérifier Compose

```bash
docker compose ps
```

Logs :

```bash
docker compose logs
```

---

# 31. Validation Compose

Tester :

```bash
curl \
  http://localhost:8000/health
```

Puis :

```bash
curl \
  http://localhost:8000/metrics
```

Puis vérifier :

```text
Prometheus
→ target UP
```

Puis :

```text
Grafana
→ datasource Prometheus
```

---

# 32. DockerHub

## Attendu source

Avant l’examen :

```text
compte DockerHub
+
Personal Access Token
```

## Guide pratique

Tag :

```bash
docker tag \
  rncp-bloc3:latest \
  USER/rncp-bloc3:latest
```

Login :

```bash
docker login
```

Push :

```bash
docker push \
  USER/rncp-bloc3:latest
```

---

# 33. `.gitlab-ci.yml`

## Template proposé

```yaml
stages:
  - test
  - build

tests:
  stage: test
  script:
    - python --version
    - python -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt
    - pytest -v

docker_build:
  stage: build
  script:
    - docker build -t rncp-bloc3:latest .
```

---

# 34. Version avec DockerHub

Pattern avancé de practice :

```yaml
stages:
  - test
  - build
  - push

tests:
  stage: test
  script:
    - python -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt
    - pytest -v

build:
  stage: build
  script:
    - docker build -t rncp-bloc3 .

push:
  stage: push
  script:
    - echo "$DOCKERHUB_TOKEN" |
      docker login
      -u "$DOCKERHUB_USER"
      --password-stdin

    - docker tag
      rncp-bloc3
      "$DOCKERHUB_USER/rncp-bloc3:latest"

    - docker push
      "$DOCKERHUB_USER/rncp-bloc3:latest"
```

> Ce pipeline est proposé pour l’entraînement ; le support ne fixe pas ces stages.

---

# 35. Runner GitLab

## Attendu source

Runner demandé :

```text
type : shell
nom  : shell
```

Vérifier :

```bash
gitlab-runner list
```

---

# 36. `k8s/namespace.yml`

```yaml
apiVersion: v1
kind: Namespace

metadata:
  name: rncp-bloc3
```

---

# 37. `k8s/configmap.yml`

```yaml
apiVersion: v1
kind: ConfigMap

metadata:
  name: api-config
  namespace: rncp-bloc3

data:
  APP_ENV: kubernetes
  MODEL_PATH: /models/model.joblib
```

---

# 38. `k8s/pv.yml`

```yaml
apiVersion: v1
kind: PersistentVolume

metadata:
  name: model-pv

spec:
  capacity:
    storage: 1Gi

  accessModes:
    - ReadWriteOnce

  hostPath:
    path: /tmp/rncp-models
```

> `hostPath` sert uniquement de backend de lab dans cet exemple ; la source n’impose pas ce choix.

---

# 39. `k8s/pvc.yml`

```yaml
apiVersion: v1
kind: PersistentVolumeClaim

metadata:
  name: model-pvc
  namespace: rncp-bloc3

spec:
  accessModes:
    - ReadWriteOnce

  resources:
    requests:
      storage: 1Gi
```

---

# 40. `k8s/deployment.yml`

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: api
  namespace: rncp-bloc3

spec:
  replicas: 1

  selector:
    matchLabels:
      app: api

  template:
    metadata:
      labels:
        app: api

    spec:
      containers:
        - name: api
          image: USER/rncp-bloc3:latest

          ports:
            - containerPort: 8000

          envFrom:
            - configMapRef:
                name: api-config

          volumeMounts:
            - name: model-storage
              mountPath: /models

      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: model-pvc
```

---

# 41. `k8s/service.yml`

```yaml
apiVersion: v1
kind: Service

metadata:
  name: api-service
  namespace: rncp-bloc3

spec:
  selector:
    app: api

  ports:
    - port: 8000
      targetPort: 8000
```

---

# 42. Appliquer Kubernetes

```bash
kubectl apply \
  -f k8s/
```

---

# 43. Vérifier Kubernetes

```bash
kubectl get pods \
  -n rncp-bloc3
```

```bash
kubectl get services \
  -n rncp-bloc3
```

```bash
kubectl get pvc \
  -n rncp-bloc3
```

```bash
kubectl get pv
```

---

# 44. Debug Kubernetes

```bash
kubectl describe pod \
  <pod> \
  -n rncp-bloc3
```

```bash
kubectl logs \
  <pod> \
  -n rncp-bloc3
```

---

# 45. Test via port-forward

```bash
kubectl port-forward \
  service/api-service \
  8000:8000 \
  -n rncp-bloc3
```

Puis :

```bash
curl \
  http://localhost:8000/health
```

---

# 46. `START_HERE.md`

Contenu proposé :

```markdown
# START HERE

1. Vérifier les prérequis
2. Créer le venv
3. Installer requirements.txt
4. Lancer pytest
5. Lancer FastAPI
6. Tester curl
7. Construire Docker
8. Lancer Compose
9. Vérifier Prometheus
10. Configurer / vérifier Grafana
11. Lancer GitLab CI
12. Déployer Kubernetes
```

---

# 47. `README.md`

Le README de practice devrait contenir :

```text
objectif
architecture
prérequis
installation
run local
tests
Docker
Compose
GitLab CI
DockerHub
Kubernetes
Prometheus
Grafana
troubleshooting
```

---

# 48. Ordre d’exécution local

```text
1. venv
2. pip install
3. create artifact
4. pytest
5. FastAPI
6. curl
7. docker build
8. docker compose
9. Prometheus
10. Grafana
```

---

# 49. Ordre d’exécution CI/CD

```text
git push
↓
GitLab
↓
Runner shell
↓
pytest
↓
docker build
↓
DockerHub
```

---

# 50. Ordre de déploiement Kubernetes

```text
Namespace
↓
ConfigMap
↓
PV
↓
PVC
↓
Deployment
↓
Service
```

---

# 51. Ordre de validation observabilité

```text
FastAPI
↓
/metrics
↓
Prometheus target UP
↓
PromQL
↓
Grafana datasource
↓
Dashboard
```

---

# 52. Commandes de validation rapide

## Local

```bash
pytest -v
```

```bash
curl \
  http://localhost:8000/health
```

## Docker

```bash
docker ps
```

```bash
docker logs \
  <container>
```

## Compose

```bash
docker compose ps
```

```bash
docker compose logs
```

## Kubernetes

```bash
kubectl get pods \
  -n rncp-bloc3
```

## GitLab Runner

```bash
gitlab-runner list
```

---

# 53. Matrice fichiers / compétences

| Fichier | Compétence |
|---|---|
| `app/config.py` | env vars Python |
| `app/schemas.py` | Pydantic |
| `app/main.py` | FastAPI |
| `scripts/http_client.py` | HTTP Python |
| `scripts/smoke_test.sh` | Bash + curl |
| `tests/*` | Pytest |
| `.gitlab-ci.yml` | GitLab CI |
| `Dockerfile` | Docker |
| `docker-compose.yml` | Compose / depends_on / volumes |
| `config/prometheus.yml` | Prometheus |
| `grafana/.../prometheus.yml` | Grafana datasource |
| `k8s/namespace.yml` | Namespace |
| `k8s/configmap.yml` | ConfigMap |
| `k8s/pv.yml` | PV |
| `k8s/pvc.yml` | PVC |
| `k8s/deployment.yml` | Deployment |
| `k8s/service.yml` | Service |

---

# 54. Ce que ce template permet de pratiquer

```text
[ ] export / env vars
[ ] Python env access
[ ] venv
[ ] HTTP Python
[ ] curl
[ ] joblib
[ ] GitLab repo
[ ] .gitlab-ci.yml
[ ] Runner shell
[ ] Dockerfile
[ ] Docker volume
[ ] docker-compose.yml
[ ] depends_on
[ ] DockerHub
[ ] Pytest
[ ] FastAPI
[ ] BaseModel
[ ] metrics
[ ] Namespace
[ ] PV
[ ] PVC
[ ] ConfigMap
[ ] Service
[ ] Deployment
[ ] Prometheus
[ ] PromQL
[ ] Grafana datasource
[ ] Grafana dashboard
```

---

# 55. Ce que ce template n’est pas

Ce n’est pas :

```text
le sujet officiel
```

ni :

```text
une correction officielle
```

ni :

```text
une architecture imposée par DataScientest
```

Il s’agit d’un :

```text
template de practice
```

construit à partir du périmètre source.

---

# 56. Première qualification proposée

Le projet est considéré comme fonctionnel quand :

```text
pytest -v
→ PASS

curl /health
→ 200

curl /predict
→ réponse JSON

curl /metrics
→ métriques

docker build
→ OK

docker compose up
→ OK

Prometheus
→ target UP

Grafana
→ datasource OK

GitLab pipeline
→ green

Kubernetes Pods
→ Running

Kubernetes Service
→ API joignable
```

---

# 57. Test end-to-end proposé

```text
git push
↓
pipeline vert
↓
image créée
↓
image disponible
↓
Deployment Kubernetes
↓
Service
↓
curl /health
↓
Prometheus
↓
Grafana
```

---

# 58. Pannes à simuler

Pour transformer le template en vrai lab :

```text
1. mauvais port
2. env var absente
3. test Pytest cassé
4. Runner offline
5. Dockerfile incorrect
6. target Prometheus incorrecte
7. datasource Grafana incorrecte
8. Deployment image invalide
9. Service selector incorrect
10. PVC Pending
```

---

# 59. Objectif final de maîtrise

Être capable de reconstruire de mémoire :

```text
FastAPI
+
Pydantic
+
Pytest
+
Docker
+
GitLab CI
+
Kubernetes
+
Prometheus
+
Grafana
```

dans une architecture minimale mais fonctionnelle.

---

# 60. Résumé architecture

```text
              ┌───────────────┐
              │     GitLab    │
              └───────┬───────┘
                      │
                Runner shell
                      │
          ┌───────────┴───────────┐
          │                       │
        Pytest               Docker build
                                  │
                                  ▼
                             DockerHub
                                  │
                                  ▼
                              Deployment
                                  │
                                  ▼
                                 Pod
                         ┌────────┼─────────┐
                         │        │         │
                         ▼        ▼         ▼
                     ConfigMap   PVC      Service
                                 │          │
                                 ▼          ▼
                                 PV       FastAPI
                                            │
                                            ▼
                                         /metrics
                                            │
                                            ▼
                                        Prometheus
                                            │
                                            ▼
                                          Grafana
```

---

# 61. Document suivant

```text
12_RNCP_38919_BLOC_3_STRATEGIE_EXAMEN_4H.md
```

Objectif :

> transformer ce périmètre technique en stratégie d’exécution
> minute par minute pour une épreuve de 4 heures :
> cadrage, priorisation, checkpoints, validation, debug,
> archive et upload final.
