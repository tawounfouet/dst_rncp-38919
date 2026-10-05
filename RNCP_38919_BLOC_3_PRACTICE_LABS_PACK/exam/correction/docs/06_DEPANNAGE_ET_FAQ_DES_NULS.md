# 06 — Guide de Dépannage & FAQ des Nuls
## La Boîte à Outils Anti-Panique pour Réussir à 100 %

Ce guide répertorie toutes les pannes et erreurs classiques que vous pouvez rencontrer lors de la manipulation du projet de référence ou pendant l'examen blanc, avec la **solution exacte en une commande**.

---

## 1. Erreurs Python & Environnement Virtuel

### Problème 1 : `[Errno 48] Address already in use` (Port 8000 déjà occupé)
* **Message d'erreur :** `ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use`
* **Pourquoi ?** Un processus Uvicorn, un script `mock_server.py` ou un conteneur Docker tourne déjà sur le port 8000.
* **Solution :**
  ```bash
  # 1. Identifier le processus qui occupe le port 8000
  lsof -i :8000

  # 2. Tuer le processus avec son PID (ex: PID 12345)
  kill -9 <PID>

  # Ou si c'est un conteneur Docker :
  docker ps | grep 8000
  docker stop <CONTAINER_ID>
  ```

---

### Problème 2 : `ModuleNotFoundError: No module named 'app'`
* **Message d'erreur :** `ModuleNotFoundError: No module named 'app'`
* **Pourquoi ?** Vous avez lancé `uvicorn app.main:app` depuis un dossier parent ou enfant sans vous placer dans `exam/correction/reference_project`.
* **Solution :**
  ```bash
  cd /Users/awf/workspace/learning/datascientest/RNCP/RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/exam/correction/reference_project
  python -m uvicorn app.main:app --port 8000
  ```

---

### Problème 3 : `ERROR: Can not perform a '--user' install`
* **Message d'erreur :** `ERROR: Can not perform a '--user' install. User site-packages are not visible in this virtualenv.`
* **Pourquoi ?** macOS ou votre shell force l'option `--user`, ce qui est interdit à l'intérieur d'un environnement virtuel (`.venv`).
* **Solution :**
  ```bash
  pip install --no-user -r requirements.txt
  ```

---

## 2. Erreurs Docker & Docker-Compose

### Problème 4 : `Cannot connect to the Docker daemon`
* **Message d'erreur :** `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`
* **Pourquoi ?** Le moteur Docker n'est pas démarré sur votre machine.
* **Solution :**
  - Sur macOS : Ouvrez l'application **Docker Desktop** et attendez que l'icône indique que le moteur est vert ("Docker is running").

---

### Problème 5 : Port 3000 (Grafana) ou 9090 (Prometheus) en conflit
* **Solution :** Si vous avez déjà un Prometheus ou Grafana qui tourne sur votre machine :
  ```bash
  # Vérifier les conteneurs actifs
  docker ps
  # Tout arrêter proprement
  docker compose down
  ```

---

## 3. Erreurs GitLab CI & Runner

### Problème 6 : Le job GitLab reste indéfiniment en statut `Pending` ("stuck")

* **Symptôme :** le pipeline reste `pending` / `stuck`, **aucun log n'apparaît**, et le runner est pourtant affiché `Active` dans l'interface.
* **Pourquoi ?** Le runner **ne vous propose jamais** pour ces jobs. La cause n°1 est la case **"Run untagged jobs"** (littéralement *« Indicate whether this runner can pick up jobs without tags »*) **décochée** :
  1. le job déclare un tag (ex: `tags: [aws]`) que le runner n'a pas ;
  2. **ou** le runner n'accepte que les jobs taggés, alors que le `.gitlab-ci.yml` de référence ne déclare **aucun `tags:`**.
* **Pourquoi c'est si trompeur :** ce réglage est **côté serveur**. Il n'apparaît **pas** dans `config.toml`, et un runner ainsi configuré est **indistinguable** d'un runner mort quand on lit le fichier de configuration. Le service peut être `active` et `gitlab-runner verify` renvoyer `is valid` : le runner est parfaitement sain, il est simplement **inéligible**.
* **Solution dans l'interface GitLab :**
  - Allez dans **Settings > CI/CD > Runners**.
  - Cliquez sur l'icône de crayon pour éditer votre runner **`shell`**.
  - Cochez impérativement la case : **"Indicate whether this runner can pick up jobs without tags"**.
  - Sauvegardez : le job démarre immédiatement.
* **Correctif plus robuste (recommandé) :** déclarez `tags: [shell]` dans votre `.gitlab-ci.yml` **et** mettez le tag `shell` sur le runner. Le pipeline devient alors insensible à ce réglage.

> ⚠️ **Deuxième piège : un pipeline vert ne prouve pas que c'est VOTRE runner qui a travaillé.** GitLab.com propose **136 runners d'instance** partagés, éligibles par défaut. Désactivez-les (**Disable instance runners**) et vérifiez la ligne `on …` en tête de chaque log :
> ```text
> on shell 57rYfgq8b, system ID: s_bec3b3a4a628
> Using Shell (bash) executor...
> Running on ip-172-31-44-121...
> ```

---

### Problème 7 : Le job `docker_build` échoue sur Docker

* **Message d'erreur le plus courant :** `ERROR: Cannot connect to the Docker daemon at unix:///var/run/docker.sock`
* **Pourquoi ?** Le runner `shell` n'est pas autorisé à parler au daemon Docker. C'est une question de **droits unix**, pas de configuration réseau.
* **Solution :** vérifier que l'utilisateur du runner est membre du groupe `docker`, et que Docker répond :
  ```bash
  id gitlab-runner | tr ',' '\n' | grep -i docker     # → doit apparaître
  sudo -u gitlab-runner docker version              # → client ET server affichés
  ```
  Si `server` n'apparaît pas, le daemon n'est pas démarré : `sudo systemctl start docker`.

* **Si le runner `shell` est dans le groupe `docker`, il n'y a ni `services:`, ni `docker:27-dind`, ni `DOCKER_TLS_CERTDIR`, ni `privileged`.** Ces éléments ne servent qu'aux exécuteurs `docker` et `kubernetes`, où le job tourne lui-même dans un conteneur ; sur l'exécuteur `shell`, **GitLab les ignore**. Les laisser dans le YAML laisse croire à une isolation qui n'existe pas.

* **Cas particulier du runner Kubernetes** (hors sujet de l'examen — runner `57025952` présent sur la VM) : un job qui utilise `services: [docker:27-dind]` exige alors `DOCKER_HOST: tcp://localhost:2375` **et** `[runners.kubernetes] privileged = true` dans le `config.toml` du runner, sinon le service DinD échoue au démarrage :
  ```text
  mount: mounting none on /sys/kernel/security failed: Permission denied
  Could not mount /sys/kernel/security.
  ```
  Le correctif se met dans le **`config.toml` du runner** (template `runners.config` de `values.yaml`), **pas** dans `securityContext.privileged`.

---

## 4. Erreurs Kubernetes

### Problème 8 : Le PVC reste bloqué en statut `Pending`
* **Message d'erreur :** `kubectl get pvc` affiche `STATUS: Pending`
* **Pourquoi ?** Le PV physique correspondant n'a pas été créé ou la classe de stockage ne correspond pas.
* **Solution :**
  1. Assurez-vous d'avoir appliqué `pv.yml` :
     ```bash
     kubectl apply -f k8s/pv.yml
     ```
  2. Vérifiez que `storageClassName: manual` est identique dans `k8s/pv.yml` ET `k8s/pvc.yml`.

---

### Problème 9 : Le Pod affiche `CrashLoopBackOff` ou `Error`
* **Solution d'enquête systématique en 2 commandes :**
  ```bash
  # 1. Lire la description des événements Kubernetes
  kubectl describe pod -l app=parcelpulse-api -n parcelpulse

  # 2. Lire les logs de l'application
  kubectl logs -l app=parcelpulse-api -n parcelpulse --all-containers=true
  ```

---

## 5. Checklist Ultime : « Suis-je Prêt pour l'Examen ? »

Avant de soumettre votre travail ou de passer votre examen blanc, cochez chaque point :

- [ ] **1. Code propre :** Mon code FastAPI charge le modèle `model.joblib` sans chemin absolu codé en dur (utilisation de `os.getenv("MODEL_PATH")`).
- [ ] **2. Typage Pydantic :** Ma route `/predict` rejette les entrées invalides avec un code HTTP 422.
- [ ] **3. Tests Pytest :** La commande `pytest -v` affiche `4 passed` à 100 %.
- [ ] **4. Dockerfile optimisé :** Mon Dockerfile copie `requirements.txt` avant le code source et utilise `python:3.12-slim`.
- [ ] **5. Docker Compose :** `docker compose up -d` démarre sans erreur l'API, Prometheus et Grafana.
- [ ] **6. GitLab CI :** Mon pipeline comporte au moins les stages `test` et `build`, et passe au vert sur le Runner.
- [ ] **7. Kubernetes PVC :** Mon PVC est bien en statut `Bound` et l'InitContainer copie le modèle si nécessaire.
- [ ] **8. Kubernetes Service :** Je peux contacter mon API dans le cluster via `kubectl port-forward`.
- [ ] **9. PromQL :** Je connais la requête PromQL pour compter les requêtes (`http_requests_total`) et calculer le débit (`rate(...)`).
- [ ] **10. Smoke Test :** Le script `scripts/smoke_test.sh` s'exécute sans aucune erreur.

---

### Félicitations !
En maîtrisant ces concepts et en suivant ces guides pas à pas, vous disposez de toutes les clés pour décrocher la note maximale au **Bloc 3 de la certification RNCP 38919** !
