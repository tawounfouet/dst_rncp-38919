# 15 — RNCP 38919 — Bloc 3
# Corrigé proposé — Examen blanc 01

**Type :** correction proposée d’un sujet blanc  
**Certification visée :** RNCP 38919 — Data Engineer  
**Bloc :** Bloc 3  
**Durée de simulation :** 4 heures  
**Scénario fictif :** ParcelPulse

**Documents de référence :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`
- `14_RNCP_38919_BLOC_3_EXAMEN_BLANC_01.md`

> **Important**
>
> Ce document est une **correction proposée de l’examen blanc**. Il ne s’agit ni d’une correction officielle DataScientest, ni du contenu réel de l’examen RNCP, ni d’un barème officiel.
>
> Les technologies couvertes proviennent du périmètre annoncé dans le support DataScientest. Le scénario ParcelPulse, l’architecture, les endpoints, les manifests et les commandes ci-dessous sont des éléments d’entraînement proposés.

---

# 1. Objectif de la correction

Construire une implémentation de référence reliant :

```text
Bash / env vars
        ↓
Python
        ↓
FastAPI + Pydantic
        ↓
joblib
        ↓
Pytest
        ↓
GitLab CI + Runner shell
        ↓
Docker + DockerHub
        ↓
Kubernetes
        ↓
Prometheus + PromQL
        ↓
Grafana
```

---

# 2. Arborescence de référence

```text
dst_rncp38919_bloc_3/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── demo_model.py
│   ├── schemas.py
│   ├── model.py
│   └── main.py
│
├── models/
│   └── model.joblib
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
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
└── README.md
```

---

# 3. Partie A — Lecture du notebook

Le notebook de bootstrap donnait :

```text
APP_NAME      = parcelpulse-api
DEFAULT_PORT  = 8000
MODEL_PATH    = models/model.joblib
NAMESPACE     = parcelpulse
```

À reporter dans le README :

```markdown
## Bootstrap configuration

- APP_NAME: parcelpulse-api
- DEFAULT_PORT: 8000
- MODEL_PATH: models/model.joblib
- NAMESPACE: parcelpulse
```

---

# 4. Partie B — Bash et variables d’environnement

```bash
export APP_ENV=exam
export API_PORT=8000
export MODEL_PATH=models/model.joblib
```

Vérifier :

```bash
echo "$APP_ENV"
echo "$API_PORT"
echo "$MODEL_PATH"
```

Résultat attendu :

```text
exam
8000
models/model.joblib
```

Ajouter `APP_ENV` à `.bashrc` :

```bash
echo 'export APP_ENV=exam' >> ~/.bashrc
source ~/.bashrc
```

---

# 5. `app/config.py`

```python
import os

APP_NAME = os.getenv("APP_NAME", "parcelpulse-api")
APP_ENV = os.getenv("APP_ENV", "development")
API_PORT = int(os.getenv("API_PORT", "8000"))
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
```

Objectif :

```text
configuration externe
+
valeurs par défaut
+
réutilisation local / Docker / Kubernetes
```

---

# 6. Partie C — environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate
```

Installation de practice :

```bash
pip install fastapi uvicorn pydantic joblib pytest httpx prometheus-fastapi-instrumentator
```

Puis :

```bash
pip freeze > requirements.txt
```

> `httpx` est ici un choix pratique pour les tests FastAPI. Il n’est pas annoncé comme exigence dans la source.

---

# 7. `requirements.txt`

Version compacte :

```text
fastapi
uvicorn
pydantic
joblib
pytest
httpx
prometheus-fastapi-instrumentator
```

---

# 8. `app/schemas.py`

```python
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    distance_km: float
    package_weight_kg: float


class PredictionResponse(BaseModel):
    risk: int
```

---

# 9. Artefact `joblib` reproductible

Pour le practice pack, on peut générer un petit modèle pédagogique compatible avec `predict()`.

Pour éviter le problème de sérialisation lié au module `__main__` avec `pickle`/`joblib`, la classe du modèle est isolée dans `app/demo_model.py` :

```python
# app/demo_model.py
class DemoRiskModel:
    """Tiny deterministic model used only by the practice pack."""

    def predict(self, rows):
        outputs = []
        for distance_km, package_weight_kg in rows:
            score = float(distance_km) + 2 * float(package_weight_kg)
            outputs.append(int(score >= 20))
        return outputs
```

Et le script de génération `scripts/create_artifact.py` configure dynamiquement `sys.path` pour être exécutable depuis n'importe quel dossier :

```python
# scripts/create_artifact.py
import sys
from pathlib import Path

# Garantit que la racine du projet est dans sys.path quel que soit le CWD
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
from app.demo_model import DemoRiskModel

models_dir = PROJECT_ROOT / "models"
models_dir.mkdir(parents=True, exist_ok=True)
output_path = models_dir / "model.joblib"
joblib.dump(DemoRiskModel(), output_path)
print(f"Artifact created: {output_path}")
```

> Ce modèle est purement pédagogique.


---

# 10. `app/model.py`

```python
from pathlib import Path
import joblib


def load_model(path: str):
    model_path = Path(path)

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    return joblib.load(model_path)
```

---

# 11. `app/main.py`

```python
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import APP_NAME, MODEL_PATH
from app.model import load_model
from app.schemas import PredictionRequest, PredictionResponse


app = FastAPI(title=APP_NAME)
model = load_model(MODEL_PATH)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": APP_NAME,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    prediction = model.predict(
        [[payload.distance_km, payload.package_weight_kg]]
    )

    return PredictionResponse(risk=int(prediction[0]))


Instrumentator().instrument(app).expose(app)
```

---

# 12. Générer puis lancer

```bash
python scripts/create_artifact.py
```

Puis :

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

# 13. Test `GET /health`

```bash
curl http://localhost:8000/health
```

Réponse :

```json
{
  "status": "ok",
  "app": "parcelpulse-api"
}
```

---

# 14. Test `POST /predict`

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"distance_km":12.5,"package_weight_kg":3.2}' \
  http://localhost:8000/predict
```

Avec le modèle pédagogique :

```text
12.5 + 2 × 3.2 = 18.9
```

Réponse :

```json
{
  "risk": 0
}
```

Cas à risque :

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"distance_km":20,"package_weight_kg":5}' \
  http://localhost:8000/predict
```

Réponse :

```json
{
  "risk": 1
}
```

---

# 15. Payload invalide

```bash
curl \
  -i \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"distance_km":"abc","package_weight_kg":5}' \
  http://localhost:8000/predict
```

La requête doit être rejetée par FastAPI / Pydantic.

---

# 16. Partie E — client HTTP Python

`scripts/http_client.py` :

```python
import json
import os
from urllib.request import Request, urlopen


api_url = os.getenv("API_URL", "http://localhost:8000")

payload = {
    "distance_km": 12.5,
    "package_weight_kg": 3.2,
}

request = Request(
    f"{api_url}/predict",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urlopen(request) as response:
    print("status:", response.status)
    print("body:", response.read().decode("utf-8"))
```

Exécuter :

```bash
python scripts/http_client.py
```

---

# 17. Partie F — Pytest

`tests/test_api.py` :

```python
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app": "parcelpulse-api",
    }


def test_predict_valid():
    response = client.post(
        "/predict",
        json={
            "distance_km": 12.5,
            "package_weight_kg": 3.2,
        },
    )
    assert response.status_code == 200
    assert "risk" in response.json()


def test_predict_invalid():
    response = client.post(
        "/predict",
        json={
            "distance_km": "abc",
            "package_weight_kg": 3.2,
        },
    )
    assert response.status_code != 200


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
```

Lancer :

```bash
pytest -v
```

Résultat visé :

```text
4 passed
```

sous réserve de l’environnement et des versions installées.

---

# 18. Partie G — métriques FastAPI

L’instrumentation :

```python
Instrumentator().instrument(app).expose(app)
```

Tester :

```bash
curl http://localhost:8000/metrics
```

On doit obtenir des métriques au format Prometheus.

---

# 19. Partie H — `Dockerfile`

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

# 20. `.dockerignore`

```text
.venv/
.git/
__pycache__/
.pytest_cache/
*.pyc
```

---

# 21. Build et run Docker

```bash
docker build -t parcelpulse-api:latest .
```

Puis :

```bash
docker run \
  --rm \
  -p 8000:8000 \
  -e MODEL_PATH=models/model.joblib \
  parcelpulse-api:latest
```

Tester :

```bash
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

---

# 22. Partie I — `docker-compose.yml`

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      APP_NAME: parcelpulse-api
      APP_ENV: docker
      API_PORT: "8000"
      MODEL_PATH: /models/model.joblib
    volumes:
      - ./models:/models:ro

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    depends_on:
      - app

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources:ro
    depends_on:
      - prometheus
```

Le bind mount :

```yaml
./models:/models:ro
```

rend le `model.joblib` local directement disponible dans le container.

---

# 23. Démarrer Compose

```bash
docker compose up -d --build
```

Vérifier :

```bash
docker compose ps
```

Logs :

```bash
docker compose logs app
docker compose logs prometheus
docker compose logs grafana
```

---

# 24. Partie J — `config/prometheus.yml`

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: parcelpulse-api
    static_configs:
      - targets:
          - app:8000
```

Pourquoi :

```text
app
=
nom DNS du service Compose
```

Donc depuis Prometheus :

```text
app:8000
```

et non `localhost:8000`.

---

# 25. Validation Prometheus

Après `docker compose up` :

```text
parcelpulse-api
→ UP
```

Générer du trafic :

```bash
for i in {1..20}; do
  curl -s http://localhost:8000/health > /dev/null
done
```

Puis quelques POST :

```bash
for i in {1..10}; do
  curl -s \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"distance_km":12.5,"package_weight_kg":3.2}' \
    http://localhost:8000/predict \
    > /dev/null
done
```

---

# 26. Partie K — PromQL

Le support annonce PromQL mais pas les noms de métriques. La bonne méthode est donc :

```text
/metrics
↓
identifier une métrique réelle
↓
utiliser son vrai nom
```

Requête simple :

```promql
<real_metric_name>
```

Si la métrique est un compteur :

```promql
sum(
  rate(
    <real_counter_metric>[5m]
  )
)
```

Si un label `method` existe :

```promql
sum by (method) (
  rate(
    <real_counter_metric>[5m]
  )
)
```

Ne pas documenter une requête non testée.

---

# 27. Partie L — datasource Grafana

`grafana/provisioning/datasources/prometheus.yml` :

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

Depuis Grafana containerisé :

```text
prometheus
```

est le nom du service Compose.

---

# 28. Partie M — dashboard Grafana

Depuis l’UI :

```text
Dashboards
→ New
→ New dashboard
→ Add visualization
```

Nom :

```text
ParcelPulse Monitoring
```

Datasource :

```text
Prometheus
```

Panel minimal :

```text
HTTP Request Rate
```

avec une requête PromQL déjà validée dans Prometheus.

---

# 29. Partie N — GitLab

Repository source attendu avant l’examen :

```text
dst_rncp38919_bloc_3
```

Vérifier :

```bash
git remote -v
git status
```

Puis :

```bash
git add .
git commit -m "feat: implement bloc 3 practice project"
git push
```

---

# 30. Partie O — `.gitlab-ci.yml`

Version de référence :

```yaml
stages:
  - test
  - build

variables:
  IMAGE: parcelpulse-api:latest
  PYTHON_IMAGE: python:3.12-slim

tests:
  stage: test
  script:
    - |
      docker run --rm \
        --user "$(id -u):$(id -g)" \
        -e HOME=/tmp \
        -v "$CI_PROJECT_DIR:/build" -w /build \
        "$PYTHON_IMAGE" \
        sh -c 'set -e
               python --version
               python -m pip install --no-cache-dir --user -r requirements.txt
               python scripts/create_artifact.py
               python -m pytest -v'

docker_build:
  stage: build
  script:
    - docker build -t "$IMAGE" .
    - docker run --rm "$IMAGE" python -c "from app.main import app; print('Import OK:', app.title)"
```

⚠️ **Attention à la formulation de la question.** L'énoncé demande un runner de type **`shell`**, et cette configuration est écrite pour lui. Sur l'exécuteur `shell`, GitLab **ignore** `image:` et `services:` : il n'y a donc **ni `docker:27-dind`, ni `DOCKER_TLS_CERTDIR`, ni `privileged`**. Les jobs lancent eux-mêmes leurs conteneurs avec `docker run`, et `docker build` utilise directement le daemon Docker de la machine virtuelle — ce qui est précisément **pourquoi** ce runner ne demande aucun privilège particulier.

Les trois éléments à ne pas oublier dans le job `tests` :

| Élément | Rôle |
|---|---|
| `--user "$(id -u):$(id -g)"` + `-e HOME=/tmp` | le conteneur tourne avec l'utilisateur du runner : les fichiers produits lui appartiennent et restent supprimables par le nettoyage GitLab |
| `pip install ... --user` | obligatoire, sinon l'installation échoue faute de droits sur `site-packages` |
| `python -m pytest` | `$HOME/.local/bin` n'est pas dans le `PATH` ; `python -m` trouve le module |

Et pour le runner : `sudo gitlab-runner list` / `sudo -u gitlab-runner gitlab-runner verify` (le `verify` doit renvoyer `is valid`).


Vérifier :

```bash
gitlab-runner list
```

Preuve visée :

```text
pipeline vert
```

---

# 31. Variante DockerHub en CI

Extension de practice :

```yaml
stages:
  - test
  - build
  - push

push_image:
  stage: push
  script:
    - echo "$DOCKERHUB_TOKEN" |
      docker login
      -u "$DOCKERHUB_USER"
      --password-stdin
    - docker tag
      parcelpulse-api:latest
      "$DOCKERHUB_USER/parcelpulse-api:latest"
    - docker push
      "$DOCKERHUB_USER/parcelpulse-api:latest"
```

Ne jamais mettre le token en clair dans le repository.

---

# 32. Partie P — DockerHub

```bash
docker login
```

```bash
docker tag \
  parcelpulse-api:latest \
  USER/parcelpulse-api:latest
```

```bash
docker push \
  USER/parcelpulse-api:latest
```

Vérifier ensuite :

```text
repository parcelpulse-api
tag latest
image visible
```

---

# 33. Partie Q — Kubernetes

Le sujet blanc demande les six objets annoncés dans le support :

```text
Namespace
ConfigMap
PersistentVolume
PersistentVolumeClaim
Deployment
Service
```

---

# 34. `k8s/namespace.yml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: parcelpulse
```

---

# 35. `k8s/configmap.yml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: parcelpulse-config
  namespace: parcelpulse

data:
  APP_NAME: parcelpulse-api
  APP_ENV: kubernetes
  API_PORT: "8000"
  MODEL_PATH: /models/model.joblib
```

---

# 36. `k8s/pv.yml`

Pour un lab local :

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: parcelpulse-pv

spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /tmp/parcelpulse-models
```

> `hostPath` est un choix de lab. Le backend réel dépend du cluster. L'attribution explicite de `storageClassName: manual` garantit la liaison immédiate avec le PVC.

---

# 37. `k8s/pvc.yml`

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: parcelpulse-pvc
  namespace: parcelpulse

spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

---

# 38. Préparer l’artefact du lab Kubernetes

Si le cluster local utilise réellement ce `hostPath`, le nœud doit voir :

```text
/tmp/parcelpulse-models/model.joblib
```

La manière exacte de copier ce fichier dépend du cluster utilisé. Un `initContainer` (voir manifest ci-dessous) permet également d'automatiser cette copie depuis l'image vers le volume afin d'éviter tout `CrashLoopBackOff`.

---

# 39. `k8s/deployment.yml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: parcelpulse-api
  namespace: parcelpulse

spec:
  replicas: 1

  selector:
    matchLabels:
      app: parcelpulse-api

  template:
    metadata:
      labels:
        app: parcelpulse-api

    spec:
      initContainers:
        - name: init-model-artifact
          image: parcelpulse-api:latest
          imagePullPolicy: IfNotPresent
          command:
            - sh
            - -c
            - "if [ ! -f /models/model.joblib ]; then cp /app/models/model.joblib /models/model.joblib; fi"
          volumeMounts:
            - name: model-storage
              mountPath: /models

      containers:
        - name: api
          # Pour le déploiement DockerHub : remplacer par <DOCKERHUB_USER>/parcelpulse-api:latest
          image: parcelpulse-api:latest
          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 8000

          envFrom:
            - configMapRef:
                name: parcelpulse-config

          volumeMounts:
            - name: model-storage
              mountPath: /models

      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: parcelpulse-pvc
```

Règle critique :

```text
selector.matchLabels
=
template.metadata.labels
```

---

# 40. `k8s/service.yml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: parcelpulse-api-service
  namespace: parcelpulse

spec:
  selector:
    app: parcelpulse-api

  ports:
    - port: 8000
      targetPort: 8000
```

Règle :

```text
Service selector
=
Pod labels
```

---

# 41. Appliquer Kubernetes

```bash
kubectl apply -f k8s/
```

Vérifier :

```bash
kubectl get namespace parcelpulse
kubectl get pv
kubectl get pvc -n parcelpulse
kubectl get deployments -n parcelpulse
kubectl get pods -n parcelpulse
kubectl get services -n parcelpulse
```

Objectifs :

```text
PVC → Bound
Deployment → Available
Pod → Running
Service → présent
```

---

# 42. Debug Kubernetes

```bash
kubectl describe pod \
  <pod> \
  -n parcelpulse
```

```bash
kubectl logs \
  <pod> \
  -n parcelpulse
```

---

# 43. Test via port-forward

```bash
kubectl port-forward \
  service/parcelpulse-api-service \
  8000:8000 \
  -n parcelpulse
```

Puis :

```bash
curl http://localhost:8000/health
```

Résultat visé :

```json
{
  "status": "ok",
  "app": "parcelpulse-api"
}
```

---

# 44. README — structure de référence

```markdown
# ParcelPulse — RNCP 38919 Bloc 3 Practice

## Architecture
## Bootstrap configuration
## Environment variables
## Local run
## HTTP tests
## Pytest
## Docker
## Docker Compose
## GitLab CI
## DockerHub
## Kubernetes
## Prometheus
## PromQL
## Grafana
## Troubleshooting
```

---

# 45. Architecture ASCII du README

```text
GitLab
  ↓
Runner
  ↓
Pytest
  ↓
Docker
  ↓
DockerHub
  ↓
Kubernetes
  ↓
FastAPI
  ↓
Prometheus
  ↓
Grafana
```

---

# 46. Validation finale de référence

## Local

```text
[ ] model.joblib existe
[ ] FastAPI démarre
[ ] /health = 200
[ ] /predict = 200
[ ] /metrics = 200
[ ] pytest = PASS
```

## Docker / Compose

```text
[ ] docker build = OK
[ ] container = Running
[ ] app = Up
[ ] prometheus = Up
[ ] grafana = Up
[ ] target Prometheus = UP
[ ] datasource Grafana = OK
```

## GitLab / DockerHub

```text
[ ] push GitLab = OK
[ ] Runner shell = online
[ ] tests job = PASS
[ ] build job = PASS
[ ] image DockerHub visible si poussée
```

## Kubernetes

```text
[ ] Namespace présent
[ ] ConfigMap présente
[ ] PV présent
[ ] PVC Bound
[ ] Deployment Available
[ ] Pod Running
[ ] Service présent
[ ] /health accessible
```

---

# 47. Pannes fréquentes et diagnostic

## API ne démarre pas

Vérifier :

```text
MODEL_PATH
model.joblib
imports
requirements
```

## Pytest échoue au chargement

Vérifier que l’artefact a été créé :

```bash
python scripts/create_artifact.py
```

## Docker plante

Vérifier :

```text
MODEL_PATH
fichier monté / copié
commande uvicorn
port 8000
```

## Prometheus `DOWN`

Vérifier :

```text
/metrics
service app
hostname app
port 8000
prometheus.yml
```

## Grafana datasource KO

Vérifier :

```text
url = http://prometheus:9090
Prometheus actif
réseau Compose
fichier YAML monté
```

## GitLab job `pending`

Vérifier :

```text
Runner online
Runner associé
tags éventuels
Runner paused
```

## Kubernetes `ImagePullBackOff`

Vérifier :

```text
USER/repository
tag
visibilité
image réellement poussée
```

## Kubernetes `CrashLoopBackOff`

```bash
kubectl logs <pod> -n parcelpulse
```

Puis vérifier :

```text
MODEL_PATH
volume
ConfigMap
commande de démarrage
```

## Service sans trafic

Vérifier :

```text
Service selector
=
Pod labels
```

## PVC `Pending`

```bash
kubectl describe pvc parcelpulse-pvc -n parcelpulse
kubectl get pv
```

---

# 48. Auto-évaluation proposée

> **Non officielle.**

### Niveau A — application

```text
FastAPI
Pydantic
joblib
curl
Pytest
```

### Niveau B — industrialisation

```text
GitLab
Runner
Docker
Compose
DockerHub
```

### Niveau C — déploiement

```text
Namespace
ConfigMap
PV
PVC
Deployment
Service
```

### Niveau D — observabilité

```text
/metrics
Prometheus
PromQL
Grafana
```

---

# 49. Résumé de la correction

```text
BOOTSTRAP NOTEBOOK
        ↓
ENV VARS
        ↓
FASTAPI + PYDANTIC
        ↓
JOBLIB
        ↓
CURL + HTTP PYTHON
        ↓
PYTEST
        ↓
INSTRUMENTATOR
        ↓
DOCKER
        ↓
COMPOSE
        ↓
GITLAB CI / RUNNER
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
        ↓
VALIDATION
        ↓
ARCHIVE
```

---

# 50. Ce qu’il faut retenir

Le Bloc 3 se prépare mieux comme une chaîne que comme une liste de technologies :

```text
une application
↓
testée
↓
automatisée
↓
containerisée
↓
publiée
↓
déployée
↓
monitorée
↓
visualisée
```

---

# 51. Étape suivante

```text
16_RNCP_38919_BLOC_3_PRACTICE_LABS_PACK.zip
```

Le pack devra transformer cette correction en environnement de pratique comprenant :

```text
examen blanc
starter project
correction
notebook bootstrap
artefact joblib
labs Bash
labs GitLab
labs Docker
labs FastAPI
labs Pytest
labs Kubernetes
labs Prometheus
labs Grafana
scripts de validation
```
