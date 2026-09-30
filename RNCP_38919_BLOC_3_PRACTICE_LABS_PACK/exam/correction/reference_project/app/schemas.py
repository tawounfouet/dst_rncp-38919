from pydantic import BaseModel


class PredictionRequest(BaseModel):
    distance_km: float
    package_weight_kg: float


class PredictionResponse(BaseModel):
    risk: int
