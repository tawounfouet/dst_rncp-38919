# 07 — Runbook Exhaustive : de la validation locale au pipeline GitLab Runner Shell
## Procédure complète, vérifiée, de A à Z

Ce guide est le **runbook opératoire** du projet ParcelPulse. Contrairement aux guides 01 à 06 qui expliquent des notions, celui-ci donne la procédure **exacte, testée et reproductible** pour valider le projet de bout en bout :

- **Partie A** — validation **locale** (macOS, sans infrastructure) ;
- **Partie B** — validation sur l'infrastructure **AWS** avec le runner `shell` (**chemin officiel de l'examen**) ;
- **Partie C** — annexe : le runner Kubernetes et le piège `privileged` de Docker-in-Docker, démontré expérimentalement (**hors sujet de l'examen**).

> Toutes les commandes de ce guide ont été **exécutées et vérifiées**. Les sorties attendues sont recopiées depuis les exécutions réelles, pas inventées.
> Les sections marquées ⚠️ signalent un comportement qui trompe les débutants.

---

## Sommaire

| Partie | Contenu |
|---|---|
| [0](#0--checklist-de-validation) | Checklist de validation |
| [1](#1--prérequis) | Prérequis et versions vérifiées |
| [2](#2--partie-a--validation-locale) | Partie A — Validation locale |
| [3](#3--partie-b--infrastructure-aws--runner-shell) | Partie B — Infrastructure AWS / Runner `shell` |
| [4](#4--partie-c--annexe--le-runner-kubernetes-et-le-piège-docker-in-docker) | Partie C — Annexe : runner Kubernetes et `privileged` |
| [5](#5--dépannage--tableau-des-symptômes) | Dépannage : tableau des symptômes |
| [6](#6--sécurité--ce-quil-ne-faut-jamais-faire) | Sécurité |
| [7](#7--limites--ce-qui-na-pas-pu-être-vérifié) | Limites |

---

## 0. Checklist de validation

| # | Étape | Attendu | Statut |
|---|---|---|---|
| A1 | Environnement + artefact + tests | `12 passed` | ✅ vérifié |
| A2 | Image Docker | `Import OK: parcelpulse-api` | ✅ vérifié |
| A3 | Compose + Prometheus + Grafana | target `app:8000` **up** | ✅ vérifié |
| A4 | Kubernetes local (kind) | pod `1/1 Running`, PVC `Bound` | ✅ vérifié |
| A5 | Smoke test HTTP | `11 verifications reussies` | ✅ vérifié |
| A6 | Validateur du pack | 6 phases ✅ | ✅ vérifié |
| B1 | Diagnostic de la VM | MicroK8s + runner `shell` actif | ✅ vérifié |
| B2 | Job `tests` isolé | `12 passed` sur Python 3.12 | ✅ vérifié |
| B3 | Job `docker_build` isolé | build + import OK | ✅ vérifié |
| B4 | Projet GitLab créé | dépôt vierge | ✅ vérifié |
| B5 | Push + runner activé | **pipeline vert sur le runner `shell`** | ✅ vérifié |
| B6 | Pipeline réellement exécuté par la VM | `on shell 57rYfgq8b` | ✅ vérifié |
| B7 | Publication DockerHub | `digest: sha256:5c559c5c…` + pull anonyme OK | ✅ vérifié |
| B8 | Déploiement sur le cluster AWS (MicroK8s) | pod `1/1`, PVC `Bound`, smoke **11/11** | ✅ vérifié |
| C1 | Diagnostic `privileged` (annexe) | crash sans, OK avec | ✅ vérifié |

---

## 1. Prérequis

### Versions utilisées et vérifiées

| Composant | Version vérifiée | Comment vérifier |
|---|---|---|
| Docker Desktop | 28.2.2 | `docker info --format '{{.ServerVersion}}'` |
| kind | v0.32.0 | `kind version` |
| Node kind | v1.36.1 | `docker images | grep kindest` |
| Python (local) | 3.13.12 | `.venv/bin/python -V` |
| Python (CI) | 3.12.15 | image `python:3.12-slim` |
| VM AWS | Ubuntu 22.04.5 LTS, kernel 6.8.0-1021-aws | `lsb_release -a` |
| Cluster distant | MicroK8s, Kubernetes **v1.30.14** | `microk8s status` |
| Runner | chart `gitlab-runner-0.93.0`, runner `19.4.0` | `helm list -A` |
| Registre | `https://gitlab.com/` | `.gitlab-ci.yml` du runner |

### Connexion à la VM

```bash
cd /chemin/vers/RNCP_38919_BLOC_3_PRACTICE_LABS_PACK
chmod 400 data_enginering_machine.pem
ssh -i "./data_enginering_machine.pem" ubuntu@52.31.224.223
```

> ⚠️ **`kubectl` n'est pas dans le `PATH` par défaut sur cette VM.** Le binaire vit dans le snap MicroK8s et l'utilisateur a un alias :
> ```bash
> # /home/ubuntu/.bashrc:118
> alias k="microk8s kubectl"
> export KUBECONFIG="$HOME/.kube/config"
> ```
> Conséquence pratique : un script distant lancé via `ssh 'bash -s'` (shell **non interactif**) ne charge pas `.bashrc`, donc `kubectl` et les alias sont absents. Pour scripter à distance :
> ```bash
> export KUBECONFIG="$HOME/.kube/config"
> K="/snap/microk8s/current/kubectl"
> $K get nodes
> ```

---

## 2. Partie A — Validation locale

Toutes les commandes se lancent depuis `exam/correction/reference_project/`.

### A0. Positionnement

```bash
cd ~/workspace/learning/datascientest/RNCP/RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/exam/correction/reference_project
```

### A1. Environnement, artefact ML et tests unitaires

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/create_artifact.py
python -m pytest -v
```

**Sortie attendue :**
```text
Artifact created: .../models/model.joblib
12 passed, 1 warning in 0.46s
```

Les 12 tests couvrent : le seuil du modèle (risque 0, risque 1, seuil exact 20), la validation Pydantic (type invalide, champ manquant), les métriques Prometheus, et la résolution de `MODEL_PATH`.

> ⚠️ **`pip install` échoue dans le `.venv` si `pip` est configuré en installation utilisateur.** Sur cette machine, `pip config list` affiche :
> ```
> global.break-system-packages='true'
> global.user='true'
> ```
> Avec `global.user='true'`, `pip install -r requirements.txt` répond :
> ```
> ERROR: Can not perform a '--user' install. User site-packages are not visible in this virtualenv.
> ```
> et le `.venv` reste vide — `ModuleNotFoundError: No module named joblib` au moindre script. **Contournement :**
> ```bash
> PIP_USER=false python -m pip install -r requirements.txt
> ```
> ou, pour tout le pack : `python3 -m pip config unset global.user`. Le conteneur Docker et GitLab CI ne sont pas concernés : ils n'utilisent pas de venv.

> ⚠️ **`MODEL_PATH` doit être résolu en chemin absolu.** C'est un défaut corrigé dans ce projet : un chemin relatif (`models/model.joblib`) n'est interprété que depuis le répertoire courant. Conséquence avant correction : `pytest` lancé depuis n'importe quel autre dossier échouait sur `FileNotFoundError`. Le test `test_model_path_is_absolute` verrouille ce comportement.

### A2. Image Docker

```bash
docker build -t parcelpulse-api:latest .
docker run --rm parcelpulse-api:latest python -c "from app.main import app; print('Import OK:', app.title)"
```

**Sortie attendue :** `Import OK: parcelpulse-api`

### A3. Stack Compose : API + Prometheus + Grafana

```bash
docker compose up -d --build
sleep 15
docker compose ps
bash scripts/smoke_test.sh
```

Contrôle dans le navigateur :
- <http://localhost:8000/docs> — documentation FastAPI
- <http://localhost:9090/targets> — **la target `parcelpulse-api` doit être verte (`up`)**
- <http://localhost:3000> — Grafana (`admin` / `admin`)

Vérification de la chaîne Prometheus → Grafana :
```bash
curl -s -u admin:admin http://localhost:3000/api/datasources \
  | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['uid'])"   # Note l'uid
# puis (remplacer <UID>) :
curl -s -u admin:admin \
  "http://localhost:3000/api/datasources/proxy/uid/<UID>/api/v1/query?query=up"
```

> ⚠️ **Utiliser l'`uid`, pas l'`id` numérique** de la datasource. Avec l'id, l'API renvoie `{"message":"Unable to find datasource"}`.

> ⚠️ **`rate(...[1m])` ne renvoie rien pendant les ~30 premières secondes.** Prometheus scrappe toutes les 15 s et `rate()` a besoin d'au moins deux points dans la fenêtre. Attendez, ou utilisez `http_requests_total` (brut) qui répond immédiatement.

### A4. Kubernetes local avec kind

> ⚠️ **Obligatoire : arrêter Compose d'abord.** Compose publie le port 8000 en `*:8000`, le port-forward uniquement en `127.0.0.1:8000`. Les deux peuvent tourner simultanément et vous ne testez alors plus la stack que vous croyez tester.

```bash
docker compose down          # libère le port 8000
kind create cluster          # si ce n'est pas déjà fait
bash scripts/deploy_k8s.sh --smoke
```

**Sortie attendue :**
```text
==> 1/5  Contexte Kubernetes et accessibilite du cluster
Cluster joignable.
==> 2/5  Construction de l'image Docker (parcelpulse-api:latest)
==> 3/5  Chargement de l'image dans le cluster
==> 4/5  Application des manifests
namespace/parcelpulse created
configmap/parcelpulse-config created
deployment.apps/parcelpulse-api created
persistentvolume/parcelpulse-pv created
persistentvolumeclaim/parcelpulse-pvc created
service/parcelpulse-api-service created
==> 5/5  Attente du deploiement et etat du cluster
deployment "parcelpulse-api" successfully rolled out
pod/parcelpulse-api-XXXXX-YYYYY   1/1   Running   0   2s
persistentvolumeclaim/parcelpulse-pvc   Bound   parcelpulse-pv   1Gi   RWO   manual
==> Bonus  Smoke test automatise (tunnel temporaire)
Port local libre choisi : 57603
...
Smoke test OK - 11 verifications reussies
Deploiement ET smoke test valides.
```

#### Les cinq étapes de `deploy_k8s.sh` et pourquoi chacune est obligatoire

| Étape | Action | Raison |
|---|---|---|
| 1 | Vérifier que le cluster répond | Détecte un contexte Kubernetes mort |
| 2 | `docker build` | L'image doit exister |
| 3 | `kind load docker-image` / `minikube image load` | Le cluster **ne voit pas** les images de l'hôte |
| 4 | `namespace.yml` **puis** `-f k8s/` | Voir l'encadré ci-dessous |
| 5 | `rollout restart` + `rollout status` | Le tag `:latest` ne redéclenche pas de rollout |

> ⚠️ **L'ordre alphabétique de `kubectl apply -f <dossier>`.** Les fichiers sont traités par nom : `configmap.yml` et `deployment.yml` passent **avant** `namespace.yml`.
> ```
> Error from server (NotFound): error when creating "k8s/configmap.yml":
> namespaces "parcelpulse" not found
> ```
> Un second `kubectl apply -f k8s/` rattrape l'erreur, mais le déploiement n'est propre qu'en appliquant le namespace d'abord.

> ⚠️ **`kubectl port-forward` est lié au POD, pas au Service.** Le `rollout restart` de l'étape 5 détruit le pod → le tunnel meurt → le smoke test échoue avec `[ECHEC] L'API ne répond pas` alors que le déploiement est parfaitement sain. C'est un **faux négatif** très trompeur. Deux solutions :
> - `bash scripts/deploy_k8s.sh --smoke` → le tunnel est géré automatiquement (recommandé) ;
> - ou rouvrir `kubectl port-forward` **après** le déploiement, dans un terminal dédié.

#### Prouver que vous testez bien Kubernetes, et pas Compose

Si les deux stacks tournent, comparez l'horodatage de démarrage du processus. Le pod K8s et le conteneur Compose n'ont pas le même âge :

```bash
svc=$(curl -s http://localhost:8000/metrics | awk '/^process_start_time_seconds /{print $2}')
pod=$(kubectl get --raw "/api/v1/namespaces/parcelpulse/pods/$(kubectl get pod -n parcelpulse -o jsonpath='{.items[0].metadata.name}')/proxy/metrics" \
      | awk '/^process_start_time_seconds /{print $2}')
python3 -c "
import time
svc=float('$svc'); pod=float('$pod'); now=time.time()
print(f'service sur localhost:8000 démarré il y a {now-svc:6.0f} s')
print(f'pod K8s                       démarré il y a {now-pod:6.0f} s')
print('=> le service est le', 'POD K8S' if abs(svc-pod) < 5 else 'CONTENEUR COMPOSE (faux positif !)')
"
```

### A5. Nettoyage

```bash
bash scripts/undeploy_k8s.sh
docker compose down
```

> ⚠️ **`undeploy_k8s.sh` supprime le PersistentVolume — c'est indispensable.** `pv.yml` déclare `persistentVolumeReclaimPolicy: Retain`. Un simple `kubectl delete -f k8s/` laisse le PV à l'état `Released` : il ne sera plus jamais associé à un nouveau PVC, et le déploiement suivant aura un PVC bloqué en `Pending` sans message d'erreur évident.

### A6. Validateur global du pack

Depuis la racine du pack (`RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/`) :

```bash
python3 tools/validate_entire_pack.py
```

**Sortie attendue :**
```text
✅ Phase 1 : Inventaire vérifié (176 fichiers conformes au MANIFEST.md)
✅ Phase 2 : Compilation Python OK (38 fichiers vérifiés sans erreur)
✅ Phase 3 : Validation YAML OK (40 manifests parsés avec succès)
✅ Phase 4 : Starter Project intègre (13 fichiers clés vérifiés)
✅ Phase 5 : Projet de Référence 100% conforme (tests validés : 12 passed)
✅ Phase 6 : Les 13 Labs Pratiques sont structurés et validés (LAB_01 à LAB_13)

STATUT GLOBAL : 100% OPÉRATIONNEL & CONFORME
```

> ⚠️ **Ce script signalait autrefois un échec derrière un ✅.** Avant correction, un `pytest` en échec était rapporté dans la ligne de succès sous la forme `(pytest code retour 2)`, et le nombre de tests était codé en dur (`4 passed`). Vérifié depuis : avec un test en échec, il sort désormais en `❌ Phase 5 FAILED ... (code retour 1)`.
>
> ⚠️ **Un environnement non installé ne doit pas ressembler à un projet non conforme.** Le script utilise le `.venv` du projet s'il existe, sinon l'interpréteur ambiant. Sans `.venv` et sans dépendances dans l'interpréteur ambiant, `pytest` échoue sur `ModuleNotFoundError: prometheus_fastapi_instrumentator` — un problème de setup, pas de code. Le script vérifie désormais la présence de `pytest`, `fastapi` et `prometheus_fastapi_instrumentator` avant de lancer la suite et émet un `⚠️ Phase 5` avec la commande à exécuter, au lieu d'un `❌` trompeur. Un **vrai** échec de test reste un `❌`.

---

## 3. Partie B — Infrastructure AWS / Runner `shell`

> **C'est le chemin officiel de l'examen.** L'énoncé demande un runner de type `shell` nommé `shell` ; le runner Kubernetes de la VM (Partie C) n'est **pas** utilisé par le pipeline de référence et n'est décrit ici que pour que vous ne le confondiez pas avec le bon.

### B1. État vérifié de la VM

Diagnostic réalisé le 4 octobre 2026, en lecture seule :

| Composant | État constaté |
|---|---|
| Système | Ubuntu 22.04.5 LTS, kernel 6.8.0-1021-aws, x86_64 |
| Adresse interne | `172.31.44.121` |
| Cluster | **MicroK8s** (snap), mono-nœud `ip-172-31-44-121` — Kubernetes **v1.30.14**, containerd 1.6.28, `Ready` |
| Addons MicroK8s actifs | dns, ha-cluster, helm, helm3, hostpath-storage |
| **Runner CI (`shell`)** | service `gitlab-runner` **active**, identifiant **`57025042`**, `executor = "shell"` |
| Executor `shell` | les jobs s'exécutent **directement sur la VM**, sans conteneur ni pod |
| Base du runner | `/etc/gitlab-runner/config.toml`, `concurrent = 1`, `check_interval = 0` |
| Registre du runner | `https://gitlab.com/` (GitLab **SaaS**, pas une instance auto-hébergée) |
| Utilisateur d'exécution | `gitlab-runner`, **membre du groupe `docker`** |
| Docker sur la VM | client **27.5.1**, serveur **27.5.1** — joignable par le runner, **sans `privileged`** |
| Python sur la VM | 3.10.12 + `venv` (non utilisé par la CI : les tests tournent en conteneur 3.12) |
| Connexion GitLab | TCP **ESTABLISHED** vers `gitlab.com:443` (long polling) |
| Accès Kubernetes | **absent** — et c'est un choix délibéré (voir [section 6](#6--sécurité--ce-quil-ne-faut-jamais-faire)) |
| Runner Kubernetes (non utilisé) | pod `gitlab-runner-7696d84b5d-pxp7j`, namespace `order-dev`, chart `gitlab-runner-0.93.0` → voir [Partie C](#4--partie-c--annexe--le-runner-kubernetes-et-le-piège-docker-in-docker) |
| Disque | `/` 20 Go, **9,6 Go utilisés (50 %)** après le build CI |
| Maintenance | 75 mises à jour disponibles, **redémarrage système requis** |

**Conclusion** : le runner `shell` est enregistré, actif et a exécuté le pipeline de bout en bout.

> ⚠️ **Pourquoi ce runner ne peut pas déployer Kubernetes, et pourquoi c'est sans importance.**
> L'énoncé sépare les rôles : le runner exécute la CI, Kubernetes héberge l'application. Notre runner n'a donc **pas** de `kubeconfig`, et le pipeline s'arrête au `docker build`. Le déploiement se fait **à la main** depuis la VM avec [`scripts/deploy_k8s.sh`](../reference_project/scripts/deploy_k8s.sh) — voir le [guide 04](04_DEPLOIEMENT_KUBERNETES_PAS_A_PAS.md).

### B2. Diagnostic reproductible (100 % lecture seule)

```bash
# Service du runner
systemctl is-active gitlab-runner     # → active
systemctl is-enabled gitlab-runner    # → enabled

# Runners enregistrés
sudo gitlab-runner list

# Enregistrement auprès de GitLab (le test qui compte)
sudo -u gitlab-runner gitlab-runner verify
#   => Verifying runner... is valid

# Configuration, sans divulguer le token
sudo sed -E 's/(token|password)[[:space:]]*=.*/\1 = "XXX"/' /etc/gitlab-runner/config.toml

# Connexion réelle vers GitLab (check_interval = 0 => long polling)
PID=$(pgrep -f 'gitlab-runner run --config /etc/gitlab-runner' | head -1)
sudo ss -tnp | grep "pid=$PID"        # → ESTAB ... :443

# Capacités nécessaires aux jobs
id gitlab-runner | tr ',' '\n' | grep -i docker
sudo -u gitlab-runner docker version
```

> ⚠️ **`config.toml` contient un token d'authentification.** Ne copiez jamais ce fichier en entier. Le `sed` ci-dessus masque la valeur mais **conserve la structure**, contrairement à `grep -vE 'token|password'` qui supprime des lignes entières et masque les clés absentes.
>
> ⚠️ **`check_interval = 0` signifie « long polling », pas « runner mort ».** Le runner ne journalise donc **pas** périodiquement `Checking for jobs...`. Son activité se prouve par la connexion TCP ouverte, pas par la présence de logs récents.
>
> ⚠️ **Le réglage « Run untagged jobs » n'apparaît nulle part dans `config.toml`.** C'est un attribut **côté serveur** : un runner configuré sans tags et avec cette case décochée est *indistinguable* d'un runner mort lorsqu'on lit le fichier. Voir [B5](#b5--activer-le-runner--le-piège-run-untagged-jobs).

### B3. Créer le projet GitLab (action manuelle)

Sur <https://gitlab.com/new/projects> :

1. **Project name** : `parcelpulse-api`
2. **Visibility** : **Private**
3. **Initialize repository with** : **ne rien cocher** (README, .gitignore, LICENSE) — le dépôt existe déjà localement
4. **Create project**

> ⚠️ **Ne pas pousser dans `devops3274103/order`.** Le dossier `~/gitlab/order` sur la VM est une **autre application** (pipeline d'évaluation, images Docker dans le registry GitLab). Mélanger les deux projets corromprait les deux pipelines.

### B4. Pousser le dépôt autonome

Le dossier `reference_project/` est imbriqué dans le pack, dont il n'est pas un dépôt Git autonome. On crée un dépôt propre contenant **exactement** ce dont le pipeline a besoin :

```bash
STAGE=/tmp/parcelpulse-api
cd ~/workspace/learning/datascientest/RNCP/RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/exam/correction/reference_project

rm -rf "$STAGE"; mkdir -p "$STAGE"
for f in .gitlab-ci.yml .dockerignore .gitignore Dockerfile requirements.txt; do cp "$f" "$STAGE"/; done
cp -R app tests scripts k8s config grafana "$STAGE/"
rm -rf "$STAGE"/.pytest_cache "$STAGE"/**/__pycache__

cd "$STAGE"
git init -b main
git add -A
git commit -m "feat(ci): pipeline ParcelPulse (tests + docker build) pour runner shell"
git remote add origin git@gitlab.com:<VOTRE_UTILISATEUR>/parcelpulse-api.git
git push -u origin main
```

**27 fichiers** sont poussés. `models/model.joblib` n'est volontairement pas inclus : le pipeline le régénère (`python scripts/create_artifact.py`), et c'est lui qui garantit que l'artefact est reproductible à chaque exécution.

### B5. Activer le runner : le piège « Run untagged jobs »

Dans **Settings → CI/CD → Runners** du projet :

1. **Désactiver les runners d'instance** — GitLab.com en propose **136**, tous éligibles par défaut. Sans cela, n'importe lequel peut exécuter vos jobs et vous faire croire que tout va bien alors que votre VM n'a jamais travaillé.
2. **Assigner le runner `shell` (`57025042`)** au projet, et vérifier qu'il apparaît comme **Active**.
3. ⚠️ **Cocher « Run untagged jobs »** — voir ci-dessous.
4. Lancer un pipeline manuel si le push n'a rien déclenché : **Build → Pipelines → Run pipeline**.

> ⚠️⚠️ **Le piège qui a fait bloquer ce pipeline deux fois.**
> Le `.gitlab-ci.yml` de référence ne déclare **aucun `tags:`** (choix de simplicité assumé). Or un runner porteur de tags n'accepte que les jobs portant les mêmes tags. Si « Run untagged jobs » est décoché :
>
> | Symptôme observé | Ce qui se passe vraiment |
> |---|---|
> | Pipeline **stuck / pending** indéfiniment | GitLab ne propose **jamais** le runner pour ces jobs |
> | Aucune erreur dans les logs | il n'y a **aucun job** à exécuter, donc rien à journaliser |
> | Runner affiché **Active** dans l'UI | l'attribut `run_untagged` est **côté serveur**, invisible dans `config.toml` |
>
> **Diagnostic en 30 secondes** : si le pipeline est stuck alors que le service est actif et `verify` renvoie `is valid`, cochez la case. C'est **la** cause — pas `privileged`, pas DinD, pas le réseau.
>
> **Correctif robuste (recommandé)** : déclarer explicitement `tags: [shell]` dans le YAML **et** mettre le tag `shell` sur le runner. Le pipeline devient alors insensible à ce réglage, ce qui est la bonne pratique dès qu'un projet a plusieurs runners.

### B6. Valider le pipeline en local, avant tout push

Inutile d'attendre GitLab pour savoir si le `.gitlab-ci.yml` est correct — les jobs se rejouent **à l'identique** en local.

**Job `tests`** — exactement les mêmes options que le YAML :
```bash
STAGE=/tmp/parcelpulse-api
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$STAGE":/build -w /build python:3.12-slim sh -c '
  set -e
  python --version
  python -m pip install --no-cache-dir --user -r requirements.txt
  python scripts/create_artifact.py
  python -m pytest -v 2>&1 | tail -5
'
```
→ attendu `12 passed`

> ⚠️ **Ne supprimez pas `--user`, `-e HOME=/tmp` ni le `--user` de pip pour « simplifier ».** Sans eux, l'installation échoue (`site-packages` non inscriptible) ; et les fichiers produits seraient ensuite possédés par root, donc **non supprimables** par le nettoyage automatique de GitLab. Ce trio est ce qui rend le job relançable sans `sudo` sur la VM.

**Job `docker_build`** — sur un runner `shell`, il n'y a **ni DinD ni `privileged`** : le runner utilise le daemon Docker de la VM.
```bash
cd "$STAGE"
docker build -t parcelpulse-api:latest .
docker run --rm parcelpulse-api:latest python -c "from app.main import app; print('Import OK:', app.title)"
```
→ attendu `Import OK: parcelpulse-api`

### B7. Résultat vérifié du pipeline

Commit `fa5c0c1`, pipeline `#2911344859` — **Passed**, 3 jobs, 36 s d'exécution :

| Job | Résultat |
|---|---|
| `tests` | ✅ `12 passed` |
| `docker_build` | ✅ `Import OK: parcelpulse-api` |
| `docker_push` | ⏸ **manuel** (`when: manual`, `allow_failure: true`) — non bloquant, conforme au design |

Preuve que c'est bien **la VM** qui a exécuté, et non un runner partagé GitLab :

```text
Running with gitlab-runner 19.4.1
  on shell 57rYfgq8b, system ID: s_bec3b3a4a628
Preparing the "shell" executor
Using Shell (bash) executor...
Running on ip-172-31-44-121...
Checking out fa5c0c11 as detached HEAD (ref is main)...
```

Et le contrôle de l'image sur la VM :

```console
$ sudo docker images parcelpulse-api
parcelpulse-api:latest  168MB  2 minutes ago
$ sudo docker run --rm parcelpulse-api:latest python -c "from app.main import app; print('Import OK:', app.title)"
Import OK: parcelpulse-api
```

> ⚠️ **« Pipeline vert » ne signifie pas « mon runner a worked ».** Un premier pipeline « vert » avait été exécuté par un runner partagé `docker+machine` de GitLab, où DinD fonctionne **par construction** (une VM jetable par job) — ce qui masquait complètement notre problème de configuration. **Toujours lire la ligne `on …` du log.**

### B8. Déploiement sur le cluster AWS — le piège Docker / containerd

Le déploiement se fait **à la main** depuis la VM (le runner n'a pas de kubeconfig), avec `scripts/deploy_k8s.sh`.

> ⚠️⚠️ **L'obstacle réel n'est pas Kubernetes, c'est le magasin d'images.**
> Kubernetes exécute les pods avec **containerd**. Le daemon **Docker** et **containerd** ont deux magasins **complètement séparés**. Une image construite par la CI dans le store Docker est donc **invisible** du cluster : le manifest part en
> ```text
> Failed to pull image "parcelpulse-api:latest": rpc error: … ErrImageNeverPull
> ```
> …alors que `docker images` affiche l'image en toutes lettres. C'est le piège le plus trompeur de cette partie, parce que le symptôme désigne Kubernetes alors que la cause est Docker.
>
> **La solution retenue : nommer l'image avec son adresse de registre.** `k8s/deployment.yml` référence `tawounfouet/parcelpulse-api:latest`, ce qui rend **un seul manifest valable pour deux situations** :
>
> | Cluster | Mécanisme | Rôle de `IfNotPresent` |
> |---|---|---|
> | kind / minikube | `kind load docker-image` | aucun pull : l'image est déjà dans le nœud |
> | MicroK8s (AWS) | containerd tire l'image **publique** | un pull, puis cache local |
>
> **Repli hors-ligne** (cluster sans accès à Internet) : `bash scripts/deploy_k8s.sh --import-local`, qui injecte l'image dans containerd (`docker save` → `sudo microk8s ctr images import`) et force `imagePullPolicy: Never`.

**Vérification faite sur le cluster AWS :**

```console
$ kubectl get pod -n parcelpulse -l app=parcelpulse-api \
    -o jsonpath='{.items[0].status.containerStatuses[0].imageID}'
docker.io/tawounfouet/parcelpulse-api@sha256:5c559c5c905ff246037b9d3c8a77ae88cbe74669d3a1ac97b8b3fc148755cad5
```

Ce digest est **identique** à celui annoncé par le job `docker_push` (`latest: digest: sha256:5c559c5c…`). C'est la preuve formelle que le pod exécute **l'image construite par la CI**, et pas une reconstruction locale : la chaîne `git push → CI → registre → pod` est vérifiée de bout en bout.

État du déploiement et smoke test :

```console
$ kubectl get all,pvc -n parcelpulse
pod/parcelpulse-api-69444c4d79-6l99b   1/1   Running   0
persistentvolumeclaim/parcelpulse-pvc   Bound  parcelpulse-pv   1Gi   RWO   manual

$ bash scripts/deploy_k8s.sh --smoke
  Smoke test OK - 11 verifications reussies
```

> ⚠️ **Deux détails d'environnement propres à cette VM, qui font échouer le déploiement :**
> 1. **`kubectl` n'est pas dans le `PATH`** : MicroK8s l'installe dans `/snap/microk8s/current/kubectl`. Sans wrapper, le script s'arrête sur `kubectl: command not found`.
> 2. **Ne pas utiliser `sudo bash scripts/deploy_k8s.sh`**. `sudo` remet `HOME` à `/root`, donc `kubectl` ne trouve plus `~/.kube/config` et le script échoue sur `Contexte actif : <aucun>` — un message qui ne parle ni de Docker ni de permissions et fait perdre du temps. Passer par `sg docker -c` pour hériter du groupe du daemon Docker sans changer de `HOME` :
>    ```bash
>    sg docker -c "bash scripts/deploy_k8s.sh --smoke"
>    ```

---

## 4. Partie C — Annexe : le runner Kubernetes et le piège Docker-in-Docker

> ⚠️ **Cette partie n'est pas exigée par l'examen et n'est plus utilisée par le pipeline de référence.** Elle est conservée parce que le runner Kubernetes **existe bel et bien sur la VM**, que l'énoncé mentionne Kubernetes, et que les deux erreurs ci-dessous ont réellement été commises puis corrigées. Si vous n'avez qu'une chose à retenir : **si vous utilisez le runner `shell` de la Partie B, tout ce qui suit ne vous concerne pas** — pas de DinD, pas de `privileged`, pas de `DOCKER_HOST`.

### Le problème

Une première version du `.gitlab-ci.yml` utilisait Docker-in-Docker, avec un runner Kubernetes :

```yaml
docker_build:
  stage: build
  image: docker:27-cli
  services:
    - docker:27-dind
  variables:
    DOCKER_TLS_CERTDIR: ""
```

Or les pods de job de ce runner **ne sont pas privileged**.

### Où se règle `privileged`, et où il ne se règle PAS

C'est le point qui piège tout le monde. Il y a **deux endroits différents** qui contiennent le mot `privileged`, et un **troisième** qui n'existe pas :

| Emplacement | Ce qu'il contrôle | Valeur sur cette VM |
|---|---|---|
| `securityContext.privileged` dans `values.yaml` (ligne 534) | Le **conteneur principal du pod runner lui-même**. Le commentaire du chart est explicite : *"Configure securitycontext for the main container"*. À côté : `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`. | `false` |
| `privileged` dans `.gitlab-ci.yml` (job) | Uniquement l'executor **`docker`**. Sur l'executor **`kubernetes`** cette ligne est **simplement ignorée**. | sans objet |
| `[runners.kubernetes] privileged` dans le **`config.toml`** du runner | **C'est celui-là qui décide** si les pods de job sont privileged. | **absent** |

Le `config.toml` réellement monté dans le pod runner a été extrait et inspecté (jetons expurgés) :

```toml
[[runners]]
  name = "gitlab-runner-7696d84b5d-pxp7j"
  url = "https://gitlab.com/"
  executor = "kubernetes"
  [runners.kubernetes]
    host = ""
    image = "alpine"
    namespace = "order-dev"
    namespace_overwrite_allowed = ""
    namespace_per_job = false
    service_account_overwrite_allowed = ""
```

**Aucune ligne `privileged` dans tout le fichier.** Or la valeur par défaut de GitLab Runner pour `[runners.kubernetes] privileged` est `false`. Donc les pods de job tournent **non privileged**, et le service `docker:27-dind` échouera.

> ⚠️ **Le correctif ne va PAS dans `securityContext`.** C'est l'erreur la plus probable : modifier `securityContext.privileged` ne change rien aux pods de job, et le runner redémarre pour rien.

### La démonstration

Test exécuté dans la topologie GitLab exacte (`docker:27-cli` partageant le namespace réseau du service `docker:27-dind`) :

| Configuration | Résultat observé |
|---|---|
| `docker run -d --name ci-dind …` (**sans** privileged) | **Le daemon DinD ne démarre pas.** Logs : `mount: permission denied (are you root?)`, `Could not mount /sys/kernel/security.` |
| `docker run -d --privileged --name ci-dind …` | `client=27.5.1 / server=27.5.1` → `docker build` OK → `Import OK: parcelpulse-api` |

**Conclusion : avec `privileged: false`, le job `docker_build` échoue.** Ce n'est pas une supposition, c'est mesuré.

### Le correctif

Sur l'executor `kubernetes`, `privileged` se règle dans le **`config.toml` du runner**, que le chart génère à partir du template `runners.config` de `values.yaml`. La clé du job dans `.gitlab-ci.yml` est ignorée.

**Étape 1 — vérifier qu'il n'existe pas déjà de ligne `privileged`** :

```bash
# Sur la VM AWS
export KUBECONFIG="$HOME/.kube/config"
K="/snap/microk8s/current/kubectl"
$K exec -n order-dev deploy/gitlab-runner -- cat /home/gitlab-runner/.gitlab-runner/config.toml \
  | sed -E 's/(Token|token|Password|password)[[:space:]]*=.*/\1 = "XXX"/g' \
  | grep -n privileged || echo ">>> absent, donc false (valeur par defaut du runner)"
```

**Étape 2 — ajouter `privileged = true` dans le template `runners.config`** :

```bash
cd ~/gitlab/kubernetes/runner
cp values.yaml values.yaml.bak.$(date +%Y%m%d)     # sauvegarde obligatoire

# Insérer la ligne juste après image = "alpine", dans le bloc [runners.kubernetes]
# du template `config: |` (autour de la ligne 400 du fichier).
python3 - <<'PY'
import re, pathlib
p = pathlib.Path("values.yaml")
s = p.read_text()
assert 'privileged' not in s.split("runners:")[1], "privileged deja present : verifier manuellement"
s2 = s.replace(
    '      [runners.kubernetes]\n        namespace = "order-dev"\n        image = "alpine"\n',
    '      [runners.kubernetes]\n        namespace = "order-dev"\n        image = "alpine"\n        privileged = true\n',
    1,
)
assert s2 != s, " motif non trouve : editer values.yaml a la main"
p.write_text(s2)
print("privileged = true insere dans le template runners.config")
PY

sed -n '/^runners:/,/^  ## Absolute path/p' values.yaml | head -15
```

**Étape 3 — appliquer et vérifier** :

```bash
helm upgrade gitlab-runner gitlab/gitlab-runner \
  -n order-dev \
  -f ~/gitlab/kubernetes/runner/values.yaml \
  --set rbac.create=true

$K rollout status deploy/gitlab-runner -n order-dev --timeout=180s
$K get pods -n order-dev

# LA vérification qui compte : la ligne doit être présente après redémarrage
$K exec -n order-dev deploy/gitlab-runner -- cat /home/gitlab-runner/.gitlab-runner/config.toml \
  | grep -n 'privileged'
```

Sortie attendue de la dernière commande : `privileged = true`.

> ⚠️ **`--set privileged=true` ne fonctionne pas et ne provoque aucune erreur.** Le chart `gitlab-runner-0.93.0` **n'expose aucune clé racine `privileged`** (vérifié avec `helm show values gitlab/gitlab-runner`). Helm accepterait la commande, l'afficherait dans le résumé de l'upgrade… et ne changerait rien. Un `no-op` silencieux est plus dangereux qu'une erreur : il donne l'impression d'avoir corrigé le problème.
>
> C'est aussi pour cela que la commande est donnée ici sous sa forme vérifiable (`gitlab/gitlab-runner` comme chemin de chart, `-f values.yaml`, puis `grep` sur le `config.toml` **après** redémarrage) et non sous une forme « à l'intuition ».

> ⚠️ **Portée du changement.** `privileged = true` s'applique à **tous** les pods de job de ce runner, pas seulement à ParcelPulse. Le runner étant partagé au niveau instance, le projet `order` en bénéficie aussi. C'est un élargissement de privilèges : un job peut alors monter le système de fichiers hôte, ce qui équivaut à un accès root au nœud. À n'activer que si les dépôts qui utilisent ce runner sont de confiance.
>
> `--set rbac.create=true` n'est pas nécessaire pour faire tourner les jobs — les permissions du ServiceAccount `default` suffisent (cf. B1). C'est néanmoins la configuration recommandée du chart : elle crée un ServiceAccount dédié au runner au lieu de laisser tous les jobs employer `default`.

### Alternative sans privileged

Si le durcissement est une contrainte, la voie sans DinD est d'utiliser **Kaniko** ou **Buildah**, qui construisent des images sans daemon Docker ni privilèges :

```yaml
docker_build:
  stage: build
  image: gcr.io/kaniko-project/executor:latest
  script:
    - /kaniko/executor --context . --dockerfile Dockerfile --destination parcelpulse-api:latest
```

> ⚠️ Cette option **divergera du guide 03 du pack**, qui présente DinD comme la notion à maîtriser pour l'examen. À réserver au cas où le durcissement prime sur la conformité au support de cours.

---

## 5. Dépannage — Tableau des symptômes

### Côt Kubernetes

| Symptôme | Cause réelle | Solution |
|---|---|---|
| `error validating "k8s/…": failed to download openapi: dial tcp …: connection refused` | **Aucun cluster joignable** — contexte mort. Pas un problème de YAML | `kind create cluster` / démarrer le cluster ; `kubectl config get-contexts` pour inspecter |
| `Error from server (NotFound): namespaces "parcelpulse" not found` | Ordre alphabétique de `apply -f <dossier>` | `kubectl apply -f k8s/namespace.yml` puis `-f k8s/` — ou `deploy_k8s.sh` |
| Pod `ErrImageNeverPull` | Image construite sur l'hôte, invisible du cluster | `kind load docker-image parcelpulse-api:latest` |
| Pod `ErrImageNeverPull` **alors que `docker images` affiche l'image** | ⚠️ **Docker et containerd n'ont pas le même magasin d'images** : Kubernetes utilise containerd, donc une image construite par `docker build` est invisible du cluster | Référencer l'image par son **nom de registre** pour que containerd la tire, ou l'injecter : `docker save … \| sudo microk8s ctr images import -` (voir B8) |
| Pod `ImagePullBackOff` | `imagePullPolicy` tente de résoudre l'image sur Docker Hub | Garder `IfNotPresent` + `kind load` |
| PVC `Pending` | PV laissé en `Released` (`Retain`) après un `delete -f` | `bash scripts/undeploy_k8s.sh` puis redéployer |
| Pod `0/1 Init` bloqué | L'`initContainer` ne copie pas le modèle | `kubectl logs <pod> -n parcelpulse -c init-model-artifact` |
| Smoke test `[ECHEC] L'API ne répond pas` après un déploiement | Le port-forward a été coupé par le `rollout restart` | `deploy_k8s.sh --smoke`, ou rouvrir le tunnel |
| `exec format error` | Image architectures incompatibles (ARM local / x86 runner) | Construire avec `--platform linux/amd64` |
| `WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8)` après un `pull` | L'image a été construite sur la VM **x86_64**, on la tire sur un Mac **Apple Silicon** | Sans gravité : l'exécution passe par l'émulation. Pour la vitesse, `docker run --platform linux/amd64` explicite, ou construire localement en arm64 |

### Côt Docker / Compose

| Symptôme | Cause réelle | Solution |
|---|---|---|
| `port is already allocated` | Compose (8000) et port-forward (8000) se disputent le port | `docker compose down` avant le K8s |
| Conteneur `app-1` en `Exited` | `/models/model.joblib` absent (montage `- ro` en lecture seule) | `python scripts/create_artifact.py` puis `docker compose up -d` |
| Target Prometheus `down` | L'API ne répond pas sur `app:8000` | `docker compose logs app` |
| `promql` renvoie *No data* | `rate()` a besoin de 2 scrapes (15 s) | Attendre ~30 s, interroger `http_requests_total` brut |
| Datasource Grafana `Unable to find datasource` | Id numérique utilisé au lieu de l'`uid` | Utiliser l'`uid` renvoyé par `/api/datasources` |

### Côt CI / GitLab

| Symptôme | Cause réelle | Solution |
|---|---|---|
| ⚠️ **Pipeline `stuck` / `pending` indéfiniment, aucun log, runner affiché `Active`** | **« Run untagged jobs » décoché** — attribut **côté serveur**, invisible dans `config.toml`. Le runner n'est jamais proposé pour un job sans `tags:` | Cocher la case dans **Settings → CI/CD → Runners → Edit**. Correctif durable : ajouter `tags: [shell]` au YAML **et** au runner |
| Job `pending` alors que le runner est bien assigné | Runner **pausé** ou **désactivé** pour ce projet | `Settings → CI/CD → Runners`, vérifier **Active** et l'assignation |
| Pipeline vert, mais le log commence par `on docker-…` ou un autre nom | Un **runner d'instance partagé** (136 sur GitLab.com) a pris le job | Désactiver les runners d'instance, ou vérifier la ligne `on …` de chaque job |
| Job échoue sur `No module named pytest` | Conteneur de test sans pytest | Utiliser `python -m pytest` après `pip install --user` (voir guide 03 §2) |
| Job échoue sur `pip install` (`permission denied` / `site-packages`) | `--user` retiré du YAML | Le conteneur tourne avec `--user "$(id -u):$(id -g)"` : **`pip` a besoin de `--user`** |
| Job `tests` échoue sur `FileNotFoundError: Model not found` | Artefact non généré | Le job lance `python scripts/create_artifact.py` avant `pytest` |
| Job `docker_build` échoue sur `Cannot connect to the Docker daemon at unix:///var/run/docker.sock` | Runner `shell` **non membre du groupe `docker`**, ou service arrêté | `id gitlab-runner \| grep docker` ; `sudo -u gitlab-runner docker version` |
| Job `docker_build` échoue sur DinD (`mount: permission denied`, `Could not mount /sys/kernel/security`) | *Runner Kubernetes uniquement* — `[runners.kubernetes] privileged` absent | **Hors sujet avec le runner `shell`.** Voir Partie C si vous repartez sur le runner K8s |
| Pod de job `CreateContainerError` | *K8s* — `hostPath` hérité du projet `order` absent ou interdit sur le nœud | `ls /home/ubuntu/gitlab/order/cache/{apt,pip}` sur le nœud |
| Pod de job créé dans `order-dev` et non dans un namespace dédié | *K8s* — `namespace_per_job = false`, `namespace_overwrite_allowed = ""` | Comportement attendu du runner mutualisé ; ne pas chercher un namespace `parcelpulse` |
| Aucune donnée avec `{app="…"}` dans Prometheus | Ce libellé n'existe pas | Libellés réels : `handler`, `method`, `status` |

---

## 6. Sécurité — Ce qu'il ne faut jamais faire

1. **Ne jamais committer ni copier `config.toml`.** Il contient le token d'authentification du runner (préfixe `glrt-`). Pour l'inspecter, **masquez la valeur et conservez la structure** :
   ```bash
   sudo sed -E 's/(token|password)[[:space:]]*=.*/\1 = "XXX"/' /etc/gitlab-runner/config.toml
   ```
   ⚠️ Pas de `grep -vE 'token|password'` : cela supprime des lignes entières et **masque les clés absentes** — or une clé manquante est précisément l'information qu'on cherche (cf. Partie C).
2. **Les credentials GitLab dans `.gitlab-ci.yml` sont interdites.** Les passer par **Settings → CI/CD → Variables** (marquées *masked and protected*) et les référencer ainsi :
   ```yaml
   script:
     - echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USER" --password-stdin
   ```
3. **`data_enginering_machine.pem` doit rester en `chmod 400`** et hors de tout dépôt Git.
4. **`privileged = true` dans `[runners.kubernetes]` élargit la surface d'attaque.** Un job peut alors monter le système de fichiers hôte. À réserver aux dépôts de confiance.
5. **Le token du runner est dans `~/gitlab/kubernetes/runner/values.yaml`** (champ `runnerToken`). Ne pas le versionner ni l'afficher dans une capture d'écran partagée.
6. **Le cluster MicroK8s est mono-nœud, `high-availability: no`.** Aucune tolérance de panne : le stockage est local au nœud (`hostPath`) et `control-plane` et `worker` tombent ensemble.

---

## 7. Limites — Ce qui n'a pas pu être vérifié

Cette distinction est importante pour ne pas sur-vendre ce qui est réellement vérifié.

| Élément | Statut | Raison |
|---|---|---|
| Cluster local kind, Compose, Prometheus, Grafana | ✅ Exécuté | — |
| Job `tests` en `python:3.12-slim` | ✅ Exécuté | — |
| Job `docker_build` via le daemon Docker de la VM | ✅ Exécuté | — |
| Diagnostic de la VM AWS | ✅ Exécuté | Lecture seule |
| **Pipeline GitLab réel sur le runner `shell`** | ✅ **Exécuté** | Pipeline `#2911344859`, commit `fa5c0c1` : `tests` ✅, `docker_build` ✅, `docker_push` manuel. Preuve `on shell 57rYfgq8b` |
| **`docker push` vers DockerHub** | ✅ **Exécuté** | Job manuel `docker_push` (pipeline `#2911344859`) : `Login Succeeded`, tag `tawounfouet/parcelpulse-api:latest`, digest `sha256:5c559c5c…`. Vérifié ensuite par **pull anonyme** + `Import OK` |
| **Déploiement sur le cluster AWS** | ✅ **Exécuté** | Cluster MicroK8s : pod `1/1 Running`, PVC `Bound`, smoke test **11/11**. Le pod tourne l'image **publiée par la CI** (`imageID` = `sha256:5c559c5c…`) |
| **Suppression du runner Kubernetes** | ⏳ Non fait | À conserver en l'état : il est désassigné du projet et n'est plus éligible pour ses jobs |
| **`helm upgrade` avec `privileged = true`** | ⏳ Non appliqué | Hors sujet (runner `shell`). De plus, `--set privileged=true` ne fonctionnerait pas : clé inexistante dans le chart, cf. Partie C |
| **Épinglage de `requirements.txt`** | ⏳ Non fait | Le venv local est en Python 3.13, le Dockerfile et la CI en 3.12 : épingler depuis le 3.13 figerait des versions potentiellement incompatibles avec Python 3.12. À faire après un `pip freeze` sur les deux interpréteurs. |

---

### Prochaine étape

- Pour comprendre la théorie du runner : [03_GITLAB_CI_ET_RUNNER_SHELL.md](03_GITLAB_CI_ET_RUNNER_SHELL.md)
- Pour le déploiement Kubernetes détaillé : [04_DEPLOIEMENT_KUBERNETES_PAS_A_PAS.md](04_DEPLOIEMENT_KUBERNETES_PAS_A_PAS.md)
- Pour les commandes de dépannage par erreur : [06_DEPANNAGE_ET_FAQ_DES_NULS.md](06_DEPANNAGE_ET_FAQ_DES_NULS.md)