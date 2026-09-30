# 12 — RNCP 38919 — Bloc 3
# Stratégie d’examen 4 heures

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures  
**Difficulté annoncée :** Difficile

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Important**
>
> Le support DataScientest fixe :
>
> ```text
> durée : 4 heures
> surveillance : Mereos
> navigateur : Google Chrome
> rendu : archive à uploader
> ```
>
> Il annonce également le périmètre technique :
>
> ```text
> Bash / env vars
> Python / HTTP / joblib
> GitLab / .gitlab-ci.yml / Runner
> Docker / Compose / DockerHub
> Pytest
> FastAPI / Pydantic
> Kubernetes
> Prometheus / PromQL
> Grafana
> ```
>
> En revanche, la page source ne fournit pas un découpage minute par minute de l’épreuve.
>
> La stratégie ci-dessous est donc une **stratégie proposée** de gestion du temps et des risques.

---

# 1. Objectif de la stratégie

L’objectif n’est pas :

```text
faire chaque partie parfaitement
```

mais :

```text
maximiser le nombre de briques fonctionnelles
+
éviter les tunnels de debug
+
sécuriser le rendu final
```

Le modèle général est :

```text
COMPRENDRE
  ↓
PRODUIRE
  ↓
TESTER
  ↓
INTEGRER
  ↓
VALIDER
  ↓
ARCHIVER
  ↓
UPLOADER
```

---

# 2. Règle absolue : garder du temps pour le rendu

## Attendu source

Le support indique que le rendu doit être :

```text
uploadé directement
sur la page de l’examen
```

## Stratégie proposée

Réserver au minimum :

```text
10 à 15 minutes
```

en fin d’épreuve pour :

```text
nettoyage
vérification
archive
upload
```

Ne jamais utiliser :

```text
les 240 minutes
```

pour du développement pur.

---

# 3. Découpage global proposé

```text
00:00–00:15  Lecture et cadrage
00:15–00:45  Fondations Bash / Python / FastAPI
00:45–01:10  Pytest et validation locale
01:10–01:45  Docker / Compose
01:45–02:20  GitLab CI / Runner / DockerHub
02:20–03:05  Kubernetes
03:05–03:35  Prometheus / PromQL
03:35–03:50  Grafana
03:50–04:00  Validation finale / archive / upload
```

Ce découpage doit être adapté au vrai sujet.

---

# 4. T0 — 00:00 à 00:15
# Lecture et cadrage

## Objectif

Ne pas commencer à coder immédiatement.

Faire d’abord :

```text
1. lire tout le sujet
2. repérer les livrables
3. repérer les fichiers attendus
4. identifier les dépendances
5. identifier ce qui peut être fait indépendamment
```

---

# 5. Checklist de lecture initiale

Créer rapidement une liste :

```text
[ ] Bash / env vars
[ ] Python / HTTP
[ ] joblib
[ ] FastAPI
[ ] Pydantic
[ ] Pytest
[ ] GitLab CI
[ ] Runner
[ ] Dockerfile
[ ] Compose
[ ] DockerHub
[ ] Kubernetes
[ ] Prometheus
[ ] PromQL
[ ] Grafana
[ ] archive finale
```

Puis marquer :

```text
OBLIGATOIRE
OPTIONNEL
DEPENDANT
INDEPENDANT
```

selon le sujet réel.

---

# 6. Construire la dependency map

## Stratégie proposée

Exemple :

```text
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

Si une brique dépend d’une autre :

```text
ne pas commencer trop tôt
la brique downstream
```

---

# 7. Créer l’arborescence immédiatement

## Stratégie proposée

Créer une structure simple :

```text
project/
├── app/
├── tests/
├── config/
├── grafana/
├── k8s/
├── Dockerfile
├── docker-compose.yml
├── .gitlab-ci.yml
└── README.md
```

Avantages :

```text
moins d’improvisation
moins d’erreurs de chemins
vision claire
```

---

# 8. Premier commit très tôt

Si le sujet utilise GitLab :

```text
git init / clone
↓
premier commit
↓
push
```

But :

```text
sécuriser une première version
```

Ne pas attendre 3 heures avant le premier push.

---

# 9. T1 — 00:15 à 00:45
# Fondations Bash / Python / FastAPI

## Priorité

Obtenir rapidement :

```text
une application minimale fonctionnelle
```

Exemple :

```text
GET /health
POST /predict
```

selon le sujet réel.

---

# 10. Variables d’environnement

## Attendu source

Le support annonce :

```text
export
.bashrc
variables d’environnement Python
```

## Stratégie proposée

Vérifier immédiatement les variables nécessaires :

```bash
echo $VAR
```

et côté Python :

```python
os.getenv("VAR")
```

Ne pas perdre 20 minutes sur un bug provoqué par :

```text
une variable absente
```

---

# 11. Venv

## Attendu source

Le support annonce :

```text
environnement virtuel Python
```

## Stratégie proposée

Dès le début :

```bash
python -m venv .venv
source .venv/bin/activate
```

Puis :

```bash
pip install -r requirements.txt
```

si le sujet fournit ou demande un fichier de dépendances.

---

# 12. Première validation

Avant d’aller plus loin :

```bash
python --version
```

Puis :

```bash
python -c "print('Python OK')"
```

---

# 13. HTTP minimal

## Attendu source

Le support annonce :

```text
requêtes HTTP Python
requêtes HTTP Bash
curl
```

## Stratégie proposée

Dès que FastAPI tourne :

```bash
curl \
  http://localhost:8000/health
```

Si ce test échoue :

```text
ne pas passer à Docker
```

---

# 14. `joblib`

Si le sujet utilise un artefact :

```text
vérifier son chemin
```

avant toute containerisation.

Test :

```python
joblib.load(...)
```

ou un script minimal.

---

# 15. Checkpoint 00:45

À ce stade, viser :

```text
[ ] projet Python démarre
[ ] env vars lues
[ ] API locale répond
[ ] curl fonctionne
[ ] artefact joblib lisible si nécessaire
```

Si ce n’est pas le cas :

```text
ne pas ajouter de complexité
```

---

# 16. T2 — 00:45 à 01:10
# Pytest et validation locale

## Attendu source

Le support annonce :

```text
Pytest
```

## Stratégie proposée

Créer rapidement les tests les plus rentables :

```text
health
payload valide
payload invalide
artefact/config si nécessaire
```

---

# 17. Matrice minimale de tests

```text
GET /health
→ 200

POST valide
→ succès

POST invalide
→ erreur contrôlée

route / ressource critique
→ comportement attendu
```

---

# 18. Lancer Pytest

```bash
pytest -v
```

Objectif :

```text
une baseline verte
```

avant Docker.

---

# 19. Ne pas viser la couverture parfaite

En 4 h, éviter :

```text
20 tests très détaillés
```

si :

```text
la pipeline principale n’existe pas encore
```

Préférer :

```text
quelques tests ciblés
+
fonctionnels
+
répétables
```

---

# 20. Checkpoint 01:10

```text
[ ] API locale OK
[ ] Pytest OK
[ ] fichiers principaux présents
[ ] premier commit/push effectué
```

---

# 21. T3 — 01:10 à 01:45
# Docker / Compose

## Attendu source

Le support annonce :

```text
Dockerfile
volumes
docker-compose.yml
services.depends_on
```

## Stratégie proposée

Ordre :

```text
Dockerfile
↓
docker build
↓
docker run
↓
docker-compose
```

Ne pas démarrer directement par un Compose complexe.

---

# 22. Dockerfile minimal d’abord

Objectif :

```text
une image qui démarre
```

avant toute optimisation.

Valider :

```bash
docker build \
  -t app .
```

---

# 23. Container seul

Puis :

```bash
docker run \
  --rm \
  -p 8000:8000 \
  app
```

Tester :

```bash
curl \
  http://localhost:8000/health
```

---

# 24. Compose ensuite

Ajouter progressivement :

```text
app
↓
prometheus
↓
grafana
```

ou les services demandés dans le sujet.

---

# 25. `depends_on`

Si le sujet exige cette clé :

```yaml
depends_on:
  - app
```

ou selon les services réels.

Toujours vérifier :

```text
indentation
nom exact du service
```

---

# 26. Volume

Si demandé :

```text
monter un volume
```

et valider réellement la persistance ou le montage.

Ne pas considérer un YAML écrit comme terminé tant qu’il n’a pas été testé.

---

# 27. Checkpoint 01:45

```text
[ ] docker build OK
[ ] container démarre
[ ] API répond dans Docker
[ ] Compose syntaxiquement valide
[ ] services critiques démarrent
```

---

# 28. T4 — 01:45 à 02:20
# GitLab CI / Runner / DockerHub

## Attendu source

Le support annonce :

```text
Repository
.gitlab-ci.yml
Runner via gitlab-runner
```

et demande avant l’examen :

```text
Runner shell
nommé shell
```

---

# 29. Pipeline minimal avant pipeline ambitieux

Commencer :

```yaml
stages:
  - test

tests:
  stage: test
  script:
    - pytest -v
```

Valider que :

```text
Runner exécute réellement le job
```

---

# 30. Runner pending

Si le job reste en attente :

```text
ne pas toucher au code applicatif
```

Vérifier :

```text
Runner online
association projet
tags éventuels
executor shell
```

---

# 31. Ajouter Docker seulement après

Quand :

```text
pytest CI
=
vert
```

ajouter :

```text
docker build
```

---

# 32. DockerHub

## Attendu source

Le support demande de préparer :

```text
compte DockerHub
Personal Access Token
```

## Stratégie proposée

Si le sujet implique un registry :

```text
build
↓
tag
↓
login
↓
push
```

---

# 33. Ne pas exposer le token

Éviter :

```text
token en clair dans .gitlab-ci.yml
```

Préférer le mécanisme de variable CI si le sujet l’autorise ou l’attend.

---

# 34. Checkpoint 02:20

```text
[ ] pipeline déclenché
[ ] Runner shell exécute
[ ] tests passent en CI
[ ] Docker build passe
[ ] image publiée si demandé
```

---

# 35. T5 — 02:20 à 03:05
# Kubernetes

## Attendu source

Le support annonce :

```text
Namespace
PV
PVC
ConfigMap
Service
Deployment
```

## Stratégie proposée

Créer les manifests dans cet ordre logique :

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

selon ce que demande le vrai sujet.

---

# 36. Namespace d’abord

Valider :

```bash
kubectl get namespaces
```

---

# 37. ConfigMap

Valider :

```bash
kubectl get configmaps \
  -n <namespace>
```

---

# 38. PV / PVC

Valider :

```bash
kubectl get pv
kubectl get pvc \
  -n <namespace>
```

Objectif :

```text
PVC = Bound
```

si un stockage est requis.

---

# 39. Deployment

Après application :

```bash
kubectl get deployments \
  -n <namespace>
```

puis :

```bash
kubectl get pods \
  -n <namespace>
```

---

# 40. Pod non Running

Ne pas aller au Service tant que :

```text
Pod
≠
Running
```

Debug :

```bash
kubectl describe pod ...
kubectl logs ...
```

---

# 41. Service

Valider :

```bash
kubectl get services \
  -n <namespace>
```

Puis vérifier :

```text
selector du Service
=
labels des Pods
```

---

# 42. Test Kubernetes

Pattern de practice :

```bash
kubectl port-forward \
  service/<service> \
  8000:8000 \
  -n <namespace>
```

Puis :

```bash
curl \
  http://localhost:8000/health
```

---

# 43. Checkpoint 03:05

```text
[ ] namespace OK
[ ] configmap OK
[ ] PVC Bound si nécessaire
[ ] deployment Ready
[ ] pods Running
[ ] service OK
[ ] API joignable
```

---

# 44. T6 — 03:05 à 03:35
# Prometheus / PromQL

## Attendu source

Le support annonce :

```text
prometheus-fastapi-instrumentator
config/prometheus.yml
PromQL
```

---

# 45. Commencer par `/metrics`

Avant toute configuration Prometheus :

```bash
curl \
  http://localhost:8000/metrics
```

Si ce test échoue :

```text
ne pas configurer Grafana
```

---

# 46. Config Prometheus

Créer ou corriger :

```text
config/prometheus.yml
```

Puis vérifier la target.

Objectif :

```text
UP
```

---

# 47. Target DOWN

Check rapide :

```text
hostname
port
/metrics
réseau
prometheus.yml
```

---

# 48. PromQL

Ne pas inventer :

```text
les noms de métriques
```

Faire d’abord :

```text
/metrics
ou
Prometheus UI
```

Puis requêtes simples :

```promql
metric_name
```

puis :

```promql
rate(
  metric_name[5m]
)
```

si adapté.

---

# 49. Checkpoint 03:35

```text
[ ] /metrics accessible
[ ] target Prometheus UP
[ ] au moins une requête PromQL valide
```

---

# 50. T7 — 03:35 à 03:50
# Grafana

## Attendu source

Le support annonce :

```text
datasources/<source_name>.yml
dashboard depuis l’UI
```

## Stratégie proposée

Objectif minimal :

```text
datasource OK
+
1 dashboard
+
1 ou quelques panels fonctionnels
```

selon le sujet réel.

---

# 51. Valider la datasource avant le dashboard

Ordre :

```text
Prometheus UP
↓
datasource Grafana OK
↓
dashboard
```

Ne pas passer 10 minutes sur un panel si :

```text
la datasource ne fonctionne pas
```

---

# 52. Panel simple d’abord

Utiliser :

```text
une métrique réellement disponible
```

et une requête PromQL déjà validée dans Prometheus.

---

# 53. Checkpoint 03:50

```text
[ ] datasource fonctionne
[ ] dashboard créé si demandé
[ ] au moins un panel retourne des données
```

---

# 54. T8 — 03:50 à 04:00
# Validation finale / archive / upload

## Attendu source

Le rendu doit être uploadé sous forme d’archive.

## Stratégie proposée

À partir de :

```text
03:50
```

interdiction de démarrer :

```text
une nouvelle fonctionnalité
```

---

# 55. Validation finale

Checklist :

```text
[ ] fichiers présents
[ ] noms corrects
[ ] secrets retirés
[ ] artefacts utiles inclus
[ ] fichiers temporaires inutiles supprimés
[ ] README ou notes à jour
```

---

# 56. Vérifier Git

```bash
git status
```

S’assurer que :

```text
les fichiers utiles ne sont pas oubliés
```

---

# 57. Vérifier Pytest

Si rapide :

```bash
pytest -q
```

---

# 58. Vérifier Compose

```bash
docker compose ps
```

---

# 59. Vérifier Kubernetes

```bash
kubectl get pods \
  -n <namespace>
```

---

# 60. Vérifier l’observabilité

```text
Prometheus
→ target UP

Grafana
→ datasource OK
```

si ces éléments font partie du sujet réel.

---

# 61. Archive

Pattern :

```bash
zip -r \
  bloc3_submission.zip \
  project/
```

ou l’outil imposé / disponible.

Vérifier :

```bash
unzip -l \
  bloc3_submission.zip
```

> La commande exacte d’archivage n’est pas donnée dans la page source ; le support exige seulement l’upload d’une archive.

---

# 62. Ne pas archiver inutilement

Éviter si non nécessaire :

```text
.venv/
.git/
caches
images Docker
fichiers temporaires
```

Le contenu exact à inclure doit suivre le sujet réel.

---

# 63. Upload

Ne pas attendre :

```text
03:59:50
```

pour commencer l’upload.

But :

```text
archive prête
↓
upload
↓
validation
```

---

# 64. Stratégie anti-tunnel

## Règle proposée

Si un problème bloque plus de :

```text
10 à 15 minutes
```

faire :

```text
1. lire logs
2. isoler
3. simplifier
4. documenter
5. passer à la suite si nécessaire
```

---

# 65. Principe de simplification

Si une architecture complexe échoue :

```text
réduire
```

Exemple :

```text
3 services
→ 1 service
```

pour valider le composant critique,
puis reconstruire progressivement.

---

# 66. Debug par couche

Toujours diagnostiquer :

```text
LOCAL
↓
DOCKER
↓
CI
↓
KUBERNETES
↓
PROMETHEUS
↓
GRAFANA
```

Ne pas déboguer Grafana si :

```text
FastAPI ne démarre pas
```

---

# 67. Ordre de résolution d’erreur

```text
1. erreur la plus basse dans la stack
2. dépendance suivante
3. intégration
```

Exemple :

```text
FastAPI KO
→ corriger FastAPI

Docker KO
→ corriger Docker

K8s KO
→ corriger K8s
```

---

# 68. Logs avant intuition

Réflexe :

```text
voir la preuve
avant
de modifier au hasard
```

Commandes utiles :

```bash
docker logs
docker compose logs
kubectl logs
kubectl describe
```

---

# 69. Ne pas réécrire ce qui fonctionne

Si :

```text
FastAPI local
=
OK
```

et :

```text
Docker
=
KO
```

ne pas réécrire l’API.

Chercher d’abord :

```text
Dockerfile
ports
paths
env vars
```

---

# 70. Priorisation proposée

## P0 — cœur fonctionnel

```text
application
tests
Docker
```

## P1 — automatisation / déploiement

```text
GitLab CI
Runner
Kubernetes
```

## P2 — observabilité

```text
Prometheus
Grafana
```

> Cette hiérarchie est une stratégie proposée. Le vrai sujet peut imposer un autre ordre.

---

# 71. Ce qu’il faut éviter pendant l’épreuve

```text
refactor esthétique long
optimisation prématurée
architecture trop complexe
documentation excessive
débogage sans logs
changement de plusieurs couches à la fois
```

---

# 72. Ce qu’il faut privilégier

```text
fonctionnel
simple
testable
reproductible
lisible
```

---

# 73. Stratégie Git

Commits proposés :

```text
chore: bootstrap project
feat: add fastapi app
test: add pytest suite
build: add docker
ci: add gitlab pipeline
ops: add kubernetes manifests
obs: add prometheus grafana
```

> Les messages sont des exemples de pratique, pas des exigences.

---

# 74. Push régulier

Faire des push à des jalons :

```text
API OK
tests OK
Docker OK
CI OK
K8s OK
```

Cela réduit le risque de :

```text
tout perdre
ou
découvrir tard un problème GitLab
```

---

# 75. Matrice temps / preuve

À chaque bloc, chercher une preuve :

| Bloc | Preuve minimale |
|---|---|
| Bash/env | `echo` / valeur Python |
| FastAPI | `curl` |
| Pytest | `pytest -v` |
| Docker | `docker run` + `curl` |
| GitLab CI | pipeline vert |
| DockerHub | image présente si demandé |
| Kubernetes | Pod `Running` + Service |
| Prometheus | target `UP` |
| PromQL | requête retourne des données |
| Grafana | panel visible |

---

# 76. Checkpoints obligatoires proposés

## 00:45

```text
API locale OK
```

## 01:10

```text
tests OK
```

## 01:45

```text
Docker OK
```

## 02:20

```text
CI OK
```

## 03:05

```text
Kubernetes OK
```

## 03:35

```text
Prometheus OK
```

## 03:50

```text
Grafana / rendu final
```

---

# 77. Si vous êtes en retard à 02:20

Supposons :

```text
Docker pas encore stable
```

Alors :

```text
ne pas ouvrir Kubernetes immédiatement
```

Il vaut mieux avoir :

```text
Docker fonctionnel
+
CI fonctionnelle
```

que :

```text
Docker cassé
+
Kubernetes à moitié écrit
```

---

# 78. Si vous êtes en retard à 03:05

Si Kubernetes bloque encore :

```text
documenter l’état
sécuriser les manifests
passer à Prometheus
```

uniquement si Prometheus peut être traité indépendamment dans le sujet.

---

# 79. Si vous êtes en retard à 03:35

Ne plus chercher à perfectionner :

```text
PromQL
Grafana
```

Faire :

```text
1 requête valide
1 panel valide
```

si cela satisfait le sujet.

---

# 80. Si vous êtes en retard à 03:50

STOP.

Faire uniquement :

```text
validation
archive
upload
```

---

# 81. Préparation la veille

## Source + stratégie

Le support demande notamment avant l’examen :

```text
repository GitLab privé
clé SSH
Runner shell
compte DockerHub
token DockerHub
```

Ajouter comme vérification de préparation :

```text
[ ] VM propre
[ ] Git OK
[ ] Python OK
[ ] Docker OK
[ ] Runner online
[ ] DockerHub login testé
```

---

# 82. Préparation VM

## Attendu source

Le support indique d’utiliser la même VM que le Bloc 2 et recommande de nettoyer les anciens éléments.

## Checklist

```text
[ ] anciens dossiers supprimés si inutiles
[ ] anciens containers arrêtés/supprimés
[ ] ports libérés
[ ] espace disque disponible
```

---

# 83. Commandes de contrôle pré-examen

```bash
python --version
git --version
docker --version
docker compose version
gitlab-runner --version
```

Puis :

```bash
gitlab-runner list
```

---

# 84. Test GitLab pré-examen

Créer / conserver un pipeline de practice :

```yaml
hello:
  script:
    - echo "Runner OK"
```

Objectif avant l’épreuve :

```text
pipeline vert
```

---

# 85. Test DockerHub pré-examen

Faire au moins une fois :

```text
login
tag
push
```

avant l’épreuve.

---

# 86. Réflexe pendant Mereos

## Attendu source

L’examen est surveillé.

Respecter les consignes affichées dans l’environnement d’examen et éviter toute action qui entre en conflit avec la surveillance ou les règles de l’épreuve.

---

# 87. Stratégie de navigation

Éviter de multiplier :

```text
20 terminaux
10 éditeurs
15 onglets
```

Organisation simple :

```text
Terminal 1
→ app / tests

Terminal 2
→ Docker / kubectl

Browser
→ GitLab / Prometheus / Grafana / exam
```

---

# 88. Nommer clairement les fichiers

Préférer :

```text
deployment.yml
service.yml
prometheus.yml
```

à :

```text
test1.yml
final2.yml
new_final.yml
```

---

# 89. README minimal

Si le sujet demande une explication ou si cela aide au rendu :

```text
run local
run tests
run docker
run compose
deploy k8s
monitoring
```

Ne pas transformer le README en dissertation.

---

# 90. Résumé de la stratégie

```text
0:00
LIRE

0:15
CODER MINIMAL

0:45
TESTER

1:10
DOCKERISER

1:45
AUTOMATISER

2:20
DEPLOYER

3:05
MONITORER

3:35
VISUALISER

3:50
STOP DEV

4:00
RENDU ENVOYÉ
```

---

# 91. Mantra d’examen

```text
Faire simple.
Faire fonctionner.
Prouver.
Passer à la suite.
```

---

# 92. Document suivant

```text
13_RNCP_38919_BLOC_3_CHECKLIST_JOUR_J.md
```

Objectif :

> condenser toute la préparation en une checklist opérationnelle
> utilisable avant le lancement, pendant les 4 heures et juste avant l’upload final.
