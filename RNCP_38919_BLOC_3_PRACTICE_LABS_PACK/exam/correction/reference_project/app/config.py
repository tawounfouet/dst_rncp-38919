import os

APP_NAME = os.getenv("APP_NAME", "parcelpulse-api")
APP_ENV = os.getenv("APP_ENV", "development")
API_PORT = int(os.getenv("API_PORT", "8000"))
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")
