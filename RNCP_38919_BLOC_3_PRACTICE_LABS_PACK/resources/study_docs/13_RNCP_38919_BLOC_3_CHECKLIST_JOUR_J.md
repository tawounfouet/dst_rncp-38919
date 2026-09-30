# 13 — RNCP 38919 — Bloc 3
# Checklist Jour J

**Certification :** RNCP 38919 — Data Engineer  
**Sprint :** Sprint 19 — Préparation RNCP 38919  
**Épreuve :** Bloc 3 — Data Engineer / DevOps  
**Durée officielle :** 4 heures

**Source principale :**
- `Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md`

> **Convention**
>
> - **Attendu source** : élément explicitement annoncé dans le support DataScientest.
> - **Checklist proposée** : organisation pratique construite à partir du périmètre annoncé.
>
> La source fixe notamment :
>
> ```text
> 4 heures
> Mereos
> Google Chrome
> archive à uploader
> même VM que pour le Bloc 2
> nettoyage préalable recommandé
> repository GitLab privé dst_rncp38919_bloc_3
> clé SSH GitLab
> Runner shell nommé shell
> compte DockerHub
> Personal Access Token DockerHub
> ```
>
> Les étapes minute par minute et critères de validation ci-dessous sont des **repères de préparation proposés**.

---

# 1. La veille / avant le lancement

## GitLab — attendu source

```text
[ ] compte GitLab accessible
[ ] repository privé créé
[ ] nom exact : dst_rncp38919_bloc_3
[ ] clé SSH créée sur la VM
[ ] clé publique ajoutée à GitLab
[ ] Runner créé
[ ] type : shell
[ ] nom : shell
[ ] Runner enregistré sur la VM
```

---

# 2. DockerHub — attendu source

```text
[ ] compte DockerHub accessible
[ ] Personal Access Token généré
```

## Vérifications proposées

```text
[ ] docker login déjà testé
[ ] push d’une image de practice déjà testé
```

---

# 3. VM — attendu source

Le support recommande de repartir sur un environnement propre.

Checklist :

```text
[ ] anciens fichiers inutiles supprimés
[ ] anciens dossiers inutiles supprimés
[ ] anciens containers Docker arrêtés / supprimés
[ ] ports libérés
[ ] espace disque suffisant
```

---

# 4. Outils — vérification rapide

## Checklist proposée

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

# 5. Navigateur et surveillance — attendu source

```text
[ ] Google Chrome utilisé
[ ] Mereos opérationnel
[ ] consignes de surveillance relues
[ ] environnement conforme avant démarrage
```

---

# 6. Démarrage de l’épreuve — 00:00

## Checklist proposée

```text
[ ] lire le sujet en entier
[ ] repérer les livrables
[ ] repérer les noms de fichiers imposés
[ ] repérer les commandes / objets explicitement demandés
[ ] repérer les dépendances entre étapes
[ ] repérer les éléments pouvant être faits en parallèle
```

---

# 7. Construire la todo du sujet

Créer une liste très courte :

```text
[ ] Bash / env
[ ] Python / HTTP
[ ] joblib
[ ] FastAPI / Pydantic
[ ] Pytest
[ ] GitLab CI
[ ] Docker / Compose
[ ] DockerHub
[ ] Kubernetes
[ ] Prometheus / PromQL
[ ] Grafana
[ ] archive finale
```

Puis adapter au vrai sujet.

---

# 8. Créer l’arborescence

## Checklist proposée

```text
[ ] app/
[ ] tests/
[ ] config/
[ ] k8s/
[ ] grafana/
[ ] Dockerfile
[ ] docker-compose.yml
[ ] .gitlab-ci.yml
[ ] README.md si utile
```

Uniquement les dossiers réellement nécessaires au sujet.

---

# 9. Bash / environnement

## Attendu source

Le support annonce :

```text
export
.bashrc
variables d’environnement Python
```

## Checklist proposée

```text
[ ] variables nécessaires identifiées
[ ] export effectué si nécessaire
[ ] .bashrc modifié uniquement si demandé
[ ] valeurs vérifiées avec echo
[ ] lecture Python testée avec os.getenv
```

---

# 10. Environnement Python

## Attendu source

```text
environnement virtuel Python
```

## Checklist

```text
[ ] venv créé
[ ] venv activé
[ ] dépendances installées
[ ] Python actif vérifié
```

Commandes :

```bash
python -m venv .venv
source .venv/bin/activate
which python
```

---

# 11. HTTP

## Attendu source

```text
requêtes HTTP en Bash
requêtes HTTP en Python
curl
```

## Checklist

```text
[ ] URL correcte
[ ] méthode correcte
[ ] headers corrects
[ ] payload valide
[ ] status code vérifié
```

---

# 12. `joblib`

## Attendu source

```text
sauvegarde de modèles / objets data science
```

## Checklist proposée

```text
[ ] fichier existe
[ ] chemin correct
[ ] joblib.load fonctionne
[ ] variable MODEL_PATH correcte si utilisée
```

---

# 13. FastAPI / Pydantic

## Attendu source

```text
FastAPI
pydantic.BaseModel
```

## Checklist

```text
[ ] app démarre
[ ] endpoint principal répond
[ ] BaseModel défini
[ ] payload valide accepté
[ ] payload invalide géré
```

---

# 14. Validation manuelle FastAPI

```text
[ ] GET testé avec curl
[ ] POST testé avec curl
[ ] status code contrôlé
[ ] JSON de réponse contrôlé
```

Exemple de practice :

```bash
curl \
  http://localhost:8000/health
```

---

# 15. Pytest

## Attendu source

```text
Pytest
```

## Checklist

```text
[ ] tests/ présent
[ ] fichiers test_*.py
[ ] au moins un test nominal
[ ] au moins un test d’erreur si pertinent
[ ] pytest -v passe
```

---

# 16. Checkpoint proposé — 01:10

À ce moment viser :

```text
[ ] Python OK
[ ] API OK
[ ] curl OK
[ ] Pytest OK
```

---

# 17. Dockerfile

## Attendu source

```text
Dockerfile
```

## Checklist

```text
[ ] FROM
[ ] WORKDIR
[ ] COPY
[ ] RUN
[ ] CMD / commande de démarrage
[ ] build OK
```

---

# 18. Docker build

```text
[ ] image construite
[ ] tag correct
```

Commande de practice :

```bash
docker build \
  -t app .
```

---

# 19. Docker run

```text
[ ] container démarre
[ ] port publié
[ ] logs propres
[ ] API joignable
```

---

# 20. Volumes

## Attendu source

```text
volumes
```

## Checklist

```text
[ ] volume déclaré si demandé
[ ] chemin host / container correct
[ ] données visibles dans le container
```

---

# 21. Docker Compose

## Attendu source

```text
docker-compose.yml
services.depends_on
```

## Checklist

```text
[ ] services bien indentés
[ ] noms de services cohérents
[ ] ports cohérents
[ ] volumes cohérents
[ ] depends_on présent si demandé
[ ] docker compose up fonctionne
```

---

# 22. Diagnostic Docker

```bash
docker ps
docker ps -a
docker logs <container>
docker compose ps
docker compose logs
```

---

# 23. Checkpoint proposé — 01:45

```text
[ ] Dockerfile OK
[ ] docker build OK
[ ] docker run OK
[ ] Compose OK
```

---

# 24. GitLab

## Attendu source

```text
Repository
.gitlab-ci.yml
Runner
```

## Checklist

```text
[ ] repository correct
[ ] branche correcte
[ ] remote correct
[ ] premier push effectué
[ ] .gitlab-ci.yml présent
```

---

# 25. Runner

## Attendu source

```text
Runner type shell
nom shell
```

## Checklist

```text
[ ] Runner online
[ ] Runner associé au projet
[ ] job non bloqué en pending
[ ] commandes exécutées sur la VM
```

---

# 26. Pipeline GitLab

## Checklist proposée

```text
[ ] pipeline déclenché
[ ] job de test passe
[ ] job de build passe si demandé
[ ] logs relus
```

---

# 27. Si le job reste `pending`

```text
[ ] Runner online ?
[ ] Runner associé ?
[ ] tags compatibles ?
[ ] Runner paused ?
```

---

# 28. DockerHub

## Attendu source

```text
compte
Personal Access Token
```

## Checklist proposée si le sujet demande une image registry

```text
[ ] login
[ ] tag
[ ] push
[ ] repository DockerHub vérifié
```

---

# 29. Checkpoint proposé — 02:20

```text
[ ] pipeline CI fonctionne
[ ] Runner shell fonctionne
[ ] image buildée
[ ] image poussée si demandé
```

---

# 30. Kubernetes

## Attendu source

Le support annonce :

```text
Namespace
PersistentVolume
PersistentVolumeClaim
ConfigMap
Service
Deployment
```

---

# 31. Namespace

```text
[ ] Namespace créé
[ ] nom cohérent
```

Vérifier :

```bash
kubectl get namespaces
```

---

# 32. ConfigMap

```text
[ ] ConfigMap créée
[ ] clés correctes
[ ] namespace correct
[ ] injection dans le Pod correcte
```

---

# 33. PV

```text
[ ] PersistentVolume créé si demandé
[ ] capacité correcte
[ ] access mode cohérent
```

---

# 34. PVC

```text
[ ] PersistentVolumeClaim créé
[ ] namespace correct
[ ] storage demandé cohérent
[ ] STATUS = Bound si applicable
```

---

# 35. Deployment

```text
[ ] image correcte
[ ] tag correct
[ ] replicas cohérents
[ ] selector correct
[ ] template labels corrects
[ ] ports corrects
[ ] ConfigMap injectée
[ ] PVC monté si demandé
```

---

# 36. Règle critique Deployment

Toujours vérifier :

```text
selector.matchLabels
=
template.metadata.labels
```

---

# 37. Service

```text
[ ] Service créé
[ ] selector correct
[ ] port correct
[ ] targetPort correct
```

Règle :

```text
Service selector
=
Pod labels
```

---

# 38. Vérifier Kubernetes

```bash
kubectl get pods \
  -n <namespace>

kubectl get deployments \
  -n <namespace>

kubectl get services \
  -n <namespace>

kubectl get pvc \
  -n <namespace>

kubectl get pv
```

---

# 39. Si Pod non `Running`

```bash
kubectl describe pod \
  <pod> \
  -n <namespace>

kubectl logs \
  <pod> \
  -n <namespace>
```

---

# 40. Checkpoint proposé — 03:05

```text
[ ] Pod Running
[ ] Deployment Ready
[ ] Service présent
[ ] PVC Bound si nécessaire
[ ] application joignable
```

---

# 41. Prometheus

## Attendu source

```text
prometheus-fastapi-instrumentator
config/prometheus.yml
PromQL
```

---

# 42. Instrumentation FastAPI

```text
[ ] Instrumentator ajouté
[ ] /metrics accessible
```

Tester :

```bash
curl \
  http://localhost:8000/metrics
```

---

# 43. `prometheus.yml`

```text
[ ] fichier au bon emplacement
[ ] YAML valide
[ ] job_name présent
[ ] target correcte
[ ] hostname correct
[ ] port correct
```

---

# 44. Target Prometheus

```text
[ ] target visible
[ ] STATUS = UP
```

Si `DOWN` :

```text
[ ] /metrics accessible ?
[ ] hostname ?
[ ] port ?
[ ] réseau ?
[ ] YAML ?
```

---

# 45. PromQL

## Checklist

```text
[ ] métrique réellement existante
[ ] labels réellement existants
[ ] requête simple fonctionne
[ ] rate utilisé seulement si pertinent
[ ] agrégation fonctionne si demandée
```

---

# 46. Checkpoint proposé — 03:35

```text
[ ] /metrics OK
[ ] Prometheus target UP
[ ] requête PromQL valide
```

---

# 47. Grafana

## Attendu source

```text
datasources/<source_name>.yml
dashboard depuis l’UI
```

---

# 48. Datasource Grafana

```text
[ ] YAML présent
[ ] type = prometheus
[ ] URL correcte
[ ] Grafana peut joindre Prometheus
```

---

# 49. Piège Docker Grafana

Si containerisé :

```text
localhost:9090
```

peut être incorrect.

Vérifier le hostname réel du service Prometheus.

---

# 50. Dashboard

```text
[ ] dashboard créé dans l’UI si demandé
[ ] datasource sélectionnée
[ ] PromQL valide
[ ] panel affiche des données
[ ] titre clair
```

---

# 51. Checkpoint proposé — 03:50

```text
[ ] datasource Grafana OK
[ ] dashboard / panel fonctionnel si demandé
```

À partir de ce moment :

```text
STOP NOUVELLE FONCTIONNALITÉ
```

---

# 52. Validation finale

## Checklist proposée

```text
[ ] tous les fichiers demandés sont présents
[ ] noms de fichiers corrects
[ ] YAML lisibles
[ ] code Python syntaxiquement valide
[ ] tests exécutés
[ ] README / notes utiles à jour
[ ] aucun secret inutile dans les fichiers
```

---

# 53. Vérifier Git

```bash
git status
```

Checklist :

```text
[ ] aucun fichier critique oublié
[ ] dernier commit effectué si nécessaire
[ ] dernier push effectué
```

---

# 54. Vérifier les tests

Si le temps le permet :

```bash
pytest -q
```

---

# 55. Vérifier Docker

```bash
docker compose ps
```

---

# 56. Vérifier Kubernetes

```bash
kubectl get pods \
  -n <namespace>
```

---

# 57. Vérifier Prometheus

```text
[ ] target UP
```

---

# 58. Vérifier Grafana

```text
[ ] datasource OK
[ ] panel affiche des données
```

---

# 59. Archive finale

## Attendu source

Le rendu doit être uploadé sous forme d’archive.

## Checklist proposée

```text
[ ] archive créée
[ ] nom explicite
[ ] contenu vérifié
[ ] pas de .venv inutile
[ ] pas de .git inutile
[ ] pas de cache inutile
[ ] fichiers demandés présents
```

---

# 60. Vérifier l’archive

Pattern :

```bash
unzip -l \
  bloc3_submission.zip
```

---

# 61. Upload final

```text
[ ] archive sélectionnée
[ ] upload démarré avant la dernière minute
[ ] upload terminé
[ ] confirmation visible
```

---

# 62. Règle anti-tunnel

Si un bug prend plus de :

```text
10–15 minutes
```

faire :

```text
[ ] lire les logs
[ ] isoler la couche
[ ] simplifier
[ ] documenter l’état
[ ] passer à la suite si nécessaire
```

---

# 63. Ordre de debug

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

Ne pas déboguer une couche haute si la couche basse est cassée.

---

# 64. Preuves minimales à chercher

| Brique | Preuve |
|---|---|
| env | valeur visible |
| Python | script démarre |
| FastAPI | `curl` répond |
| Pytest | tests verts |
| Docker | container actif |
| Compose | services `Up` |
| GitLab CI | pipeline vert |
| DockerHub | image présente si demandée |
| Kubernetes | Pod `Running` |
| Service | API joignable |
| Prometheus | target `UP` |
| PromQL | résultat |
| Grafana | panel avec données |

---

# 65. Commandes flash

```bash
echo $VAR

python -m venv .venv
source .venv/bin/activate

pytest -v

curl URL

docker build -t app .
docker ps
docker logs <container>

docker compose up -d
docker compose ps
docker compose logs

git status
git push

gitlab-runner list

kubectl get pods
kubectl describe pod <pod>
kubectl logs <pod>
```

---

# 66. Questions à se poser avant chaque étape

```text
Qu’est-ce qui est demandé ?
Quelle preuve valide cette étape ?
De quoi dépend-elle ?
Puis-je la tester maintenant ?
Combien de temps suis-je prêt à perdre dessus ?
```

---

# 67. Si je suis en retard

## À 02:20

```text
priorité :
application
tests
Docker
CI
```

## À 03:05

```text
sécuriser Kubernetes
puis observabilité minimale
```

## À 03:35

```text
1 requête PromQL valide
1 panel valide si demandé
```

## À 03:50

```text
STOP DEV
ARCHIVE
UPLOAD
```

---

# 68. Check final ultra-court

```text
[ ] CODE
[ ] TEST
[ ] CI
[ ] DOCKER
[ ] K8S
[ ] METRICS
[ ] DASHBOARD
[ ] ARCHIVE
[ ] UPLOAD
```

À adapter au sujet réel.

---

# 69. Mantra Jour J

```text
Lire.
Construire petit.
Tester.
Prouver.
Passer à la suite.
Archiver.
Uploader.
```

---

# 70. Document suivant

```text
14_RNCP_38919_BLOC_3_EXAMEN_BLANC_01.md
```

Objectif :

> simuler une épreuve complète de 4 heures,
> avec un scénario DevOps fictif mais strictement construit
> autour des compétences annoncées par le support DataScientest.
