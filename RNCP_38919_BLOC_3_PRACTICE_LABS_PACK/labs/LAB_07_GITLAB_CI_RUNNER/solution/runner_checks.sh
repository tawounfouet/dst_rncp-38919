#!/usr/bin/env bash
set -euo pipefail

echo "=== 1. Statut du service GitLab Runner ==="
gitlab-runner --version || echo "⚠️ gitlab-runner non installé sur cette machine"
gitlab-runner list || true

echo "=== 2. Outils d'exécution disponibles pour le Runner Shell ==="
which python3 || which python
which pytest || echo "⚠️ pytest non présent dans le PATH global (sera exécuté via le venv)"
docker --version || echo "⚠️ Docker daemon non accessible"
