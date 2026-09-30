# 01 — RNCP 38919 — Bloc 3
# Fiche de révision

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures  
**Difficulté annoncée :** Difficile  
**Surveillance :** Mereos  
**Navigateur requis :** Google Chrome

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Source** : notion explicitement annoncée dans le support DataScientest.
> - **Réflexe de révision** : synthèse ou exemple pratique proposé pour préparer l’épreuve.
>
> Cette fiche ne cherche pas à inventer des exigences supplémentaires.

---

# 1. Le Bloc 3 en une page

## Source

L’épreuve dure :

```text
4 heures
```

Elle est surveillée avec :

```text
Mereos
```

et nécessite :

```text
Google Chrome
```

Le support annonce un périmètre centré sur :

```text
Bash
Python
HTTP
joblib
GitLab
GitLab CI
GitLab Runner
Docker
DockerHub
Pytest
FastAPI
Pydantic
Kubernetes
Prometheus
PromQL
Grafana
```

---

# 2. Modèle mental global

## Réflexe de révision

```text
CODE
 ↓
TEST
 ↓
CI
 ↓
BUILD IMAGE
 ↓
REGISTRY
 ↓
DEPLOY
 ↓
EXPOSE
 ↓
MONITOR
 ↓
DASHBOARD
```

Traduction concrète :

```text
Python / FastAPI
→ Pytest
→ GitLab CI
→ Docker
→ DockerHub
→ Kubernetes
→ Prometheus
→ Grafana
```

---

# 3. Préparation obligatoire avant l’examen

## Source

Le support demande de préparer :

```text
GitLab
DockerHub
```

### GitLab

Créer un repository privé nommé :

```text
dst_rncp38919_bloc_3
```

Créer une clé SSH puis ajouter la clé publique au compte GitLab.

Créer un Runner :

```text
type : shell
nom : shell
```

et l’enregistrer sur la machine virtuelle.

### DockerHub

Créer un compte puis générer :

```text
un Personal Access Token
```

---

# 4. Bash — variables d’environnement

## Source

Le support cite :

```text
export
.bashrc
```

## Réflexe de révision

### Variable temporaire

```bash
export API_URL=http://localhost:8000
```

Lire :

```bash
echo $API_URL
```

### Persistance via `.bashrc`

Ajouter :

```bash
export API_URL=http://localhost:8000
```

puis recharger :

```bash
source ~/.bashrc
```

---

# 5. Variables d’environnement en Python

## Source

Le support annonce leur utilisation dans des scripts Python.

## Réflexe

```python
import os

api_url = os.getenv("API_URL")
```

Modèle mental :

```text
Shell
→ Environment
→ Python
```

---

# 6. Environnement virtuel Python

## Source

Le support cite :

```text
initialisation d’environnements virtuels
```

## Réflexe

```bash
python -m venv .venv
```

Activation Linux / macOS :

```bash
source .venv/bin/activate
```

---

# 7. Requêtes HTTP

## Source

Le support demande de savoir envoyer des requêtes :

```text
avec Python
et
avec Bash
```

et cite :

```text
curl
```

## Réflexe Bash

```bash
curl http://localhost:8000
```

## Réflexe conceptuel Python

Le support ne fixe pas dans la page fournie une bibliothèque Python spécifique.

À retenir :

```text
URL
method
headers
body
response
status code
```

---

# 8. `joblib`

## Source

Le support cite `joblib` pour enregistrer :

```text
des modèles de machine learning
et autres objets liés à la data science
```

## Réflexe

```python
import joblib

joblib.dump(
    model,
    "model.joblib",
)
```

Chargement :

```python
model = joblib.load(
    "model.joblib"
)
```

---

# 9. GitLab Repository

## Source

Le support annonce l’utilisation :

```text
d’un Repository
```

## Réflexe de révision

Chaîne :

```text
git init
→ add
→ commit
→ remote
→ push
```

Exemple :

```bash
git add .
git commit -m "Initial commit"
git push
```

---

# 10. `.gitlab-ci.yml`

## Source

Le support annonce :

```text
création d’un pipeline
à l’aide de .gitlab-ci.yml
```

## Modèle mental

```text
Repository
   ↓
.gitlab-ci.yml
   ↓
Pipeline
   ↓
Jobs
   ↓
Runner
```

---

# 11. GitLab Runner

## Source

Le support cite :

```text
gitlab-runner
```

et un Runner :

```text
shell
```

## Réflexe

```text
Pipeline
→ Runner
→ shell de la VM
→ commandes exécutées
```

---

# 12. Pipeline CI minimal

## Réflexe de révision

Exemple conceptuel :

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
    - docker build -t my-image .
```

> Le support n’impose pas ce pipeline exact ; c’est un squelette de révision.

---

# 13. Dockerfile

## Source

Le support annonce :

```text
création d’un Dockerfile
```

## Réflexe

Squelette :

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

# 14. Volumes Docker

## Source

Le support cite :

```text
volumes
```

## Réflexe

```yaml
volumes:
  - data:/app/data
```

Modèle mental :

```text
container
≠
stockage persistant
```

---

# 15. Docker Compose

## Source

Le support demande :

```text
docker-compose.yml
```

et cite explicitement :

```text
services.depends_on
```

## Réflexe

```yaml
services:
  app:
    build: .
    depends_on:
      - prometheus
```

À retenir :

```text
services
image
build
ports
volumes
environment
depends_on
```

---

# 16. DockerHub

## Source

Le support demande de savoir utiliser :

```text
les repositories d’un compte DockerHub
```

## Modèle mental

```text
docker build
   ↓
docker tag
   ↓
docker push
   ↓
DockerHub
```

---

# 17. Pytest

## Source

Le framework annoncé est :

```text
Pytest
```

## Réflexes

Lancer :

```bash
pytest
```

Mode verbeux :

```bash
pytest -v
```

Convention :

```text
test_*.py
test_*
```

Exemple :

```python
def test_health():
    assert True
```

---

# 18. FastAPI

## Source

Le support cite :

```text
FastAPI
```

## Réflexe minimal

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

# 19. Pydantic `BaseModel`

## Source

Le support cite explicitement :

```text
pydantic.BaseModel
```

## Réflexe

```python
from pydantic import BaseModel


class PredictionRequest(
    BaseModel
):
    value: float
```

Modèle mental :

```text
JSON request
→ BaseModel
→ FastAPI endpoint
```

---

# 20. FastAPI + Pydantic

## Réflexe

```python
@app.post("/predict")
def predict(
    payload: PredictionRequest
):
    return {
        "prediction": 0
    }
```

Le support n’impose pas cet endpoint précis.

---

# 21. `curl` + FastAPI

## Source

`curl` est explicitement annoncé.

## Réflexe

GET :

```bash
curl \
  http://localhost:8000/
```

POST :

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": 12.5}' \
  http://localhost:8000/predict
```

---

# 22. `prometheus-fastapi-instrumentator`

## Source

Le support cite :

```text
prometheus-fastapi-instrumentator
```

avec FastAPI et Prometheus.

## Modèle mental

```text
FastAPI
↓
instrumentator
↓
metrics endpoint
↓
Prometheus
```

---

# 23. Kubernetes — objets à connaître

## Source

Le support cite exactement :

```text
Namespaces
PersistentVolumes
PersistentVolumeClaims
ConfigMaps
Services
Deployments
```

---

# 24. Namespace

## Réflexe

```text
Namespace
=
espace logique d’isolation
```

Exemple conceptuel :

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: rncp-bloc3
```

---

# 25. ConfigMap

## Réflexe

```text
ConfigMap
=
configuration non sensible
```

Exemple :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  API_MODE: production
```

---

# 26. Deployment

## Réflexe

```text
Deployment
→ pods applicatifs
```

Concepts :

```text
replicas
selector
template
containers
image
ports
env
```

---

# 27. Service

## Réflexe

```text
Service
→ accès réseau aux Pods
```

Modèle mental :

```text
Client
↓
Service
↓
Pod(s)
```

---

# 28. PersistentVolume

## Source

```text
PersistentVolume
```

## Réflexe

```text
PV
=
ressource de stockage disponible
```

---

# 29. PersistentVolumeClaim

## Source

```text
PersistentVolumeClaim
```

## Modèle mental

```text
Pod
 ↓
PVC
 ↓
PV
```

---

# 30. Architecture Kubernetes à retenir

```text
Namespace
   │
   ├── ConfigMap
   │
   ├── Deployment
   │      ↓
   │     Pods
   │
   ├── Service
   │      ↓
   │     réseau
   │
   └── PVC
          ↓
         PV
```

---

# 31. Prometheus

## Source

Le support cite :

```text
Prometheus
```

avec :

```text
prometheus-fastapi-instrumentator
config/prometheus.yml
PromQL
```

---

# 32. `prometheus.yml`

## Source

Le chemin annoncé est :

```text
config/prometheus.yml
```

## Modèle mental

```text
Prometheus
→ scrape target
→ metrics
```

---

# 33. PromQL

## Source

Le langage annoncé est :

```text
PromQL
```

## Réflexe

Comprendre :

```text
metric
labels
filter
rate
aggregation
```

Le support ne fournit pas dans cette page une liste de requêtes imposées.

---

# 34. Grafana

## Source

Le support cite :

```text
Grafana
```

avec :

```text
datasources/<source_name>.yml
```

et :

```text
création d’un dashboard depuis l’UI
```

---

# 35. Chaîne Prometheus → Grafana

```text
FastAPI
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

# 36. Chaîne CI/CD complète

## Réflexe de révision

```text
git push
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
```

---

# 37. Chaîne déploiement complète

```text
DockerHub image
     ↓
Kubernetes Deployment
     ↓
Pods
     ↓
Service
     ↓
FastAPI
```

---

# 38. Chaîne observabilité complète

```text
FastAPI
↓
prometheus-fastapi-instrumentator
↓
Prometheus
↓
PromQL
↓
Grafana
```

---

# 39. Commandes à connaître en priorité

## Bash

```bash
export VAR=value
echo $VAR
source ~/.bashrc
```

## Python

```bash
python -m venv .venv
source .venv/bin/activate
```

## HTTP

```bash
curl URL
```

## Tests

```bash
pytest -v
```

## Docker

```bash
docker build
docker run
docker ps
docker logs
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

---

# 40. Kubernetes — commandes de révision

## Réflexe de préparation

```bash
kubectl apply -f file.yml
kubectl get pods
kubectl get services
kubectl get deployments
kubectl describe pod <name>
kubectl logs <pod>
```

> Le support annonce les objets Kubernetes mais ne liste pas ces commandes exactes.

---

# 41. Fichiers YAML à savoir reconnaître

```text
.gitlab-ci.yml
docker-compose.yml
namespace.yml
configmap.yml
deployment.yml
service.yml
pv.yml
pvc.yml
prometheus.yml
datasource.yml
```

---

# 42. Pièges fréquents

## Réflexe de révision

### GitLab

```text
Runner non disponible
tag incorrect
pipeline qui ne démarre pas
```

### Docker

```text
port incorrect
volume absent
depends_on mal indenté
```

### Kubernetes

```text
selector ≠ labels
image incorrecte
namespace oublié
PVC non lié
```

### Prometheus

```text
target non joignable
mauvais port
mauvais endpoint metrics
```

### Grafana

```text
mauvaise URL datasource
Prometheus inaccessible
```

---

# 43. Diagnostic rapide GitLab

```text
Pipeline créé ?
Runner online ?
Runner shell enregistré ?
Job assigné ?
Logs du job ?
```

---

# 44. Diagnostic rapide Docker

```text
docker ps
docker logs
docker compose ps
docker compose logs
```

---

# 45. Diagnostic rapide Kubernetes

```text
Deployment existe ?
Pods Running ?
Service existe ?
ConfigMap existe ?
PVC Bound ?
Logs du Pod ?
```

---

# 46. Diagnostic rapide Prometheus

```text
FastAPI expose des métriques ?
Prometheus peut joindre la cible ?
prometheus.yml correct ?
target UP ?
PromQL renvoie des données ?
```

---

# 47. Diagnostic rapide Grafana

```text
datasource configurée ?
URL Prometheus correcte ?
connexion OK ?
dashboard utilise une métrique existante ?
```

---

# 48. Préparation avant Jour J

## Source

GitLab :

```text
[ ] compte créé
[ ] repo dst_rncp38919_bloc_3
[ ] clé SSH ajoutée
[ ] Runner shell créé
[ ] Runner enregistré
```

DockerHub :

```text
[ ] compte créé
[ ] token généré
[ ] authentification prête
```

---

# 49. VM — réflexes avant démarrage

## Source

La VM est la même que pour le Bloc 2.

Le support recommande de repartir sur :

```text
un environnement vierge
```

## Checklist

```text
[ ] vieux fichiers supprimés
[ ] vieux dossiers supprimés
[ ] vieux containers supprimés
[ ] Docker OK
[ ] Git OK
[ ] Python OK
```

---

# 50. Révision flash — 2 minutes

Réciter :

```text
export
.bashrc
os.getenv
venv
curl
joblib

GitLab
.gitlab-ci.yml
Runner

Dockerfile
volume
Compose
depends_on
DockerHub

Pytest
FastAPI
BaseModel

Namespace
PV
PVC
ConfigMap
Service
Deployment

Prometheus
prometheus.yml
PromQL

Grafana
datasource
dashboard
```

---

# 51. Auto-évaluation express

1. Comment rendre une variable disponible dans le shell ?
2. Comment la rendre persistante via Bash ?
3. Comment lire une env var dans Python ?
4. Comment créer un venv ?
5. À quoi sert `curl` ?
6. À quoi sert `joblib` ?
7. Quel fichier définit le pipeline GitLab ?
8. Quel est le rôle du Runner ?
9. Quelle différence entre Dockerfile et Compose ?
10. À quoi sert `depends_on` ?
11. À quoi sert DockerHub ?
12. Quel rôle joue `BaseModel` ?
13. Comment lancer Pytest ?
14. Que fait un Deployment ?
15. Que fait un Service ?
16. Différence PV / PVC ?
17. À quoi sert ConfigMap ?
18. Comment Prometheus récupère-t-il les métriques ?
19. À quoi sert PromQL ?
20. À quoi sert la datasource Grafana ?

---

# 52. Réponses express

```text
1. export VAR=value
2. ajouter l’export dans .bashrc
3. os.getenv(...)
4. python -m venv .venv
5. envoyer une requête HTTP depuis le shell
6. sérialiser / recharger des objets Python
7. .gitlab-ci.yml
8. exécuter les jobs du pipeline
9. Dockerfile = image ; Compose = orchestration de services
10. déclarer une dépendance logique entre services
11. stocker / distribuer des images Docker
12. définir / valider des structures de données
13. pytest / pytest -v
14. gérer le déploiement des Pods
15. exposer / router vers les Pods
16. PV = stockage ; PVC = demande de stockage
17. fournir de la configuration
18. en scrappant une cible configurée
19. interroger les métriques Prometheus
20. connecter Grafana à une source de métriques
```

---

# 53. Priorités de révision

## Priorité 1

```text
GitLab CI
Runner
Docker
FastAPI
Pytest
```

## Priorité 2

```text
Kubernetes
Prometheus
Grafana
```

## Priorité 3

```text
Bash
env vars
curl
joblib
```

> Cette hiérarchie est une stratégie de préparation proposée, pas un barème officiel.

---

# 54. Fil rouge final

À mémoriser :

```text
CODE
 ↓
TEST
 ↓
CI
 ↓
IMAGE
 ↓
REGISTRY
 ↓
KUBERNETES
 ↓
METRICS
 ↓
DASHBOARD
```

---

# 55. Document suivant

```text
02_RNCP_38919_BLOC_3_MEGA_CHEATSHEET.md
```

Objectif :

> réduire cette fiche aux commandes, snippets, YAML et patterns à retrouver en quelques secondes.
