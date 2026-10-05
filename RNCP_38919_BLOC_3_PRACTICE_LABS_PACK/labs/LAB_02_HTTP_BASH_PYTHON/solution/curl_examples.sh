#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000}"

# Vérification préalable si le serveur écoute sur l'URL
if ! curl -s --connect-timeout 1 "$API_URL/health" > /dev/null 2>&1; then
  echo "⚠️  ATTENTION : Aucun serveur HTTP ne répond actuellement sur $API_URL"
  echo "👉 Pour démarrer un serveur local de test, lancez dans un autre terminal :"
  echo "   python mock_server.py"
  echo "   (ou depuis labs/LAB_03_FASTAPI_PYDANTIC_JOBLIB/solution : uvicorn app:app --port 8000)"
  echo ""
fi

echo "=== 1. Test GET /health ==="
curl -i "$API_URL/health"

echo -e "\n=== 2. Test POST /predict ==="
curl -X POST -H "Content-Type: application/json" \
  -d '{"distance_km":12.5,"package_weight_kg":3.2}' \
  "$API_URL/predict"

echo ""
