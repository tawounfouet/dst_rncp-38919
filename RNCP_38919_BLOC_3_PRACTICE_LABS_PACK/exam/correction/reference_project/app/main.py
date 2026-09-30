from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import APP_NAME, MODEL_PATH
from app.model import load_model
from app.schemas import PredictionRequest, PredictionResponse

app = FastAPI(title=APP_NAME)
model = load_model(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok", "app": APP_NAME}


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    prediction = model.predict([[payload.distance_km, payload.package_weight_kg]])
    return PredictionResponse(risk=int(prediction[0]))


Instrumentator().instrument(app).expose(app)
