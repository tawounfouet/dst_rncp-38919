# LAB 06 — Docker Compose, volumes et depends_on

Construire une stack :

```text
app
prometheus
grafana
```

Contraintes :

- volume `/models` ;
- `prometheus depends_on app` ;
- `grafana depends_on prometheus`.

## Lancement & Validation de la stack

Pour lancer et valider la stack multi-services complète (API + Prometheus + Grafana) :
```bash
# Se placer dans le projet de référence complet
cd ../../exam/correction/reference_project

# Démarrer l'ensemble des conteneurs
docker compose up --build -d

# Vérifier l'état des conteneurs
docker compose ps

# Tester les flux
curl -i http://localhost:8000/health
curl -i http://localhost:9090/-/healthy
curl -i http://localhost:3000/api/health

# Arrêter la stack
docker compose down
```
