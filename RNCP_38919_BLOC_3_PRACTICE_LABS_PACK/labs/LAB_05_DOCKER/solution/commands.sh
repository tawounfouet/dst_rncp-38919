#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="parcelpulse-api:latest"
CONTAINER_NAME="parcelpulse-api-container"

echo "=== 1. Construction de l'image Docker ==="
docker build -t "$IMAGE_NAME" .

echo "=== 2. Démarrage du conteneur en arrière-plan ==="
docker run -d --rm -p 8000:8000 --name "$CONTAINER_NAME" "$IMAGE_NAME"

echo "=== 3. Vérification des conteneurs actifs ==="
docker ps --filter "name=$CONTAINER_NAME"

echo "=== 4. Test HTTP de l'endpoint /health ==="
sleep 2
curl -i http://localhost:8000/health

echo -e "\n=== 5. Logs du conteneur ==="
docker logs "$CONTAINER_NAME"

echo -e "\n=== 6. Arrêt du conteneur de test ==="
docker stop "$CONTAINER_NAME"
