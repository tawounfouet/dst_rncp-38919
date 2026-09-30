from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

class Payload(BaseModel):
    distance_km: float
    package_weight_kg: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: Payload):
    risk = int(payload.distance_km + 2 * payload.package_weight_kg >= 20)
    return {"risk": risk}

Instrumentator().instrument(app).expose(app)
