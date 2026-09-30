# 05 — RNCP 38919 — Bloc 3
# Guide Docker, Docker Compose et DockerHub

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Attendu source** : élément explicitement annoncé dans le support DataScientest.
> - **Guide pratique** : commandes, exemples YAML et mini-labs proposés pour la préparation.
>
> Le support annonce explicitement :
>
> ```text
> Docker
> Dockerfile
> volumes
> docker-compose.yml
> services.depends_on
> DockerHub repositories
> compte DockerHub
> Personal Access Token
> ```
>
> Le support ne fournit pas, dans la page source, un Dockerfile ou un Compose exact à reproduire.
> Les exemples ci-dessous sont donc des **patterns de pratique**.

---

# 1. Position de Docker dans le Bloc 3

## Attendu source

Le support annonce :

```text
Docker
├── Dockerfile
├── volumes
├── docker-compose.yml
├── services.depends_on
└── DockerHub
```

## Modèle mental

```text
Code
 ↓
Dockerfile
 ↓
docker build
 ↓
Image
 ↓
docker run
 ↓
Container
```

Puis :

```text
Image
 ↓
tag
 ↓
DockerHub
 ↓
pull
 ↓
Kubernetes
```

---

# 2. Dockerfile

## Attendu source

Le support demande :

```text
la création d’un Dockerfile
```

## Guide pratique

Squelette minimal :

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

# 3. Instructions Dockerfile à reconnaître

## Guide pratique

```text
FROM
WORKDIR
COPY
RUN
CMD
```

Pattern :

```text
FROM
→ image de base

WORKDIR
→ répertoire de travail

COPY
→ copie des fichiers

RUN
→ commande pendant le build

CMD
→ commande au démarrage du container
```

---

# 4. Dockerfile FastAPI

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

# 5. Construire une image

```bash
docker build \
  -t rncp-bloc3:latest \
  .
```

---

# 6. Vérifier les images

```bash
docker images
```

---

# 7. Lancer un container

```bash
docker run \
  --rm \
  -p 8000:8000 \
  rncp-bloc3:latest
```

---

# 8. Ports

Pattern :

```text
host:container
```

Exemple :

```bash
-p 8000:8000
```

signifie :

```text
localhost:8000
→
container:8000
```

---

# 9. Variables d’environnement dans Docker

## Guide pratique

```bash
docker run \
  --rm \
  -e APP_ENV=production \
  rncp-bloc3:latest
```

Dans Python :

```python
import os

app_env = os.getenv(
    "APP_ENV"
)
```

---

# 10. Fichier `.env`

Pattern pratique :

```env
APP_ENV=production
API_PORT=8000
MODEL_PATH=models/model.joblib
```

Avec Compose :

```yaml
env_file:
  - .env
```

> Le support annonce les variables d’environnement au niveau général du Bloc 3 ; cet exemple montre leur intégration Docker.

---

# 11. Logs Docker

```bash
docker logs <container>
```

Suivi :

```bash
docker logs \
  -f \
  <container>
```

---

# 12. Lister les containers

Actifs :

```bash
docker ps
```

Tous :

```bash
docker ps -a
```

---

# 13. Arrêter un container

```bash
docker stop \
  <container>
```

---

# 14. Supprimer un container

```bash
docker rm \
  <container>
```

---

# 15. Supprimer une image

```bash
docker rmi \
  rncp-bloc3:latest
```

---

# 16. Volumes Docker

## Attendu source

Le support cite explicitement :

```text
volumes
```

## Modèle mental

```text
Container
→ éphémère

Volume
→ persistance
```

---

# 17. Volume nommé

```bash
docker volume create \
  app_data
```

Lister :

```bash
docker volume ls
```

---

# 18. Monter un volume

```bash
docker run \
  --rm \
  -v app_data:/data \
  rncp-bloc3:latest
```

---

# 19. Bind mount

Pattern :

```bash
docker run \
  -v "$(pwd)/data:/data" \
  rncp-bloc3:latest
```

Différence mentale :

```text
named volume
→ géré par Docker

bind mount
→ dossier local explicite
```

---

# 20. Docker Compose

## Attendu source

Le support demande :

```text
création d’un docker-compose.yml
```

## Guide pratique

Compose permet de définir :

```text
plusieurs services
réseau
ports
variables
volumes
dépendances
```

---

# 21. Squelette Compose minimal

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
```

---

# 22. `services.depends_on`

## Attendu source

Le support cite explicitement :

```text
services.depends_on
```

## Pattern

```yaml
services:
  app:
    depends_on:
      - prometheus
```

---

# 23. Interprétation de `depends_on`

## Guide pratique

```text
depends_on
=
déclaration de dépendance entre services
```

Attention :

```text
dépendance de démarrage
≠
garantie applicative complète de readiness
```

> Ce dernier point est une précision générale de pratique, pas une phrase du support.

---

# 24. Compose — app + Prometheus + Grafana

Pattern de préparation :

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"

  prometheus:
    image: prom/prometheus
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

# 25. Compose avec volumes

```yaml
services:
  app:
    build: .
    volumes:
      - app_data:/data

volumes:
  app_data:
```

---

# 26. Compose avec variables

```yaml
services:
  app:
    build: .
    environment:
      APP_ENV: production
```

ou :

```yaml
services:
  app:
    env_file:
      - .env
```

---

# 27. Commandes Compose

Démarrer :

```bash
docker compose up -d
```

Avec rebuild :

```bash
docker compose up \
  -d \
  --build
```

---

# 28. Vérifier les services

```bash
docker compose ps
```

---

# 29. Logs Compose

```bash
docker compose logs
```

Un service :

```bash
docker compose logs \
  app
```

Suivi :

```bash
docker compose logs \
  -f \
  app
```

---

# 30. Arrêter Compose

```bash
docker compose down
```

---

# 31. Supprimer aussi les volumes

Pattern de pratique :

```bash
docker compose down \
  -v
```

À utiliser avec prudence si les données doivent être conservées.

---

# 32. DockerHub — exigence du support

## Attendu source

Le support demande :

```text
créer un compte DockerHub
```

puis :

```text
générer un token d’accès
```

Chemin indiqué :

```text
Profile
→ Account settings
→ Personal access tokens
→ Generate new token
```

---

# 33. Pourquoi DockerHub

## Analyse

DockerHub joue le rôle de :

```text
registry d’images
```

Chaîne :

```text
docker build
 ↓
image locale
 ↓
docker tag
 ↓
docker push
 ↓
DockerHub
```

---

# 34. Login DockerHub

```bash
docker login
```

Le mot de passe peut être remplacé par :

```text
Personal Access Token
```

selon la méthode d’authentification utilisée.

---

# 35. Login avec token

Pattern de pratique :

```bash
echo "$DOCKERHUB_TOKEN" \
  | docker login \
      -u "$DOCKERHUB_USER" \
      --password-stdin
```

---

# 36. Tag d’image

Image locale :

```text
rncp-bloc3:latest
```

Image DockerHub :

```text
USER/rncp-bloc3:latest
```

Commande :

```bash
docker tag \
  rncp-bloc3:latest \
  USER/rncp-bloc3:latest
```

---

# 37. Push

```bash
docker push \
  USER/rncp-bloc3:latest
```

---

# 38. Pull

```bash
docker pull \
  USER/rncp-bloc3:latest
```

---

# 39. Vérification du repository DockerHub

## Guide pratique

Après le push, vérifier dans DockerHub :

```text
repository
tag
date
```

---

# 40. Cycle complet DockerHub

```text
CODE
 ↓
DOCKERFILE
 ↓
BUILD
 ↓
IMAGE LOCAL
 ↓
TAG
 ↓
LOGIN
 ↓
PUSH
 ↓
DOCKERHUB
```

---

# 41. GitLab CI + DockerHub

## Guide pratique

Le Bloc 3 annonce à la fois :

```text
GitLab CI
et
DockerHub
```

Un pattern d’entraînement cohérent est :

```text
git push
↓
pipeline
↓
pytest
↓
docker build
↓
docker login
↓
docker push
```

---

# 42. Pipeline de pratique

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

> Squelette de practice, non fourni par la source.

---

# 43. Attention au Runner shell

Avec un Runner `shell`, Docker doit être disponible dans l’environnement du Runner.

Vérifier :

```bash
docker --version
```

Puis :

```bash
docker ps
```

dans le même contexte utilisateur si possible.

---

# 44. Docker et permissions

## Guide pratique

Symptôme possible :

```text
permission denied
```

Vérifier :

```bash
whoami
docker ps
```

Le problème peut être lié à :

```text
droits utilisateur
groupe Docker
daemon inaccessible
```

> Ce diagnostic est une aide générale, non détaillée dans la page source.

---

# 45. Dockerfile — ordre des couches

## Guide pratique

Pattern utile :

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

Cela permet généralement de mieux exploiter le cache de build qu’un :

```dockerfile
COPY . .
RUN pip install ...
```

> Optimisation générale de pratique, pas exigence du support.

---

# 46. `.dockerignore`

Pattern utile :

```text
.venv/
__pycache__/
.git/
.pytest_cache/
*.pyc
```

> `.dockerignore` n’est pas cité dans la page source ; il est ajouté comme bonne pratique.

---

# 47. Health check manuel

Après démarrage :

```bash
curl \
  http://localhost:8000/health
```

Modèle :

```text
docker run
↓
port
↓
curl
↓
réponse API
```

---

# 48. Debug Docker 60 secondes

```text
Image existe ?
      ↓
Container running ?
      ↓
Port publié ?
      ↓
Logs ?
      ↓
Variable présente ?
      ↓
Volume correct ?
```

---

# 49. Commandes de debug prioritaires

```bash
docker ps
docker ps -a
docker images
docker logs <container>
docker inspect <container>
```

> `docker inspect` est une commande de pratique utile, non explicitement citée dans le support.

---

# 50. Debug Compose

```bash
docker compose ps
docker compose logs
```

Un service :

```bash
docker compose logs \
  app
```

---

# 51. Erreur — port déjà utilisé

Symptôme :

```text
bind: address already in use
```

Réflexe :

```text
identifier le service qui occupe le port
ou
changer le port host
```

---

# 52. Erreur — application inaccessible

Vérifier :

```text
container actif ?
port exposé ?
app écoute sur 0.0.0.0 ?
bon port ?
```

Pour FastAPI dans un container :

```text
0.0.0.0
```

est généralement nécessaire pour être accessible depuis l’extérieur du container.

---

# 53. Erreur — fichier absent pendant le build

Vérifier :

```text
contexte de build
COPY
chemin relatif
.dockerignore
```

---

# 54. Erreur — image DockerHub introuvable

Vérifier :

```text
username
repository
tag
visibilité
push effectué
```

---

# 55. Erreur — push refusé

Vérifier :

```text
docker login
token
repository
nom du tag
droits
```

---

# 56. Erreur — `depends_on`

Vérifier :

```text
nom du service
indentation YAML
structure services:
```

Exemple correct :

```yaml
services:
  app:
    depends_on:
      - db
```

---

# 57. Mini-lab 1 — Dockerfile

## Mission

Créer une app Python :

```python
print("Bloc 3 Docker OK")
```

Créer un Dockerfile.

Puis :

```bash
docker build \
  -t bloc3-demo .
```

et :

```bash
docker run \
  --rm \
  bloc3-demo
```

---

# 58. Mini-lab 2 — FastAPI containerisée

Créer :

```text
GET /health
```

Puis :

```bash
docker build \
  -t bloc3-api .
```

```bash
docker run \
  --rm \
  -p 8000:8000 \
  bloc3-api
```

Tester :

```bash
curl \
  http://localhost:8000/health
```

---

# 59. Mini-lab 3 — volume

Créer un container qui écrit :

```text
/data/result.txt
```

Monter :

```text
app_data:/data
```

Redémarrer le container et vérifier la persistance.

---

# 60. Mini-lab 4 — Compose

Créer :

```text
app
+
prometheus
```

avec :

```text
depends_on
```

Puis :

```bash
docker compose up -d
```

---

# 61. Mini-lab 5 — logs

Provoquer volontairement une erreur Python.

Puis diagnostiquer uniquement avec :

```bash
docker compose ps
docker compose logs app
```

---

# 62. Mini-lab 6 — DockerHub

Créer un repository :

```text
bloc3-practice
```

Puis :

```text
build
tag
login
push
```

Vérifier dans l’UI.

---

# 63. Mini-lab 7 — pull propre

Supprimer l’image locale :

```bash
docker rmi \
  USER/bloc3-practice:latest
```

Puis :

```bash
docker pull \
  USER/bloc3-practice:latest
```

---

# 64. Mini-lab 8 — GitLab CI + Docker

Créer un pipeline :

```text
test
→ build
```

Puis pousser un commit et vérifier que :

```text
pytest passe
docker build passe
```

---

# 65. Mini-lab 9 — GitLab CI + DockerHub

Objectif :

```text
commit
↓
pytest
↓
build
↓
tag
↓
push DockerHub
```

Ce lab relie directement :

```text
GitLab
+
Docker
+
DockerHub
```

---

# 66. Checklist Docker avant examen

```text
[ ] docker --version
[ ] docker ps
[ ] docker build testé
[ ] docker run testé
[ ] docker compose version
[ ] docker compose up testé
[ ] volumes compris
[ ] depends_on compris
```

---

# 67. Checklist DockerHub avant examen

## Source + préparation

```text
[ ] compte DockerHub créé
[ ] token généré
[ ] docker login fonctionne
[ ] repository de practice créé
[ ] docker push déjà testé
```

Les deux premiers éléments sont explicitement demandés par le support ; les trois suivants sont des vérifications de préparation proposées.

---

# 68. Questions flash

1. À quoi sert un Dockerfile ?
2. Différence image / container ?
3. À quoi sert un volume ?
4. Quelle commande construit une image ?
5. Quelle commande lance un container ?
6. Quel rôle joue `-p` ?
7. À quoi sert `docker-compose.yml` ?
8. À quoi sert `depends_on` ?
9. À quoi sert DockerHub ?
10. Pourquoi taguer une image ?
11. Comment pousser une image ?
12. Pourquoi utiliser un token DockerHub ?
13. Quelle commande permet de voir les logs ?
14. Comment voir les services Compose ?
15. Quelle chaîne relie GitLab CI et DockerHub ?

---

# 69. Réponses flash

```text
1. décrire la construction d’une image.
2. image = modèle ; container = instance en exécution.
3. persister / monter des données.
4. docker build.
5. docker run.
6. publier un port host vers container.
7. décrire et lancer plusieurs services.
8. déclarer une dépendance entre services.
9. stocker et distribuer des images.
10. donner un nom complet repository:tag.
11. docker push.
12. authentifier sans utiliser directement le mot de passe du compte.
13. docker logs.
14. docker compose ps.
15. pipeline → build → tag → login → push.
```

---

# 70. Cheatsheet 30 secondes

```bash
docker build \
  -t app .

docker run \
  --rm \
  -p 8000:8000 \
  app

docker ps
docker logs <container>

docker compose up -d
docker compose ps
docker compose logs
docker compose down

docker login

docker tag \
  app \
  USER/app:latest

docker push \
  USER/app:latest
```

---

# 71. Fil rouge à retenir

```text
CODE
 ↓
DOCKERFILE
 ↓
BUILD
 ↓
IMAGE
 ↓
CONTAINER
 ↓
TAG
 ↓
DOCKERHUB
```

Puis :

```text
DOCKERHUB
 ↓
KUBERNETES
```

---

# 72. Document suivant

```text
06_RNCP_38919_BLOC_3_FASTAPI_PYDANTIC_GUIDE.md
```

Objectif :

> approfondir FastAPI, `pydantic.BaseModel`,
> endpoints HTTP, chargement d’artefact `joblib`,
> tests manuels avec `curl` et exposition des métriques.
