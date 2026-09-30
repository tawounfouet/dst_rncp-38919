# RNCP 38919 — Bloc 3 — Practice Labs Pack

Ce pack est un **environnement d'entraînement proposé** pour le Bloc 3 Data Engineer / DevOps.
Il est construit à partir du périmètre annoncé dans le support DataScientest fourni par l'utilisateur.

Il ne constitue **ni le sujet officiel, ni une correction officielle, ni un barème officiel**.

## Périmètre source couvert

```text
Lecture de notebooks Jupyter
Bash : export, .bashrc
Variables d'environnement dans Python
Environnements virtuels Python
Requêtes HTTP en Python et Bash
joblib
GitLab Repository / .gitlab-ci.yml / gitlab-runner
Dockerfile / volumes / docker-compose.yml / services.depends_on / DockerHub
Pytest
FastAPI / prometheus-fastapi-instrumentator
pydantic.BaseModel
curl
Kubernetes : Namespace / PV / PVC / ConfigMap / Service / Deployment
Prometheus : prometheus.yml / PromQL
Grafana : datasource YAML / dashboard via UI
```

## Démarrage rapide

1. Lire `START_HERE.md`.
2. Faire l'examen blanc dans `exam/sujet/` sans ouvrir `exam/correction/`.
3. Utiliser `exam/starter_project/` comme point de départ.
4. Après la simulation, comparer avec `exam/correction/reference_project/`.
5. Refaire les labs de `labs/` individuellement.
6. Utiliser `resources/study_docs/` pour les révisions ciblées.

## Structure

```text
RNCP_38919_BLOC_3_PRACTICE_LABS_PACK/
├── START_HERE.md
├── MANIFEST.md
├── sources/
├── resources/
│   └── study_docs/
├── exam/
│   ├── sujet/
│   ├── starter_project/
│   └── correction/
├── labs/
└── tools/
```

## Validation du pack

Le pack contient des utilitaires dans `tools/` pour vérifier la syntaxe Python, la structure du projet et inventorier les fichiers.
