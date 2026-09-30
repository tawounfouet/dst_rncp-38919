# ParcelPulse — Starter Project (Examen Blanc)

Ce projet constitue le squelette de départ de l'examen blanc **ParcelPulse** pour l'épreuve **RNCP 38919 — Bloc 3**.

---

## 1. Documents de référence

* **Sujet officiel de l'examen :** [14_RNCP_38919_BLOC_3_EXAMEN_BLANC_01.md](../sujet/14_RNCP_38919_BLOC_3_EXAMEN_BLANC_01.md)
* **Données & Notebook source :** [README_DATA.md](../sujet/resources/README_DATA.md)
* **Stratégie de gestion du temps (4h) :** [12_RNCP_38919_BLOC_3_STRATEGIE_EXAMEN_4H.md](../../resources/study_docs/12_RNCP_38919_BLOC_3_STRATEGIE_EXAMEN_4H.md)
* **Checklist du Jour J :** [13_RNCP_38919_BLOC_3_CHECKLIST_JOUR_J.md](../../resources/study_docs/13_RNCP_38919_BLOC_3_CHECKLIST_JOUR_J.md)

---

## 2. Déroulement du travail

Tous les fichiers à compléter contiennent des balises `# TODO:` ou `# TODO` précisant les attendus :

```text
starter_project/
├── app/
│   ├── config.py         # TODO: variables d'environnement APP_NAME, PORT, MODEL_PATH
│   ├── schemas.py        # TODO: schémas Pydantic (PredictionInput, PredictionResponse)
│   ├── model.py          # TODO: chargement joblib du modèle et méthode predict
│   └── main.py           # TODO: routes /, /health, /predict et métriques Prometheus
├── scripts/
│   ├── create_artifact.py# TODO: génération du modèle scikit-learn / joblib
│   └── smoke_test.sh     # TODO: script de test curl
├── tests/
│   └── test_api.py       # TODO: tests pytest (health, predict nominal et invalide)
├── Dockerfile            # TODO: conteneurisation de l'API
├── docker-compose.yml    # TODO: orchestration API + Prometheus + Grafana
├── .gitlab-ci.yml        # TODO: pipeline CI multi-stages
└── k8s/                  # TODO: manifestes Kubernetes (Namespace, PV, PVC, CM, Deploy, Svc)
```

---

## 3. Commandes d'initialisation locale

```bash
# 1. Création et activation de l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# 2. Installation des dépendances
pip install -r requirements.txt

# 3. Génération de l'artefact initial
python scripts/create_artifact.py

# 4. Exécution des tests au fil de l'implémentation
pytest -v

# 5. Démarrage du serveur local de dev
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
