#!/usr/bin/env bash
set -euo pipefail

DOCKER_USER="${DOCKER_USER:-${1:-}}"
if [ -z "$DOCKER_USER" ]; then
    read -r -p "Entrez votre identifiant DockerHub : " DOCKER_USER
fi

echo "=== Authentification et Publication DockerHub pour : $DOCKER_USER ==="
docker build -t parcelpulse-api:latest .
docker login
docker tag parcelpulse-api:latest "${DOCKER_USER}/parcelpulse-api:latest"
docker push "${DOCKER_USER}/parcelpulse-api:latest"
docker pull "${DOCKER_USER}/parcelpulse-api:latest"
echo "Image ${DOCKER_USER}/parcelpulse-api:latest publiée et vérifiée avec succès."
