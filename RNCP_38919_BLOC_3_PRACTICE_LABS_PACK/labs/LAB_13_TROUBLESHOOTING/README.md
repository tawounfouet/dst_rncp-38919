# LAB 13 — Troubleshooting

Pour chaque panne, identifier la couche la plus basse cassée avant de modifier les couches suivantes.

## Scénarios

1. `MODEL_PATH` invalide.
2. Pytest rouge.
3. Port Docker incorrect.
4. Runner GitLab offline.
5. Image DockerHub tag inexistante.
6. Deployment selector différent des Pod labels.
7. Service selector incorrect.
8. PVC `Pending`.
9. Prometheus target `DOWN`.
10. Grafana datasource pointant vers `localhost:9090` dans Compose.

Documenter pour chaque cas : symptôme → preuve → cause → correction.
