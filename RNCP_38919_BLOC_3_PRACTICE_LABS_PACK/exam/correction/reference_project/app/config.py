import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_NAME = os.getenv("APP_NAME", "parcelpulse-api")
APP_ENV = os.getenv("APP_ENV", "development")
API_PORT = int(os.getenv("API_PORT", "8000"))


def resolve_model_path(raw_path: str) -> str:
    """Resout MODEL_PATH contre la racine du projet si le chemin est relatif.

    MODEL_PATH vaut "models/model.joblib" par defaut. Un chemin relatif n'est
    interprete que depuis le repertoire courant : l'API echoue donc au demarrage
    des que le CWD n'est plus la racine du projet (pytest lance depuis le
    dossier parent, job CI, IDE, script appele par son chemin absolu).

    Les chemins absolus sont conserves tels quels, ce qui couvre les
    environnements conteneurises : "/models/model.joblib" sous Docker Compose
    (volume ./models:/models:ro) et sous Kubernetes (PVC monte sur /models).
    """
    path = Path(raw_path)
    if path.is_absolute():
        return str(path)
    return str(PROJECT_ROOT / path)


MODEL_PATH = resolve_model_path(os.getenv("MODEL_PATH", "models/model.joblib"))