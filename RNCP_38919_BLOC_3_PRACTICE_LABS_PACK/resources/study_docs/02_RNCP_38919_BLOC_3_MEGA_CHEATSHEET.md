# 02 — RNCP 38919 — Bloc 3
# Mega Cheatsheet

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures  
**Difficulté annoncée :** Difficile

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Source** = notion explicitement annoncée dans le support DataScientest.
> - **Cheatsheet** = commandes, snippets et patterns proposés pour les révisions.
>
> Le support officiel annonce les domaines ci-dessous mais ne fournit pas toujours les syntaxes exactes.
> Les commandes et YAML de ce document servent donc de **mémo pratique**, pas de consigne officielle supplémentaire.

---

# 1. Vue d’ensemble

```text
BASH / ENV
   ↓
PYTHON / HTTP
   ↓
FASTAPI / PYDANTIC
   ↓
PYTEST
   ↓
GITLAB CI
   ↓
RUNNER
   ↓
DOCKER
   ↓
DOCKERHUB
   ↓
KUBERNETES
   ↓
PROMETHEUS
   ↓
PROMQL
   ↓
GRAFANA
```

---

# 2. Format examen

```text
Durée        : 4 h
Surveillance : Mereos
Navigateur   : Google Chrome
Rendu        : archive uploadée sur la page du sujet
```

---

# 3. Préparation GitLab

## Source

Le repository privé demandé avant l’examen est :

```text
dst_rncp38919_bloc_3
```

Le Runner demandé :

```text
type : shell
nom  : shell
```

---

# 4. Bash — variables d’environnement

Définir :

```bash
export API_URL=http://localhost:8000
```

Lire :

```bash
echo $API_URL
```

Persistant :

```bash
echo 'export API_URL=http://localhost:8000' >> ~/.bashrc
```

Recharger :

```bash
source ~/.bashrc
```

---

# 5. Python — variables d’environnement

```python
import os

api_url = os.getenv("API_URL")
```

Avec valeur par défaut :

```python
api_url = os.getenv(
    "API_URL",
    "http://localhost:8000",
)
```

---

# 6. Python — environnement virtuel

Créer :

```bash
python -m venv .venv
```

Activer :

```bash
source .venv/bin/activate
```

Désactiver :

```bash
deactivate
```

---

# 7. HTTP avec `curl`

GET :

```bash
curl http://localhost:8000/
```

Avec headers :

```bash
curl \
  -H "Accept: application/json" \
  http://localhost:8000/
```

POST JSON :

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 42}' \
  http://localhost:8000/predict
```

---

# 8. HTTP en Python

Le support annonce les requêtes HTTP en Python mais ne fixe pas la bibliothèque.

Pattern général :

```python
response = ...
status_code = ...
payload = ...
```

Si vous utilisez une librairie pendant vos entraînements, gardez toujours en tête :

```text
URL
method
headers
body
status
response
```

---

# 9. `joblib`

Sauvegarder :

```python
import joblib

joblib.dump(
    model,
    "model.joblib",
)
```

Charger :

```python
model = joblib.load(
    "model.joblib"
)
```

---

# 10. Git — commandes utiles

```bash
git status
git add .
git commit -m "message"
git push
git pull
```

Clone SSH :

```bash
git clone git@gitlab.com:USER/REPO.git
```

---

# 11. GitLab CI — structure mentale

```text
.gitlab-ci.yml
   ↓
stages
   ↓
jobs
   ↓
runner
   ↓
script
```

---

# 12. `.gitlab-ci.yml` minimal

```yaml
stages:
  - test
  - build

test:
  stage: test
  script:
    - pytest -v

build:
  stage: build
  script:
    - docker build -t my-app .
```

> Exemple de révision, non imposé par le support.

---

# 13. GitLab CI — variables utiles

Pattern :

```yaml
variables:
  APP_ENV: "test"
```

Dans un job :

```yaml
script:
  - echo "$APP_ENV"
```

---

# 14. GitLab Runner

Vérifier :

```bash
gitlab-runner --version
```

Lister :

```bash
gitlab-runner list
```

Concept :

```text
GitLab
→ pipeline
→ runner
→ shell
→ commandes
```

---

# 15. Docker — build

```bash
docker build \
  -t my-app:latest \
  .
```

---

# 16. Docker — run

```bash
docker run \
  --rm \
  -p 8000:8000 \
  my-app:latest
```

---

# 17. Docker — inspecter

```bash
docker ps
docker ps -a
docker images
docker logs <container>
docker logs -f <container>
```

---

# 18. Docker — supprimer

```bash
docker stop <container>
docker rm <container>
docker rmi <image>
```

---

# 19. Dockerfile — squelette

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

---

# 20. Dockerfile FastAPI

Pattern de révision :

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
  "app:app",
  "--host",
  "0.0.0.0",
  "--port",
  "8000"
]
```

---

# 21. Docker volumes

Volume nommé :

```yaml
volumes:
  - app_data:/data
```

Bind mount :

```yaml
volumes:
  - ./data:/data
```

---

# 22. Docker Compose — commandes

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose logs -f
docker compose down
```

Rebuild :

```bash
docker compose up -d --build
```

---

# 23. Docker Compose — squelette

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"

  prometheus:
    image: prom/prometheus
    depends_on:
      - app
```

---

# 24. `depends_on`

Source explicitement annoncée :

```text
services.depends_on
```

Pattern :

```yaml
services:
  app:
    depends_on:
      - db
```

À retenir :

```text
depends_on
=
dépendance logique de démarrage
```

---

# 25. DockerHub — login

```bash
docker login
```

Avec token :

```text
username
+
Personal Access Token
```

---

# 26. DockerHub — tag

```bash
docker tag \
  my-app:latest \
  USER/my-app:latest
```

---

# 27. DockerHub — push

```bash
docker push \
  USER/my-app:latest
```

---

# 28. Pytest

Lancer :

```bash
pytest
```

Verbeux :

```bash
pytest -v
```

Un fichier :

```bash
pytest tests/test_api.py
```

Un test :

```bash
pytest \
  tests/test_api.py::test_health
```

---

# 29. Pytest — structure

```text
tests/
├── test_api.py
├── test_model.py
└── test_utils.py
```

Convention :

```text
test_*.py
test_*
```

---

# 30. Pytest — assertion

```python
def test_value():
    assert 2 + 2 == 4
```

---

# 31. Pytest — exception

```python
import pytest

with pytest.raises(
    ValueError
):
    ...
```

---

# 32. FastAPI minimal

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

# 33. FastAPI — run

Pattern de révision :

```bash
uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000
```

---

# 34. Pydantic `BaseModel`

```python
from pydantic import BaseModel


class PredictionRequest(
    BaseModel
):
    value: float
```

---

# 35. FastAPI POST

```python
@app.post("/predict")
def predict(
    payload: PredictionRequest,
):
    return {
        "prediction": 0,
        "input": payload.value,
    }
```

---

# 36. FastAPI health endpoint

```python
@app.get("/health")
def health():
    return {
        "status": "ok"
    }
```

---

# 37. FastAPI — TestClient

Cheatsheet de révision :

```python
from fastapi.testclient import (
    TestClient,
)

from app import app


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

> `TestClient` n’est pas cité dans la page source, mais c’est un pattern de pratique utile pour relier FastAPI et Pytest.

---

# 38. Prometheus FastAPI Instrumentator

Pattern de révision :

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

Modèle :

```text
FastAPI
→ /metrics
→ Prometheus
```

---

# 39. Kubernetes — commandes de base

```bash
kubectl apply -f file.yml
kubectl get pods
kubectl get services
kubectl get deployments
kubectl get namespaces
kubectl get pv
kubectl get pvc
kubectl get configmaps
```

---

# 40. Kubernetes — debug

```bash
kubectl describe pod <pod>
kubectl logs <pod>
kubectl logs -f <pod>
```

---

# 41. Namespace YAML

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: rncp-bloc3
```

---

# 42. ConfigMap YAML

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
```

---

# 43. Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
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
          image: USER/my-app:latest
          ports:
            - containerPort: 8000
```

---

# 44. Service YAML

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
    - port: 8000
      targetPort: 8000
```

---

# 45. PV YAML

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
```

> Squelette pédagogique ; le support annonce les PV mais ne fixe pas leur backend exact.

---

# 46. PVC YAML

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

---

# 47. PV / PVC — relation mentale

```text
Pod
 ↓
PVC
 ↓
PV
```

---

# 48. Deployment / Service

```text
Deployment
   ↓
Pods
   ↓
Service
   ↓
Client
```

---

# 49. Selector / Labels

À vérifier toujours :

```text
Deployment selector
=
Pod labels
=
Service selector
```

Exemple :

```yaml
labels:
  app: api
```

---

# 50. Kubernetes — namespace ciblé

```bash
kubectl get pods \
  -n rncp-bloc3
```

Appliquer :

```bash
kubectl apply \
  -f deployment.yml \
  -n rncp-bloc3
```

---

# 51. Prometheus — config minimale

Source annoncée :

```text
config/prometheus.yml
```

Pattern :

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

# 52. Prometheus — modèle mental

```text
target
 ↓
/metrics
 ↓
Prometheus scrape
 ↓
time series
 ↓
PromQL
```

---

# 53. PromQL — métrique simple

Pattern générique :

```promql
metric_name
```

---

# 54. PromQL — filtre label

```promql
metric_name{
  label="value"
}
```

---

# 55. PromQL — `rate`

Pattern :

```promql
rate(
  metric_name[5m]
)
```

---

# 56. PromQL — agrégation

```promql
sum(
  metric_name
)
```

ou :

```promql
sum by (label) (
  metric_name
)
```

> Ces snippets sont des exemples de révision. La page source annonce PromQL sans fournir de requêtes précises.

---

# 57. Prometheus — debug

Vérifier :

```text
target accessible ?
port correct ?
/metrics existe ?
prometheus.yml correct ?
target UP ?
```

---

# 58. Grafana datasource YAML

Source annoncée :

```text
datasources/<source_name>.yml
```

Pattern :

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

# 59. Grafana — modèle mental

```text
Prometheus
   ↓
Datasource
   ↓
Panel
   ↓
Dashboard
```

---

# 60. Grafana — debug

```text
datasource existe ?
URL correcte ?
Save & Test OK ?
requête PromQL retourne des données ?
panel utilise la bonne métrique ?
```

---

# 61. Architecture end-to-end

```text
Git Push
   ↓
GitLab
   ↓
.gitlab-ci.yml
   ↓
Runner shell
   ↓
pytest
   ↓
docker build
   ↓
docker push
   ↓
DockerHub
   ↓
Kubernetes Deployment
   ↓
Service
   ↓
FastAPI
   ↓
/metrics
   ↓
Prometheus
   ↓
PromQL
   ↓
Grafana
```

---

# 62. Pipeline GitLab de révision

```yaml
stages:
  - test
  - build
  - push

test:
  stage: test
  script:
    - pytest -v

build:
  stage: build
  script:
    - docker build -t my-app .

push:
  stage: push
  script:
    - docker tag my-app USER/my-app:latest
    - docker push USER/my-app:latest
```

> Squelette de pratique, non imposé par le support.

---

# 63. FastAPI + metrics — mini app

```python
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import (
    Instrumentator,
)


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


Instrumentator().instrument(
    app
).expose(
    app
)
```

---

# 64. Docker Compose — app + Prometheus + Grafana

Pattern de révision :

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"

  prometheus:
    image: prom/prometheus
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    depends_on:
      - app

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

---

# 65. Ports courants de pratique

```text
FastAPI     8000
Prometheus  9090
Grafana     3000
```

> Ces ports sont des conventions fréquentes de pratique, pas des valeurs imposées dans le support.

---

# 66. Debug — FastAPI

```text
process running ?
port correct ?
endpoint correct ?
payload Pydantic valide ?
curl correct ?
```

---

# 67. Debug — GitLab CI

```text
.gitlab-ci.yml valide ?
pipeline créé ?
runner online ?
job pending ?
logs du job ?
variables présentes ?
```

---

# 68. Debug — Docker

```text
image build ?
container running ?
port publié ?
logs ?
volume ?
network ?
```

---

# 69. Debug — Kubernetes

```text
namespace ?
deployment ?
pod ?
service ?
selector ?
image ?
configmap ?
pvc ?
logs ?
```

---

# 70. Debug — Prometheus

```text
/metrics ?
target UP ?
hostname ?
port ?
scrape config ?
PromQL ?
```

---

# 71. Debug — Grafana

```text
datasource ?
URL ?
Prometheus joignable ?
requête valide ?
dashboard ?
```

---

# 72. Les fichiers à savoir produire

```text
.gitlab-ci.yml
Dockerfile
docker-compose.yml

namespace.yml
configmap.yml
deployment.yml
service.yml
pv.yml
pvc.yml

config/prometheus.yml
datasources/prometheus.yml
```

---

# 73. Les commandes à savoir sans hésiter

```bash
export VAR=value
source ~/.bashrc

python -m venv .venv
source .venv/bin/activate

curl URL

pytest -v

docker build ...
docker run ...
docker compose up -d
docker compose ps
docker compose logs

docker login
docker push ...

kubectl apply -f ...
kubectl get pods
kubectl describe pod ...
kubectl logs ...

gitlab-runner list
```

---

# 74. Réflexe 30 secondes

```text
ENV
→ API
→ TEST
→ CI
→ BUILD
→ PUSH
→ DEPLOY
→ EXPOSE
→ SCRAPE
→ DASHBOARD
```

---

# 75. Pièges YAML

Toujours vérifier :

```text
indentation
:
-
noms des clés
selector / labels
service names
paths
ports
```

---

# 76. Pièges variables d’environnement

```text
variable non exportée
.bashrc non rechargé
mauvais nom de variable
variable absente du runner
variable absente du container
ConfigMap non injectée
```

---

# 77. Pièges DockerHub

```text
tag absent
mauvais repository
login non effectué
token invalide
push non autorisé
```

---

# 78. Pièges Kubernetes

```text
image inaccessible
selector incorrect
namespace incorrect
PVC Pending
Pod CrashLoopBackOff
Service sans endpoints
```

---

# 79. Pièges monitoring

```text
app ne publie pas /metrics
Prometheus cible localhost au lieu du service
mauvais hostname
mauvais port
Grafana pointe vers mauvaise URL
```

---

# 80. Checklist examen

```text
[ ] repo GitLab prêt
[ ] SSH prêt
[ ] Runner shell prêt
[ ] DockerHub prêt
[ ] token prêt
[ ] Docker OK
[ ] Python OK
[ ] Git OK
[ ] environnement VM propre
```

---

# 81. Résumé final

```text
BASH
→ PYTHON
→ FASTAPI
→ PYTEST
→ GITLAB CI
→ RUNNER
→ DOCKER
→ DOCKERHUB
→ KUBERNETES
→ PROMETHEUS
→ GRAFANA
```

---

# 82. Document suivant

```text
03_RNCP_38919_BLOC_3_BASH_ENV_HTTP_GUIDE.md
```

Objectif :

> approfondir uniquement les fondamentaux système du Bloc 3 :
> `export`, `.bashrc`, variables d’environnement, venv, `curl`,
> requêtes HTTP en Python et `joblib`.
