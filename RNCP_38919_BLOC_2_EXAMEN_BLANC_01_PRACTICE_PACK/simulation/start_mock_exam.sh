#!/usr/bin/env bash
#
# Prépare un workspace candidat propre pour la simulation 4 h.
#
# Usage :
#   ./start_mock_exam.sh            # crée candidate_workspace/ (échoue s'il existe)
#   ./start_mock_exam.sh --force    # réinitialise candidate_workspace/
#   ./start_mock_exam.sh --no-docker
#
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PACK="$(cd "$HERE/.." && pwd)"
STARTER="$PACK/exam/starter_project"
WS="$HERE/candidate_workspace"

FORCE=0
WITH_DOCKER=1
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --no-docker) WITH_DOCKER=0 ;;
    *) echo "Argument inconnu : $arg" >&2; exit 2 ;;
  esac
done

if [ ! -d "$STARTER" ]; then
  echo "Starter introuvable : $STARTER" >&2
  exit 1
fi

if [ -d "$WS" ] && [ "$FORCE" -ne 1 ]; then
  echo "Le workspace existe déjà : $WS"
  echo "Relance avec --force pour le réinitialiser (perte du travail en cours)."
  exit 1
fi

rm -rf "$WS"
cp -R "$STARTER" "$WS"
rm -rf "$WS/.venv" "$WS/src/__pycache__" "$WS/tests/__pycache__" "$WS/.pytest_cache"
mkdir -p "$WS/notebooks" "$WS/models" "$WS/data/processed"

echo "==> Workspace créé : $WS"
echo "==> Création du venv + installation des dépendances..."
(
  cd "$WS"
  python3 -m venv .venv
  # shellcheck disable=SC1091
  . .venv/bin/activate
  python -m pip install -q --upgrade pip
  python -m pip install -q -r requirements.txt
  [ -f .env ] || cp .env.example .env
)

if [ "$WITH_DOCKER" -eq 1 ] && command -v docker >/dev/null 2>&1; then
  echo "==> Démarrage de la base (docker compose up -d)..."
  ( cd "$WS" && docker compose up -d >/dev/null 2>&1 || true )
  sleep 8
  ( cd "$WS" && docker compose ps || true )
fi

START="$(date '+%H:%M')"
END="$(date -v+4H '+%H:%M' 2>/dev/null || date -d '+4 hours' '+%H:%M' 2>/dev/null || echo '??')"

cat <<EOF

============================================================
 SIMULATION 4 H PRÊTE
============================================================
Workspace : $WS
Départ    : $START     Fin imposée : $END (STOP CODING)

À faire maintenant :
  cd "$WS"
  source .venv/bin/activate
  # puis ouvre le sujet :
  #   $PACK/exam/sujet/11_RNCP_38919_BLOC_2_EXAMEN_BLANC_01.md

À la fin, auto-correction :
  cd "$HERE"
  python grade.py candidate_workspace --with-db
============================================================
EOF
