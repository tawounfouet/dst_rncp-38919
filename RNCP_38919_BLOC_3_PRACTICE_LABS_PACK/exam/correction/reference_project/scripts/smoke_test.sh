#!/usr/bin/env bash
#
# Smoke test HTTP de l'API ParcelPulse.
#
#   bash scripts/smoke_test.sh
#
# Verifie les 3 endpoints sur les 2 regimes du modele (risk 0 et risk 1),
# plus le rejet d'un payload invalide.
#
# Regle du modele (app/demo_model.py) :
#   score = distance_km + 2 * package_weight_kg ;  risk = 1 si score >= 20
#
# Variables d'environnement optionnelles :
#   API_URL  URL de base de l'API (défaut : http://localhost:8000)
#
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000}"
TIMEOUT="${TIMEOUT:-10}"

FAILURES=0
CHECKS=0

# --- Helpers ---------------------------------------------------------------
check() {
    local label="$1" expected="$2" actual="$3"
    CHECKS=$((CHECKS + 1))
    if [ "$actual" = "$expected" ]; then
        printf '  \033[32mOK\033[0m    %-42s %s\n' "$label" "$actual"
    else
        printf '  \033[31mFAIL\033[0m  %-42s attendu=%s obtenu=%s\n' "$label" "$expected" "$actual"
        FAILURES=$((FAILURES + 1))
    fi
}

# Extrait la valeur d'une clé d'un objet JSON sans dépendre de jq.
# Gère les valeurs chaînes ("status":"ok") et numériques ("risk":0).
json_value() {
    tr -d ' \n' <<<"$2" | sed -n "s/.*\"$1\":\"\{0,1\}\([^\",}]*\)\"\{0,1\}.*/\1/p"
}

request() {
    curl -sS --max-time "$TIMEOUT" -w '\n%{http_code}' "$@"
}

# --- Verification prealable -----------------------------------------------
printf '\n\033[1m=== Smoke test ParcelPulse ===\033[0m\n'
printf 'API cible : %s\n' "$API_URL"

if ! curl -fsS --max-time "$TIMEOUT" "$API_URL/health" >/dev/null 2>&1; then
    cat <<EOF

\033[31m[ECHEC] L'API ne repond pas sur $API_URL\033[0m

Verifiez que le deploiement tourne et que le tunnel est ouvert :
    kubectl get pods -n parcelpulse
    kubectl port-forward svc/parcelpulse-api-service 8000:8000 -n parcelpulse

Pour pointer une autre URL : API_URL=http://host:port bash scripts/smoke_test.sh
EOF
    exit 1
fi

# --- 1. GET /health --------------------------------------------------------
printf '\n\033[1m=== 1. Test GET /health ===\033[0m\n'
RAW="$(request "$API_URL/health")" || RAW='
---STATUS---000'
HEALTH_BODY="${RAW%$'\n'*}"; HEALTH_STATUS="${RAW##*$'\n'}"
check "code HTTP" "200" "$HEALTH_STATUS"
check "status" "ok" "$(json_value status "$HEALTH_BODY")"
check "app" "parcelpulse-api" "$(json_value app "$HEALTH_BODY")"
printf '  corps : %s\n' "$HEALTH_BODY"

# --- 2. POST /predict : risque faible (score 18.9 < 20) -------------------
printf '\n\033[1m=== 2. Test POST /predict - risque faible (12.5 km / 3.2 kg)\033[0m\n'
RAW="$(request -X POST -H 'Content-Type: application/json' \
    -d '{"distance_km":12.5,"package_weight_kg":3.2}' "$API_URL/predict")" || RAW='
---STATUS---000'
BODY="${RAW%$'\n'*}"; STATUS="${RAW##*$'\n'}"
check "code HTTP" "200" "$STATUS"
check "risk (score=18.9 < 20)" "0" "$(json_value risk "$BODY")"
printf '  corps : %s\n' "$BODY"

# --- 3. POST /predict : risque eleve (score 30 >= 20) --------------------
printf '\n\033[1m=== 3. Test POST /predict - risque eleve (20 km / 5 kg)\033[0m\n'
RAW="$(request -X POST -H 'Content-Type: application/json' \
    -d '{"distance_km":20,"package_weight_kg":5}' "$API_URL/predict")" || RAW='
---STATUS---000'
BODY="${RAW%$'\n'*}"; STATUS="${RAW##*$'\n'}"
check "code HTTP" "200" "$STATUS"
check "risk (score=30 >= 20)" "1" "$(json_value risk "$BODY")"
printf '  corps : %s\n' "$BODY"

# --- 4. POST /predict : seuil pile (score 20) ----------------------------
printf '\n\033[1m=== 4. Test POST /predict - seuil exact (18 km / 1 kg)\033[0m\n'
RAW="$(request -X POST -H 'Content-Type: application/json' \
    -d '{"distance_km":18,"package_weight_kg":1}' "$API_URL/predict")" || RAW='
---STATUS---000'
BODY="${RAW%$'\n'*}"; STATUS="${RAW##*$'\n'}"
check "code HTTP" "200" "$STATUS"
check "risk (score=20 >= 20)" "1" "$(json_value risk "$BODY")"
printf '  corps : %s\n' "$BODY"

# --- 5. POST /predict : payload invalide rejete ---------------------------
printf '\n\033[1m=== 5. Test POST /predict - payload invalide (422 attendu)\033[0m\n'
RAW="$(request -X POST -H 'Content-Type: application/json' \
    -d '{"distance_km":"abc","package_weight_kg":3.2}' "$API_URL/predict")" || RAW='
---STATUS---000'
STATUS="${RAW##*$'\n'}"
check "code HTTP" "422" "$STATUS"

# --- 6. GET /metrics -------------------------------------------------------
printf '\n\033[1m=== 6. Test GET /metrics (exposition Prometheus)\033[0m\n'
RAW="$(request "$API_URL/metrics")" || RAW='
---STATUS---000'
BODY="${RAW%$'\n'*}"; STATUS="${RAW##*$'\n'}"
check "code HTTP" "200" "$STATUS"
if grep -q '^http_requests_total' <<<"$BODY"; then
    printf '  \033[32mOK\033[0m    %-42s %s\n' "metrique http_requests_total exposee" \
        "$(grep -m1 '^http_requests_total' <<<"$BODY" | cut -c1-60)"
else
    printf '  \033[31mFAIL\033[0m  %-42s metrique absente\n' "metrique http_requests_total"
    FAILURES=$((FAILURES + 1))
fi

# --- Bilan -----------------------------------------------------------------
printf '\n\033[1m=== Bilan ===\033[0m\n'
if [ "$FAILURES" -eq 0 ]; then
    printf '\033[32mSmoke test OK - %d verifications reussies\033[0m\n' "$CHECKS"
    exit 0
fi
printf '\033[31mSmoke test KO - %d echec(s) sur %d verifications\033[0m\n' "$FAILURES" "$CHECKS"
exit 1