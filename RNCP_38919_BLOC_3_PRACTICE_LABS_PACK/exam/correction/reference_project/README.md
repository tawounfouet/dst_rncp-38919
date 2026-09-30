# ParcelPulse — RNCP 38919 Bloc 3 Practice

## Bootstrap configuration

```text
APP_NAME      = parcelpulse-api
DEFAULT_PORT  = 8000
MODEL_PATH    = models/model.joblib
NAMESPACE     = parcelpulse
```

## Architecture

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

## Local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/create_artifact.py
pytest -v
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker

```bash
docker build -t parcelpulse-api .
docker run --rm -p 8000:8000 parcelpulse-api
```

## Compose

```bash
docker compose up -d --build
docker compose ps
```

## Kubernetes

```bash
kubectl apply -f k8s/
kubectl get pods -n parcelpulse
```

## PromQL

Documenter ici **les noms de métriques réellement observés** dans `/metrics` et les deux requêtes testées. Ne pas inventer un nom de métrique.
