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

app = FastAPI(title="parcelpulse-api-lab03-starter")

# 1. Définir le schéma Pydantic pour la requête
class Payload(BaseModel):
    distance_km: float
    package_weight_kg: float

# 2. Charger le modèle joblib
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
model = None
if joblib is not None and Path(MODEL_PATH).exists():
    try:
        model = joblib.load(MODEL_PATH)
    except Exception:
        model = None

# TODO: Endpoint GET /health retournant {"status": "ok"}
@app.get("/health")
def health():
    return {"status": "ok"}

# TODO: Endpoint POST /predict recevant payload: Payload et retournant {"risk": int}
@app.post("/predict")
def predict(payload: Payload):
    if model is not None and hasattr(model, "predict"):
        pred = model.predict([[payload.distance_km, payload.package_weight_kg]])
        return {"risk": int(pred[0])}
    # Fallback si modèle non disponible
    risk = int(payload.distance_km + 2 * payload.package_weight_kg >= 20)
    return {"risk": risk}

# 3. Exposer les métriques Prometheus sur GET /metrics
if has_prometheus:
    Instrumentator().instrument(app).expose(app)
else:
    @app.get("/metrics")
    def metrics():
        return {"status": "warning", "message": "Installez prometheus-fastapi-instrumentator pour les métriques complètes"}
