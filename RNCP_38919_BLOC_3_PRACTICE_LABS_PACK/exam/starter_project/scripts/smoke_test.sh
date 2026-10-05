#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000}"

echo "=== Lancement des Smoke Tests sur $API_URL ==="

# TODO 1: Décommenter pour tester /health
# curl -fsS "$API_URL/health"
# echo

# TODO 2: Décommenter pour tester /predict avec un payload valide
# curl -fsS -X POST \
#   -H "Content-Type: application/json" \
#   -d '{"distance_km":12.5,"package_weight_kg":3.2}' \
#   "$API_URL/predict"
# echo

# TODO 3: Décommenter pour tester /metrics
# curl -fsS "$API_URL/metrics" >/dev/null
# echo "Smoke tests OK"
