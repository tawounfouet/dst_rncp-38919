#!/usr/bin/env bash
# LAB 02 — Starter : Requêtes HTTP avec cURL
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000}"

echo "=== 1. Test GET /health ==="
# TODO : Effectuer une requête GET avec curl affichant les en-têtes (-i)
# curl -i "$API_URL/health"

echo -e "\n=== 2. Test POST /predict ==="
# TODO : Effectuer une requête POST avec curl en envoyant un JSON (Content-Type: application/json)
# curl -X POST -H "Content-Type: application/json" \
#   -d '{"distance_km":12.5,"package_weight_kg":3.2}' \
#   "$API_URL/predict"

echo ""
