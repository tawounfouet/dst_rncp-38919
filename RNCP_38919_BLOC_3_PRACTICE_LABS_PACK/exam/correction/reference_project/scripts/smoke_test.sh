#!/usr/bin/env bash
set -euo pipefail
API_URL="${API_URL:-http://localhost:8000}"
curl -fsS "$API_URL/health"
echo
curl -fsS -X POST \
  -H "Content-Type: application/json" \
  -d '{"distance_km":12.5,"package_weight_kg":3.2}' \
  "$API_URL/predict"
echo
curl -fsS "$API_URL/metrics" >/dev/null
echo "Smoke tests OK"
