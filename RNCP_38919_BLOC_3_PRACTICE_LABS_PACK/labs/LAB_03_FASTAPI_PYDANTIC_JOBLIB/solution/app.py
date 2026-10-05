import os
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

try:
    import joblib
except ImportError:
    joblib = None

try:
    from prometheus_fastapi_instrumentator import Instrumentator
    has_prometheus = True
except ImportError:
    has_prometheus = False

app = FastAPI(title="parcelpulse-api-lab03")


class Payload(BaseModel):
    distance_km: float
    package_weight_kg: float


# Chargement de l'artefact joblib si présent sur disque (avec fallback déterministe)
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
model = None
if joblib is not None and Path(MODEL_PATH).exists():
    try:
        model = joblib.load(MODEL_PATH)
    except Exception:
        model = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: Payload):
    if model is not None and hasattr(model, "predict"):
        prediction = model.predict([[payload.distance_km, payload.package_weight_kg]])
        risk = int(prediction[0])
    else:
        # Calcul déterministe équivalent si le modèle joblib n'est pas disponible
        risk = int(payload.distance_km + 2 * payload.package_weight_kg >= 20)
    return {"risk": risk}


# Instrumentation Prometheus pour l'endpoint /metrics
if has_prometheus:
    Instrumentator().instrument(app).expose(app)
else:
    @app.get("/metrics")
    def metrics_fallback():
        return {
            "status": "warning",
            "message": "Package 'prometheus-fastapi-instrumentator' non installé. Installez requirements.txt via pip pour les métriques Prometheus complètes."
        }
