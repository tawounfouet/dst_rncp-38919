#!/usr/bin/env bash
# Note : Pour que l'export et l'activation du venv persistent dans votre terminal actuel,
# exécutez ce script avec 'source ./commands.sh' (ou '. ./commands.sh') au lieu de './commands.sh'.

export APP_ENV=practice
export API_PORT=8000

echo "APP_ENV=$APP_ENV"
echo "API_PORT=$API_PORT"

# Création et activation de l'environnement virtuel
python3 -m venv .venv 2>/dev/null || python -m venv .venv
source .venv/bin/activate

echo "Python actif : $(which python)"
