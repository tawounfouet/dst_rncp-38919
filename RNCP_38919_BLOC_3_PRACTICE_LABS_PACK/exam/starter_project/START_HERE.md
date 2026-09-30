# Guide de Démarrage — Starter Project

Ce guide vous accompagne pas à pas dans la réalisation de l'examen blanc.

---

## Étapes recommandées

1. **Prise de connaissance :**
   * Lire le [Sujet officiel de l'examen blanc](../sujet/14_RNCP_38919_BLOC_3_EXAMEN_BLANC_01.md).
   * Consulter les métadonnées et données dans [bootstrap_info.ipynb](../sujet/resources/bootstrap_info.ipynb).

2. **Environnement virtuel & Artefact :**
   * Créer et activer l'environnement :
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt
     ```
   * Générer le modèle initial avec `python scripts/create_artifact.py`.

3. **Implémentation progressive (suivre les `TODO`) :**
   * Étape 1 : `app/config.py` (variables d'environnement).
   * Étape 2 : `app/schemas.py` (validation des entrées/sorties Pydantic).
   * Étape 3 : `app/model.py` (chargement du modèle et prédiction).
   * Étape 4 : `app/main.py` (endpoints `/`, `/health`, `/predict` et instrumentateur Prometheus).
   * Étape 5 : `tests/test_api.py` (validation Pytest).
   * Étape 6 : `Dockerfile` et validation de l'image locale.
   * Étape 7 : `docker-compose.yml` (orchestration API + Prometheus + Grafana).
   * Étape 8 : `.gitlab-ci.yml` (pipeline multi-stages).
   * Étape 9 : `k8s/` (manifestes Kubernetes Namespace, PV, PVC, ConfigMap, Deployment, Service).

4. **Validation continue :**
   * Exécuter `pytest -v`.
   * Lancer `bash scripts/smoke_test.sh` pour tester les endpoints HTTP en conditions réelles.
