# 14 — RNCP 38919 — Bloc 3
# Examen blanc 01 — Data Engineer / DevOps

**Type :** Sujet blanc proposé  
**Certification visée :** RNCP 38919 — Data Engineer  
**Bloc :** Bloc 3  
**Durée de simulation :** 4 heures  
**Niveau :** Difficile  
**Format :** pratique, chronométré, rendu sous forme d’archive

**Source de cadrage :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Important**
>
> Ce sujet blanc est un **entraînement proposé**. Il n’est ni le sujet officiel ni une reproduction d’un examen DataScientest.
>
> Il est construit uniquement à partir des thèmes explicitement annoncés dans le support :
>
> ```text
> lecture de notebook Jupyter
> export / .bashrc
> variables d’environnement Python
> environnements virtuels Python
> requêtes HTTP avec Python et Bash
> joblib
> GitLab Repository
> .gitlab-ci.yml
> gitlab-runner
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
> Kubernetes :
>   Namespace
>   PersistentVolume
>   PersistentVolumeClaim
>   ConfigMap
>   Service
>   Deployment
> Prometheus
> config/prometheus.yml
> PromQL
> Grafana
> datasources/<source_name>.yml
> dashboard via l’interface Grafana
> ```
>
> Le support source ne précise pas le scénario métier exact, les endpoints, les manifests attendus ni le contenu final précis de l’archive. Tous ces éléments sont donc définis ici uniquement pour la simulation.

---

# 1. Contexte fictif

Vous rejoignez l’équipe Data Platform de l’entreprise fictive :

```text
ParcelPulse
```

L’équipe dispose d’un artefact Data Science pré-entraîné :

```text
models/model.joblib
```

Cet artefact permet de produire un indicateur simple de risque à partir de variables numériques.

Votre mission consiste à transformer cet artefact en un service exploitable dans une chaîne DevOps complète :

```text
FastAPI
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

---

# 2. Règles de simulation

Chronomètre :

```text
4 heures
```

Travaillez comme en condition d’examen :

```text
[ ] pas de pause du chronomètre
[ ] progression incrémentale
[ ] validation régulière
[ ] archive finale obligatoire
```

Le support officiel annonce bien une épreuve de 4 heures avec rendu d’une archive ; le détail ci-dessus est adapté à l’entraînement.

---

# 3. Ressources fournies pour le sujet blanc

Dans le futur pack de practice associé à cet examen blanc, vous disposerez de :

```text
resources/
├── bootstrap_info.ipynb
├── model.joblib
└── README_DATA.md
```

Pour cette version Markdown du sujet, considérez que `bootstrap_info.ipynb` contient :

```text
APP_NAME      = parcelpulse-api
DEFAULT_PORT  = 8000
MODEL_PATH    = models/model.joblib
NAMESPACE     = parcelpulse
```

et que `model.joblib` est déjà fourni.

Vous n’avez pas à entraîner un modèle.

---

# 4. Objectif final

À la fin des 4 heures, votre projet doit idéalement permettre :

```text
1. lancer une API FastAPI
2. valider les entrées avec Pydantic
3. charger l’artefact joblib
4. tester l’API avec Pytest
5. tester l’API avec curl
6. lancer la CI GitLab
7. construire une image Docker
8. lancer une stack Compose
9. pousser une image DockerHub
10. déployer l’application sur Kubernetes
11. exposer des métriques
12. les collecter avec Prometheus
13. les interroger avec PromQL
14. les visualiser dans Grafana
```

---

# 5. Structure de projet attendue — proposition de l’examen blanc

```text
dst_rncp38919_bloc_3/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── schemas.py
│
├── models/
│   └── model.joblib
│
├── tests/
│   └── test_api.py
│
├── scripts/
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
├── .gitlab-ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Cette arborescence est propre au sujet blanc.

---

# 6. Partie A — Lecture du notebook Jupyter

**Temps conseillé : 10 minutes**

Le support officiel annonce la lecture de notebooks Jupyter.

À partir de `bootstrap_info.ipynb`, récupérer :

```text
APP_NAME
DEFAULT_PORT
MODEL_PATH
NAMESPACE
```

Puis reporter ces informations dans `README.md` sous :

```text
## Bootstrap configuration
```

---

# 7. Partie B — Bash et variables d’environnement

**Temps conseillé : 15 minutes**

Initialiser avec `export` :

```text
APP_ENV=exam
API_PORT=8000
MODEL_PATH=models/model.joblib
```

Afficher ensuite ces variables.

Ajouter uniquement :

```text
APP_ENV=exam
```

dans `~/.bashrc`, puis recharger le shell.

Documenter dans le README la commande utilisée.

---

# 8. Partie C — Configuration Python et venv

**Temps conseillé : 15 minutes**

Créer :

```text
app/config.py
```

qui lit :

```text
APP_ENV
API_PORT
MODEL_PATH
```

depuis l’environnement, avec des valeurs par défaut cohérentes.

Créer ensuite :

```text
.venv
```

et :

```text
requirements.txt
```

---

# 9. Partie D — FastAPI + Pydantic

**Temps conseillé : 30 minutes**

Créer une API FastAPI comportant au minimum :

```text
GET /health
POST /predict
```

## `GET /health`

Réponse attendue :

```json
{
  "status": "ok",
  "app": "parcelpulse-api"
}
```

## `POST /predict`

Créer :

```python
class PredictionRequest(BaseModel):
    distance_km: float
    package_weight_kg: float
```

Payload de test :

```json
{
  "distance_km": 12.5,
  "package_weight_kg": 3.2
}
```

Le chemin du modèle doit provenir de :

```text
MODEL_PATH
```

L’artefact `model.joblib` est fourni et doit être chargé avec `joblib`.

Pour cet entraînement, considérez que l’objet expose :

```python
predict(...)
```

compatible avec :

```python
[[distance_km, package_weight_kg]]
```

Réponse proposée :

```json
{
  "risk": 0
}
```

ou :

```json
{
  "risk": 1
}
```

---

# 10. Partie E — requêtes HTTP Bash et Python

**Temps conseillé : 15 minutes**

Tester `GET /health` avec `curl`.

Tester `POST /predict` avec :

```text
Content-Type: application/json
```

et un body JSON valide.

Créer aussi :

```text
scripts/http_client.py
```

qui :

```text
1. lit l’URL de l’API
2. envoie une requête
3. affiche le status code
4. affiche la réponse
```

Le support officiel ne fixe pas la bibliothèque Python HTTP.

---

# 11. Partie F — Pytest

**Temps conseillé : 20 minutes**

Créer `tests/test_api.py` avec au minimum :

```text
Test 1
GET /health
→ 200
→ body attendu

Test 2
POST /predict avec payload valide
→ 200
→ clé risk présente

Test 3
POST /predict avec payload invalide
→ erreur de validation

Test 4
GET /metrics
→ 200
```

---

# 12. Partie G — Prometheus Instrumentator

**Temps conseillé : 10 minutes**

Ajouter :

```text
prometheus-fastapi-instrumentator
```

à l’application.

Objectif :

```text
GET /metrics
```

doit être accessible.

---

# 13. Partie H — Dockerfile

**Temps conseillé : 20 minutes**

Créer un `Dockerfile` permettant de lancer l’API.

L’image doit :

```text
1. partir d’une image Python
2. installer requirements.txt
3. copier le projet
4. lancer FastAPI
```

Construire :

```text
parcelpulse-api:latest
```

Puis lancer le container en publiant :

```text
host 8000
→
container 8000
```

Tester ensuite `GET /health`.

---

# 14. Partie I — Docker Compose

**Temps conseillé : 20 minutes**

Créer `docker-compose.yml` avec :

```text
app
prometheus
grafana
```

## `app`

Doit :

```text
builder l’image locale
exposer 8000
recevoir les variables d’environnement
utiliser un volume pour /models
```

## `prometheus`

Doit :

```text
utiliser une image Prometheus
monter config/prometheus.yml
exposer 9090
dépendre de app
```

avec `services.depends_on`.

## `grafana`

Doit :

```text
utiliser une image Grafana
exposer 3000
monter la configuration de datasource
dépendre de prometheus
```

Créer également un volume nommé pour `/models`.

---

# 15. Partie J — Prometheus

**Temps conseillé : 20 minutes**

Créer :

```text
config/prometheus.yml
```

avec une target correspondant au service :

```text
app:8000
```

Après démarrage de Compose :

```text
la target FastAPI doit être UP
```

---

# 16. Partie K — PromQL

**Temps conseillé : 10 minutes**

À partir des métriques réellement exposées :

```text
1. identifier une métrique HTTP
2. exécuter une requête simple
3. filtrer ou agréger selon un label existant
4. utiliser rate(...) si la métrique s’y prête
```

Documenter dans le README au moins :

```text
2 requêtes PromQL réellement testées
```

Ne pas inventer les noms de métriques.

---

# 17. Partie L — Grafana datasource

**Temps conseillé : 10 minutes**

Créer :

```text
grafana/provisioning/datasources/prometheus.yml
```

ou une arborescence équivalente.

La datasource doit pointer vers Prometheus dans le réseau Compose.

---

# 18. Partie M — Grafana dashboard

**Temps conseillé : 10 minutes**

Depuis l’interface Grafana, créer un dashboard nommé :

```text
ParcelPulse Monitoring
```

Ajouter au minimum :

```text
1 panel
```

basé sur une requête PromQL réellement fonctionnelle.

---

# 19. Partie N — GitLab

**Temps conseillé : 15 minutes**

Utiliser le repository préparé avant l’épreuve :

```text
dst_rncp38919_bloc_3
```

Le projet doit être :

```text
commit
et
push
```

dans GitLab.

---

# 20. Partie O — `.gitlab-ci.yml`

**Temps conseillé : 20 minutes**

Créer un pipeline comportant au minimum :

```text
test
build
```

Le stage `test` doit exécuter Pytest.

Le stage `build` doit construire l’image Docker.

Le pipeline doit s’exécuter avec le Runner préparé :

```text
type : shell
nom : shell
```

---

# 21. Partie P — DockerHub

**Temps conseillé : 10 minutes**

Utiliser le compte et le token préparés avant l’examen.

Créer ou utiliser un repository de practice :

```text
parcelpulse-api
```

Puis :

```text
taguer
et
pousser
```

l’image.

`parcelpulse-api` est propre à cet examen blanc, pas au support officiel.

---

# 22. Partie Q — Kubernetes

**Temps conseillé : 40 minutes**

Créer les six types de ressources annoncés dans le support :

```text
Namespace
ConfigMap
PersistentVolume
PersistentVolumeClaim
Deployment
Service
```

## Namespace

Créer :

```text
parcelpulse
```

## ConfigMap

Créer :

```text
parcelpulse-config
```

avec :

```text
APP_ENV=kubernetes
MODEL_PATH=/models/model.joblib
```

## PersistentVolume

Créer :

```text
parcelpulse-pv
```

avec une capacité de practice de :

```text
1Gi
```

Le backend de stockage peut être adapté à votre environnement de lab.

## PersistentVolumeClaim

Créer :

```text
parcelpulse-pvc
```

demandant :

```text
1Gi
```

## Deployment

Créer :

```text
parcelpulse-api
```

avec :

```text
1 replica
```

et l’image DockerHub poussée précédemment.

Injecter la ConfigMap.

Monter le PVC dans :

```text
/models
```

## Service

Créer :

```text
parcelpulse-api-service
```

qui cible les Pods de l’application.

---

# 23. Validation Kubernetes

Vérifier :

```text
[ ] Namespace existe
[ ] Deployment disponible
[ ] Pod Running
[ ] Service présent
[ ] PVC Bound
```

dans la mesure permise par l’environnement de simulation.

Si possible, tester `GET /health` via un mécanisme de lab tel que `port-forward`.

---

# 24. Partie R — README

**Temps conseillé : 10 minutes**

Le README doit contenir au minimum :

```text
1. architecture générale
2. variables d’environnement
3. lancement local
4. tests
5. Docker
6. Compose
7. GitLab CI
8. DockerHub
9. Kubernetes
10. Prometheus
11. requêtes PromQL testées
12. Grafana
```

Ajouter cette architecture ASCII :

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

# 25. Partie S — validation finale

**Temps conseillé : 10 minutes**

Avant de créer l’archive :

```text
[ ] pytest passe
[ ] Dockerfile build
[ ] Compose démarre
[ ] /health répond
[ ] /metrics répond
[ ] Prometheus target UP
[ ] PromQL testé
[ ] Grafana datasource correcte
[ ] pipeline GitLab exécuté
[ ] manifests Kubernetes présents
```

---

# 26. Archive à produire

Créer :

```text
RNCP_38919_BLOC_3_EXAMEN_BLANC_01_<VOTRE_NOM>.zip
```

Contenu minimal proposé :

```text
app/
models/
tests/
scripts/
config/
grafana/
k8s/
.gitlab-ci.yml
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

Ne pas inclure inutilement :

```text
.venv/
.git/
caches
```

---

# 27. Critères d’auto-validation

> **Grille proposée pour l’entraînement — non officielle.**

## Niveau 1 — fondations

```text
[ ] env vars
[ ] FastAPI
[ ] Pydantic
[ ] curl
[ ] joblib
[ ] Pytest
```

## Niveau 2 — CI / container

```text
[ ] GitLab push
[ ] .gitlab-ci.yml
[ ] Runner
[ ] Dockerfile
[ ] Compose
[ ] DockerHub
```

## Niveau 3 — déploiement

```text
[ ] Namespace
[ ] ConfigMap
[ ] PV
[ ] PVC
[ ] Deployment
[ ] Service
```

## Niveau 4 — observabilité

```text
[ ] /metrics
[ ] Prometheus
[ ] target UP
[ ] PromQL
[ ] Grafana datasource
[ ] dashboard
```

---

# 28. Pannes volontaires optionnelles

Si vous terminez avant la fin des 4 heures, provoquer puis corriger une panne :

```text
1. mauvais port Prometheus
2. Service selector incorrect
3. image Docker tag incorrect
4. variable MODEL_PATH absente
5. test Pytest volontairement cassé
```

Documenter brièvement :

```text
symptôme
diagnostic
correction
```

---

# 29. Chronométrage conseillé

```text
00:00–00:10  Notebook / cadrage
00:10–00:25  Bash / env / venv
00:25–00:55  FastAPI / Pydantic / joblib
00:55–01:15  HTTP / Pytest / metrics
01:15–01:55  Docker / Compose
01:55–02:30  GitLab CI / DockerHub
02:30–03:10  Kubernetes
03:10–03:35  Prometheus / PromQL
03:35–03:50  Grafana / README
03:50–04:00  validation / archive
```

Ce chronométrage est spécifique à l’entraînement.

---

# 30. Règle anti-tunnel

Si une erreur dépasse :

```text
10–15 minutes
```

faire :

```text
logs
isolation
simplification
contournement
suite
```

---

# 31. Commandes de validation utiles

```bash
pytest -v

curl   http://localhost:8000/health

curl   http://localhost:8000/metrics

docker build   -t parcelpulse-api .

docker compose up   -d   --build

docker compose ps

gitlab-runner list

kubectl get pods   -n parcelpulse

kubectl get pvc   -n parcelpulse
```

---

# 32. Livrable attendu pour l’entraînement

À la fin :

```text
un projet exécutable
+
une archive
+
un README
+
des preuves de validation
```

---

# 33. Résumé du sujet blanc

```text
READ NOTEBOOK
    ↓
SET ENV
    ↓
CREATE FASTAPI
    ↓
LOAD JOBLIB
    ↓
TEST HTTP
    ↓
PYTEST
    ↓
INSTRUMENT METRICS
    ↓
DOCKER
    ↓
COMPOSE
    ↓
GITLAB CI
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
ARCHIVE
```

---

# 34. Fin de l’examen blanc

Lorsque le chronomètre atteint :

```text
03:50
```

arrêtez toute nouvelle fonctionnalité.

Passez uniquement à :

```text
validation
nettoyage
archive
upload simulé
```

---

# 35. Document suivant

```text
15_RNCP_38919_BLOC_3_CORRIGE_EXAMEN_BLANC_01.md
```

Le corrigé proposera :

```text
une implémentation de référence
les fichiers attendus
les commandes de validation
une pipeline CI
les manifests Kubernetes
Prometheus / PromQL
Grafana
et les principaux points de debug
```

tout en restant explicitement présenté comme **correction proposée de l’examen blanc**, et non comme correction officielle DataScientest.
