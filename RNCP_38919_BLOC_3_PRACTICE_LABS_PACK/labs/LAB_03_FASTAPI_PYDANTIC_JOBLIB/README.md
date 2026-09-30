# LAB 03 — FastAPI, Pydantic et joblib

## Mission

Construire :

```text
GET /health
POST /predict
GET /metrics
```

Le POST reçoit `distance_km` et `package_weight_kg` via `BaseModel` et utilise un artefact joblib.
