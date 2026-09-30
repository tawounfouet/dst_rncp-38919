# LAB 12 — Checklist d'Intégration End-to-End

Utilisez cette grille pour valider chaque étape du défi d'intégration avant de passer à la suivante.

---

## 1. Socle Python, Modèle & API

- [ ] L'environnement virtuel `.venv` est activé et isolé.
- [ ] Le modèle `models/model.joblib` est généré avec succès par `python scripts/create_artifact.py`.
- [ ] Le modèle s'appuie sur une classe importable hors du script (`app/demo_model.py`) pour éviter les conflits `__main__`.
- [ ] L'application FastAPI démarre sans avertissement : `uvicorn app.main:app --port 8000`.
- [ ] Les endpoints `/` et `/health` renvoient un code HTTP 200 et du JSON valide.
- [ ] L'endpoint `/predict` renvoie une prédiction conforme au schéma Pydantic en payload nominal.
- [ ] L'endpoint `/predict` rejette les payloads non valides avec un code HTTP 422.
- [ ] L'endpoint `/metrics` expose les compteurs Prometheus de l'API.

---

## 2. Qualité de Code & Tests Automatisés

- [ ] La suite de tests unitaires `pytest -v` s'exécute avec 100% de réussite.
- [ ] Le script de test HTTP `bash scripts/smoke_test.sh` valide tous les scénarios.

---

## 3. Conteneurisation & Compose

- [ ] L'image Docker se construit sans cache corrompu : `docker build -t parcelpulse-api .`.
- [ ] Le conteneur s'exécute et répond sur le port mappé : `docker run --rm -p 8000:8000 parcelpulse-api`.
- [ ] La stack `docker compose up -d --build` démarre les 3 services : `api`, `prometheus`, `grafana`.
- [ ] Les 3 conteneurs sont à l'état `healthy` ou `running` dans `docker compose ps`.
- [ ] Prometheus scrape l'API avec succès (cible `fastapi:8000` à l'état `UP`).
- [ ] Grafana est accessible sur le port 3000 et la datasource Prometheus est fonctionnelle.

---

## 4. Pipeline CI/CD

- [ ] Le fichier `.gitlab-ci.yml` est syntaxiquement valide (GitLab CI Lint).
- [ ] Le job de test s'exécute avec succès sur le Runner Shell.
- [ ] L'image est construite et poussée sur DockerHub avec les tags appropriés.

---

## 5. Déploiement Kubernetes

- [ ] Le `Namespace` est créé et actif : `kubectl get ns`.
- [ ] Le `PersistentVolume` (`PV`) et la `PersistentVolumeClaim` (`PVC`) sont au statut `Bound`.
- [ ] La `ConfigMap` injecte correctement les variables d'environnement dans les pods.
- [ ] Les pods du `Deployment` sont tous à l'état `1/1 Running` (aucun `CrashLoopBackOff`).
- [ ] Le `Service` Kubernetes route le trafic vers les pods sur le port 8000.
