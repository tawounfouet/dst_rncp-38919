# Source scope

Le pack est fondé sur le document DataScientest :

```text
Examen RNCP 38919 _ Bloc 3 - Data Engineer . DevOps.md
```

La source annonce notamment :

- épreuve de 4 heures ;
- surveillance Mereos et Google Chrome ;
- dépôt d'une archive en fin d'épreuve ;
- lecture de notebooks Jupyter ;
- `export`, `.bashrc`, variables d'environnement Python, venv ;
- requêtes HTTP avec Bash et Python, `curl` ;
- `joblib` ;
- GitLab Repository, `.gitlab-ci.yml`, Runner via `gitlab-runner` ;
- Dockerfile, volumes, Compose, `services.depends_on`, DockerHub ;
- Pytest ;
- FastAPI, `prometheus-fastapi-instrumentator`, `pydantic.BaseModel` ;
- Kubernetes : Namespace, PV, PVC, ConfigMap, Service, Deployment ;
- Prometheus : `config/prometheus.yml`, PromQL ;
- Grafana : datasource via `datasources/<source_name>.yml`, dashboard via l'UI ;
- prérequis GitLab : projet privé `dst_rncp38919_bloc_3`, clé SSH, Runner shell nommé `shell` ;
- prérequis DockerHub : compte + Personal Access Token.

Tout scénario métier, endpoint, architecture, manifest ou pipeline concret contenu dans ce pack est un **entraînement proposé**, pas une exigence officielle supplémentaire.
