from fastapi import FastAPI

from app.config import APP_NAME

app = FastAPI(title=APP_NAME)


# TODO 1: définir GET /health
# TODO 2: définir PredictionRequest avec pydantic.BaseModel dans app/schemas.py
# TODO 3: charger models/model.joblib avec joblib
# TODO 4: définir POST /predict
# TODO 5: ajouter prometheus-fastapi-instrumentator et exposer /metrics
