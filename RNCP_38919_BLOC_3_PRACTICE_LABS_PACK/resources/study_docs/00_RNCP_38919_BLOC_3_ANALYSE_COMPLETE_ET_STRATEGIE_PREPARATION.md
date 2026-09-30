# 00 — RNCP 38919 — Bloc 3
# Analyse complète et stratégie de préparation

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures  
**Niveau annoncé :** Difficile  
**Surveillance :** Mereos  
**Navigateur requis :** Google Chrome

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

**Source visuelle complémentaire :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.pdf`

> **Convention de ce document**
>
> - **Attendu source** : ce qui est explicitement annoncé dans le support DataScientest.
> - **Analyse** : lecture structurée du périmètre annoncé.
> - **Stratégie proposée** : méthode de préparation ou d’exécution construite à partir de ce périmètre.
>
> Ce document ne cherche pas à inventer le contenu exact de l’examen réel.
> Il organise uniquement les thèmes, outils et prérequis explicitement annoncés par DataScientest.

---

# 1. Positionnement général du Bloc 3

## Attendu source

Le support annonce :

```text
Bloc 3 RNCP 38919
Difficulté : Difficile
Temps approximatif : 4h00
```

L’examen est minuté et dure :

```text
4 heures
```

La surveillance est assurée par :

```text
Mereos
```

et l’utilisation de :

```text
Google Chrome
```

est obligatoire.

Le rendu est uploadé directement :

```text
sur la page du sujet de l'examen
```

---

# 2. Différence fondamentale avec le Bloc 2

## Analyse

Le Bloc 2 était centré autour d’une chaîne :

```text
Data
→ ETL
→ Base
→ ORM
→ ML
```

Le Bloc 3 change de nature.

Le cœur du périmètre devient :

```text
DEV
→ TEST
→ CI/CD
→ CONTAINER
→ DEPLOY
→ MONITOR
```

Autrement dit :

```text
Python / FastAPI
        ↓
Pytest
        ↓
GitLab CI/CD
        ↓
Docker / DockerHub
        ↓
Kubernetes
        ↓
Prometheus
        ↓
Grafana
```

---

# 3. Vue consolidée du périmètre officiel

## Attendu source

Les sujets annoncés sont :

```text
1. Lecture de notebooks Jupyter
2. Variables d'environnement via bash export
3. Modification de .bashrc
4. Variables d'environnement dans Python
5. Environnements virtuels Python
6. Requêtes HTTP avec Python et Bash
7. joblib
8. GitLab
9. Docker
10. Pytest
11. FastAPI
12. prometheus-fastapi-instrumentator
13. pydantic.BaseModel
14. curl
15. Kubernetes
16. Prometheus
17. PromQL
18. Grafana
```

---

# 4. Cartographie par domaine

## 4.1 Système / Bash

```text
export
.bashrc
variables d'environnement
curl
requêtes HTTP
```

## 4.2 Python

```text
virtualenv
variables d'environnement
requêtes HTTP
joblib
FastAPI
Pydantic
Pytest
```

## 4.3 CI/CD

```text
GitLab Repository
.gitlab-ci.yml
GitLab Runner
gitlab-runner
```

## 4.4 Containerisation

```text
Dockerfile
volumes
docker-compose.yml
services.depends_on
DockerHub
```

## 4.5 Orchestration

```text
Kubernetes Namespace
PersistentVolume
PersistentVolumeClaim
ConfigMap
Service
Deployment
```

## 4.6 Observabilité

```text
prometheus-fastapi-instrumentator
prometheus.yml
PromQL
Grafana datasource
Grafana dashboard
```

---

# 5. Modèle mental du Bloc 3

## Analyse

Le Bloc 3 peut être lu comme la construction d’une application industrialisée :

```text
Python App
   │
   ▼
FastAPI
   │
   ▼
Pydantic
   │
   ▼
Pytest
   │
   ▼
GitLab Repository
   │
   ▼
.gitlab-ci.yml
   │
   ▼
GitLab Runner
   │
   ▼
Docker Build
   │
   ▼
DockerHub
   │
   ▼
Kubernetes Deployment
   │
   ├────────────┐
   │            │
   ▼            ▼
Service      ConfigMap
   │
   ▼
Prometheus
   │
   ▼
PromQL
   │
   ▼
Grafana
```

---

# 6. Machine virtuelle et environnement de départ

## Attendu source

Le support indique que :

```text
la machine virtuelle utilisée
est la même que pour le Bloc 2
```

et recommande :

```text
si elle n'est pas vide,
supprimer fichiers,
dossiers,
containers Docker,
etc.
```

pour repartir sur :

```text
un environnement vierge
```

## Stratégie proposée

Avant l’examen :

```text
[ ] vérifier Docker
[ ] vérifier Git
[ ] vérifier Python
[ ] vérifier GitLab Runner
[ ] vérifier connexion SSH GitLab
[ ] nettoyer anciens containers
[ ] nettoyer anciens dossiers de travail
```

---

# 7. Préparation GitLab obligatoire

## Attendu source

Avant l’examen, le support demande :

```text
créer un compte GitLab
```

puis un repository privé nommé exactement :

```text
dst_rncp38919_bloc_3
```

---

# 8. Clé SSH GitLab

## Attendu source

Il faut :

```text
créer une clé SSH sur la VM
```

puis :

```text
ajouter la clé publique au compte GitLab
```

## Analyse

Cela implique que la préparation ne doit pas commencer le jour J avec :

```text
aucune authentification GitLab configurée
```

Le repository doit déjà être exploitable.

---

# 9. GitLab Runner

## Attendu source

Le support demande :

```text
créer un Runner de type shell
```

nommé :

```text
shell
```

puis l’enregistrer sur la machine virtuelle avec :

```text
gitlab-runner
```

## Analyse

Ce point est particulièrement important.

Le Bloc 3 ne teste donc pas uniquement :

```text
syntaxe .gitlab-ci.yml
```

mais aussi le lien :

```text
GitLab
→ pipeline
→ Runner
→ machine
```

---

# 10. Préparation DockerHub

## Attendu source

Il faut :

```text
créer un compte DockerHub
```

puis générer :

```text
un Personal Access Token
```

Le support détaille le chemin :

```text
Profile
→ Account settings
→ Personal access tokens
→ Generate new token
```

---

# 11. Premier grand axe : variables d’environnement

## Attendu source

Le support cite :

```text
export
.bashrc
variables d’environnement dans Python
```

## Analyse

Ce thème relie plusieurs couches :

```text
Bash
→ environnement shell
→ Python
→ Docker
→ Kubernetes ConfigMap
```

C’est donc un concept transversal.

---

# 12. `export`

## Attendu source

Le support demande de savoir initialiser des variables via :

```bash
export
```

## Stratégie de révision

Exemple :

```bash
export API_URL=http://localhost:8000
```

Puis :

```bash
echo $API_URL
```

---

# 13. `.bashrc`

## Attendu source

Le support demande de savoir :

```text
modifier le shell Bash
via le fichier .bashrc
```

## Analyse

La compétence attendue est probablement de comprendre la différence entre :

```text
export dans une session
```

et :

```text
variable réinitialisée via .bashrc
```

---

# 14. Variables d’environnement en Python

## Attendu source

Le support annonce :

```text
utilisation de variables d’environnement
dans des scripts Python
```

## Réflexe

```python
import os

api_url = os.getenv(
    "API_URL"
)
```

Modèle mental :

```text
Shell
→ env var
→ Python
```

---

# 15. Environnement virtuel Python

## Attendu source

Le support cite :

```text
initialisation d'environnements virtuels
pour des projets Python
```

## Réflexe

```bash
python -m venv .venv
```

Puis :

```bash
source .venv/bin/activate
```

---

# 16. Requêtes HTTP en Bash

## Attendu source

Le support mentionne :

```text
Bash
→ requêtes vers une URL
```

et cite explicitement :

```text
curl
```

## Réflexe

```bash
curl http://localhost:8000
```

---

# 17. Requêtes HTTP en Python

## Attendu source

Le support demande aussi :

```text
Python
→ requêtes HTTP
```

## Analyse

Le support ne précise pas dans la page fournie la librairie Python à utiliser.

Il ne faut donc pas imposer une bibliothèque particulière comme exigence officielle.

---

# 18. `joblib`

## Attendu source

Le support décrit :

```text
joblib
```

comme une librairie permettant d’enregistrer :

```text
des modèles de machine learning
et autres objets liés à la data science
```

## Analyse

Contrairement au Bloc 2 où `joblib` apparaissait dans la chaîne ML,
ici il réapparaît dans un contexte DevOps.

Il faut donc savoir :

```text
sauvegarder
et
recharger
```

un artefact.

---

# 19. GitLab — Repository

## Attendu source

Le support cite :

```text
utilisation d’un Repository
```

## Analyse

Le repository est le point d’entrée du pipeline :

```text
code
↓
commit
↓
push
↓
pipeline
```

---

# 20. `.gitlab-ci.yml`

## Attendu source

Le support demande :

```text
création d’un pipeline
à l’aide de .gitlab-ci.yml
```

## Analyse

C’est une compétence centrale.

Le candidat doit comprendre le lien :

```text
repository
→ .gitlab-ci.yml
→ jobs
→ runner
```

---

# 21. GitLab Runner

## Attendu source

Le support cite :

```text
gitlab-runner
```

et la création d’un :

```text
Runner shell
```

## Modèle mental

```text
GitLab Pipeline
       │
       ▼
Runner
       │
       ▼
Shell de la VM
       │
       ▼
Commandes exécutées
```

---

# 22. Dockerfile

## Attendu source

Le support cite explicitement :

```text
création d’un Dockerfile
```

## Analyse

Le candidat doit au minimum comprendre :

```text
base image
workdir
copy
install
command
```

même si la page source ne liste pas ces instructions individuellement.

---

# 23. Volumes Docker

## Attendu source

Le support cite :

```text
volumes
```

## Analyse

La notion de persistance revient donc aussi dans le Bloc 3.

---

# 24. `docker-compose.yml`

## Attendu source

Le support demande :

```text
création d’un docker-compose.yml
```

avec attention particulière à :

```text
services.depends_on
```

## Analyse

Ce n’est donc pas seulement :

```text
savoir lancer Compose
```

mais aussi comprendre :

```text
ordre logique des services
```

---

# 25. DockerHub

## Attendu source

Le support mentionne :

```text
utilisation des répertoires d’un compte DockerHub
```

## Analyse

La chaîne CI/CD complète devient :

```text
GitLab
→ build Docker
→ DockerHub
→ Kubernetes
```

---

# 26. Pytest

## Attendu source

Le framework annoncé est :

```text
Pytest
```

## Analyse

Il faut pouvoir intégrer :

```text
tests
```

dans :

```text
le projet Python
et
le pipeline CI
```

---

# 27. FastAPI

## Attendu source

Le support cite :

```text
FastAPI
```

## Analyse

FastAPI sert probablement de composant applicatif central autour duquel se construisent :

```text
Pydantic
tests
Docker
Kubernetes
Prometheus
Grafana
```

Le support ne donne pas dans cette page une API précise à implémenter.

---

# 28. Pydantic `BaseModel`

## Attendu source

Le support cite explicitement :

```text
pydantic.BaseModel
```

## Analyse

Il faut donc être capable de relier :

```text
request JSON
→ modèle Pydantic
→ endpoint FastAPI
```

---

# 29. `prometheus-fastapi-instrumentator`

## Attendu source

Le support cite deux fois :

```text
prometheus-fastapi-instrumentator
```

une première fois avec FastAPI,
puis dans la section Prometheus.

## Analyse

Cette librairie constitue le pont :

```text
FastAPI
→ métriques
→ Prometheus
```

---

# 30. Kubernetes — vue d’ensemble

## Attendu source

Le support annonce :

```text
Namespaces
PersistentVolumes
PersistentVolumeClaims
ConfigMaps
Services
Deployments
```

## Analyse

Ces objets peuvent être structurés ainsi :

```text
Namespace
   │
   ├── ConfigMap
   ├── Deployment
   │      ↓
   │     Pods
   │
   ├── Service
   │      ↓
   │    exposition
   │
   └── PVC
          ↓
         PV
```

---

# 31. Namespace

## Attendu source

Le support demande la gestion des :

```text
Namespaces
```

## Analyse

Le candidat doit comprendre leur rôle d’isolation logique.

---

# 32. PersistentVolume

## Attendu source

Le support cite :

```text
PersistentVolumes
```

---

# 33. PersistentVolumeClaim

## Attendu source

Le support cite :

```text
PersistentVolumeClaims
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

# 34. ConfigMap

## Attendu source

Le support cite :

```text
ConfigMaps
```

## Analyse

C’est le prolongement Kubernetes du thème :

```text
configuration
≠
code
```

---

# 35. Service

## Attendu source

Le support cite :

```text
Services
```

## Analyse

Il faut comprendre le lien :

```text
Service
→ accès réseau
→ Pods
```

---

# 36. Deployment

## Attendu source

Le support cite :

```text
Deployments
```

## Modèle mental

```text
Deployment
↓
ReplicaSet
↓
Pods
```

Le support ne détaille pas ReplicaSet dans la page fournie ;
il faut donc rester centré sur le rôle du Deployment.

---

# 37. Prometheus

## Attendu source

Le support annonce :

```text
outil de monitoring Prometheus
```

avec :

```text
prometheus-fastapi-instrumentator
config/prometheus.yml
PromQL
```

---

# 38. `prometheus.yml`

## Attendu source

Le support cite explicitement :

```text
config/prometheus.yml
```

## Analyse

Le candidat doit donc connaître au minimum la logique :

```text
Prometheus
→ scrape target
→ métriques
```

---

# 39. PromQL

## Attendu source

Le langage annoncé est :

```text
PromQL
```

## Analyse

Il faut donc pouvoir interroger des métriques.

Le support ne fournit pas dans cette page la liste des requêtes PromQL exactes.

---

# 40. Grafana

## Attendu source

Le support cite :

```text
Grafana
```

avec deux compétences :

```text
configuration d’une source de données
via datasources/<source_name>.yml
```

et :

```text
création d’un dashboard
depuis l’UI
```

---

# 41. Chaîne d’observabilité complète

## Analyse

```text
FastAPI
   │
   ▼
prometheus-fastapi-instrumentator
   │
   ▼
/metrics
   │
   ▼
Prometheus
   │
   ▼
PromQL
   │
   ▼
Grafana
```

C’est l’un des flux à connaître par cœur.

---

# 42. Architecture end-to-end du Bloc 3

## Analyse

```text
Developer
   │
   ▼
GitLab Repository
   │
   ▼
.gitlab-ci.yml
   │
   ▼
Shell Runner
   │
   ├── pytest
   ├── docker build
   └── docker push
            │
            ▼
        DockerHub
            │
            ▼
       Kubernetes
            │
            ▼
        FastAPI App
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

# 43. Compétences à automatiser

## Stratégie proposée

Le Bloc 3 contient de nombreux outils.

L’objectif ne doit pas être :

```text
tout apprendre en profondeur
```

mais plutôt :

```text
automatiser les gestes critiques
```

à savoir :

```text
env vars
venv
curl
pytest
FastAPI minimal
Dockerfile
Compose
GitLab CI
Runner
kubectl apply
Kubernetes YAML
Prometheus config
Grafana datasource
```

---

# 44. Matrice compétences / outils

| Domaine | Outils | Niveau à viser |
|---|---|---|
| Shell | Bash, export, .bashrc, curl | Fluide |
| Python | venv, env vars, joblib | Fluide |
| API | FastAPI, Pydantic | Fluide |
| Tests | Pytest | Fluide |
| CI/CD | GitLab CI, Runner | Très fluide |
| Containers | Docker, Compose, DockerHub | Très fluide |
| Orchestration | Kubernetes YAML | Opérationnel |
| Monitoring | Prometheus, PromQL | Opérationnel |
| Dashboard | Grafana | Opérationnel |

> Cette échelle est une stratégie de préparation proposée, pas un barème officiel.

---

# 45. Risques principaux

## Analyse

### Risque 1 — dispersion

Le périmètre est large :

```text
GitLab
Docker
FastAPI
Kubernetes
Prometheus
Grafana
```

Le risque est de connaître :

```text
un peu de tout
```

sans savoir assembler la chaîne.

---

# 46. Risque 2 — perte de temps sur l’infrastructure

Les zones à fort risque de debug sont :

```text
Runner
Docker
réseau
ports
Kubernetes
Prometheus
```

Un petit problème de configuration peut consommer beaucoup de temps.

---

# 47. Risque 3 — prérequis non préparés

Le support demande de préparer avant l’examen :

```text
GitLab
SSH
Runner
DockerHub token
```

Arriver sans cela peut consommer une partie importante des 4 heures.

---

# 48. Risque 4 — YAML

Le Bloc 3 contient plusieurs fichiers YAML :

```text
.gitlab-ci.yml
docker-compose.yml
Kubernetes manifests
prometheus.yml
Grafana datasource.yml
```

Le risque de :

```text
indentation
clé incorrecte
nom incorrect
```

est donc élevé.

---

# 49. Risque 5 — confusion configuration / code

Le thème configuration revient partout :

```text
export
.bashrc
Python env vars
Docker env
ConfigMap
Prometheus config
Grafana datasource
```

Il faut garder le principe :

```text
CODE
≠
CONFIG
```

---

# 50. Stratégie de préparation globale

## Phase 1 — fondamentaux shell / Python

À maîtriser :

```text
export
.bashrc
os.getenv
venv
curl
requêtes HTTP
joblib
```

---

# 51. Phase 2 — FastAPI + Pydantic + Pytest

Construire un mini-service :

```text
GET /
POST /predict
GET /metrics
```

avec :

```text
BaseModel
pytest
```

---

# 52. Phase 3 — Docker

Containeriser l’application :

```text
FastAPI
→ Dockerfile
→ docker build
→ docker run
```

---

# 53. Phase 4 — Compose

Ajouter :

```text
app
+
Prometheus
+
Grafana
```

ou un ensemble réduit selon le lab.

---

# 54. Phase 5 — GitLab CI/CD

Pipeline minimal :

```text
test
↓
build
↓
push
```

avec :

```text
Runner shell
```

---

# 55. Phase 6 — Kubernetes

Déployer l’image :

```text
Namespace
ConfigMap
Deployment
Service
```

Puis, si stockage nécessaire :

```text
PV
PVC
```

---

# 56. Phase 7 — Monitoring

Brancher :

```text
FastAPI metrics
↓
Prometheus
↓
PromQL
↓
Grafana
```

---

# 57. Phase 8 — examen blanc

Simulation complète :

```text
4 heures
```

avec :

```text
GitLab
Docker
FastAPI
Kubernetes
Prometheus
Grafana
```

---

# 58. Découpage proposé d’une simulation 4 h

> Stratégie proposée, non officielle.

```text
00:00–00:15  Lecture / cadrage
00:15–00:45  Python / FastAPI / Pydantic
00:45–01:10  Pytest
01:10–01:45  Docker / Compose
01:45–02:20  GitLab CI / Runner
02:20–03:05  Kubernetes
03:05–03:35  Prometheus / PromQL
03:35–03:50  Grafana
03:50–04:00  Vérification / archive / upload
```

---

# 59. Checkpoint à 1 h

```text
[ ] app Python fonctionne
[ ] API répond
[ ] modèle Pydantic fonctionne
[ ] tests principaux passent
```

---

# 60. Checkpoint à 2 h

```text
[ ] image Docker construite
[ ] Compose fonctionnel
[ ] pipeline GitLab lancé
```

---

# 61. Checkpoint à 3 h

```text
[ ] ressources Kubernetes appliquées
[ ] service accessible
```

---

# 62. Checkpoint à 3 h 30

```text
[ ] Prometheus scrape
[ ] requête PromQL valide
[ ] Grafana relié
```

---

# 63. Checkpoint à 3 h 50

```text
STOP NOUVEAU CHANTIER
```

Faire uniquement :

```text
vérifier
documenter
archiver
uploader
```

---

# 64. Règle anti-tunnel

## Stratégie proposée

Aucun bug ne devrait absorber :

```text
30+ minutes
```

sans décision.

Après :

```text
10–15 minutes
```

faire :

```text
logs
simplification
contournement
documentation
suite
```

---

# 65. Ordre des priorités

## Stratégie proposée

```text
P0
──
FastAPI
tests
Docker

P1
──
GitLab CI
Kubernetes

P2
──
Prometheus
Grafana

P3
──
raffinements / optimisation
```

Cette priorité peut être adaptée au sujet réel.

---

# 66. Artéfacts à savoir produire de mémoire

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

prometheus.yml
grafana datasource.yml
```

---

# 67. Syntaxes à savoir retrouver très vite

```text
export VAR=value
echo $VAR

python -m venv .venv
source .venv/bin/activate

curl ...

pytest

docker build
docker run
docker compose up -d

gitlab-runner ...

kubectl apply -f ...
kubectl get ...
kubectl describe ...
kubectl logs ...
```

> Les commandes `kubectl` ci-dessus relèvent d’une stratégie de préparation générale.
> La page source annonce les objets Kubernetes, mais ne liste pas les commandes exactes à utiliser.

---

# 68. Documents de préparation proposés

```text
00_RNCP_38919_BLOC_3_ANALYSE_COMPLETE_ET_STRATEGIE_PREPARATION.md
01_RNCP_38919_BLOC_3_FICHE_REVISION.md
02_RNCP_38919_BLOC_3_MEGA_CHEATSHEET.md
03_RNCP_38919_BLOC_3_BASH_ENV_HTTP_GUIDE.md
04_RNCP_38919_BLOC_3_GITLAB_CICD_RUNNER_GUIDE.md
05_RNCP_38919_BLOC_3_DOCKER_DOCKERHUB_GUIDE.md
06_RNCP_38919_BLOC_3_FASTAPI_PYDANTIC_GUIDE.md
07_RNCP_38919_BLOC_3_PYTEST_TESTING_GUIDE.md
08_RNCP_38919_BLOC_3_KUBERNETES_GUIDE.md
09_RNCP_38919_BLOC_3_PROMETHEUS_PROMQL_GUIDE.md
10_RNCP_38919_BLOC_3_GRAFANA_GUIDE.md
11_RNCP_38919_BLOC_3_TEMPLATE_PROJECT.md
12_RNCP_38919_BLOC_3_STRATEGIE_EXAMEN_4H.md
13_RNCP_38919_BLOC_3_CHECKLIST_JOUR_J.md
14_RNCP_38919_BLOC_3_EXAMEN_BLANC_01.md
15_RNCP_38919_BLOC_3_CORRIGE_EXAMEN_BLANC_01.md
16_RNCP_38919_BLOC_3_PRACTICE_LABS_PACK.zip
```

---

# 69. Dépendances entre les sujets

## Analyse

```text
Bash env vars
     ↓
Python env vars
     ↓
FastAPI
     ↓
Pytest
     ↓
Docker
     ↓
GitLab CI
     ↓
DockerHub
     ↓
Kubernetes
     ↓
Prometheus
     ↓
Grafana
```

Cette séquence fournit un ordre naturel d’apprentissage.

---

# 70. Parcours de révision conseillé

```text
JOUR 1
Bash + env + HTTP

JOUR 2
FastAPI + Pydantic

JOUR 3
Pytest + joblib

JOUR 4
Docker + Compose

JOUR 5
GitLab CI + Runner

JOUR 6
Kubernetes

JOUR 7
Prometheus + Grafana

JOUR 8
End-to-End

JOUR 9
Examen blanc 4 h
```

> Ce calendrier est une proposition de préparation, pas une consigne officielle.

---

# 71. Questions essentielles à savoir répondre

1. Quelle différence entre `export` et `.bashrc` ?
2. Comment lire une variable d’environnement en Python ?
3. Quel rôle joue `BaseModel` dans FastAPI ?
4. Comment tester une API avec Pytest ?
5. À quoi sert `.gitlab-ci.yml` ?
6. Quel rôle joue un GitLab Runner ?
7. Quelle différence entre Dockerfile et Compose ?
8. À quoi sert `depends_on` ?
9. Quel rôle joue DockerHub ?
10. Quelle différence entre Deployment et Service ?
11. Quelle différence entre PV et PVC ?
12. À quoi sert ConfigMap ?
13. Comment Prometheus récupère-t-il les métriques ?
14. À quoi sert PromQL ?
15. Comment Grafana consomme-t-il Prometheus ?

---

# 72. Checklist de préparation pré-examen

## GitLab

```text
[ ] compte actif
[ ] repo dst_rncp38919_bloc_3 créé
[ ] accès SSH OK
[ ] Runner shell créé
[ ] Runner enregistré
```

## DockerHub

```text
[ ] compte actif
[ ] token créé
[ ] connexion DockerHub testée
```

## VM

```text
[ ] environnement nettoyé
[ ] Docker opérationnel
[ ] Python opérationnel
[ ] Git opérationnel
```

---

# 73. Définition de maîtrise minimale

Le candidat est prêt lorsque, sans suivre un tutoriel ligne par ligne, il peut reconstruire :

```text
FastAPI
↓
Pytest
↓
Dockerfile
↓
docker-compose
↓
GitLab CI
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

# 74. Ce qu’il ne faut pas sur-préparer

## Analyse

Le support ne mentionne pas explicitement :

```text
Helm
Terraform
ArgoCD
Istio
Kafka
Airflow
GitHub Actions
```

Ils peuvent être utiles dans d’autres contextes, mais ils ne doivent pas détourner la préparation du périmètre annoncé.

---

# 75. Fil rouge à retenir

Le Bloc 3 peut être résumé en une phrase :

> **Prendre une application Python et l’amener jusqu’à un état testable, intégrable, conteneurisé, déployable et observable.**

Modèle final :

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
DEPLOYMENT
 ↓
METRICS
 ↓
DASHBOARD
```

---

# 76. Prochaine étape

```text
01_RNCP_38919_BLOC_3_FICHE_REVISION.md
```

Objectif :

> condenser ce document en fiche de révision structurée par blocs :
> Bash, Python, FastAPI, GitLab CI, Docker, Kubernetes, Prometheus et Grafana.
