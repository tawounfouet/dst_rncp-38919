from pathlib import Path

from fastapi.testclient import TestClient

from app.config import MODEL_PATH, resolve_model_path
from app.demo_model import DemoRiskModel
from app.main import app

client = TestClient(app)


def test_model_path_is_absolute():
    """Un MODEL_PATH relatif casse l'import de l'API hors racine du projet."""
    assert Path(MODEL_PATH).is_absolute()


def test_resolve_model_path_keeps_absolute_paths():
    """Docker/Kubernetes fournissent un chemin absolu : il doit rester intact."""
    assert resolve_model_path("/models/model.joblib") == "/models/model.joblib"


def test_resolve_model_path_resolves_relative_paths():
    assert resolve_model_path("models/model.joblib") == str(
        Path(__file__).resolve().parent.parent / "models" / "model.joblib"
    )


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "parcelpulse-api"}


def test_model_threshold_low_risk():
    """score = 12.5 + 2 * 3.2 = 18.9 < 20 -> risque 0."""
    assert DemoRiskModel().predict([[12.5, 3.2]]) == [0]


def test_model_threshold_high_risk():
    """score = 20 + 2 * 5 = 30 >= 20 -> risque 1."""
    assert DemoRiskModel().predict([[20, 5]]) == [1]


def test_model_threshold_boundary():
    """score = 18 + 2 * 1 = 20 : le seuil est inclus (>=)."""
    assert DemoRiskModel().predict([[18, 1]]) == [1]


def test_predict_valid_low_risk():
    response = client.post(
        "/predict",
        json={"distance_km": 12.5, "package_weight_kg": 3.2},
    )
    assert response.status_code == 200
    assert response.json() == {"risk": 0}


def test_predict_valid_high_risk():
    response = client.post(
        "/predict",
        json={"distance_km": 20, "package_weight_kg": 5},
    )
    assert response.status_code == 200
    assert response.json() == {"risk": 1}


def test_predict_invalid_type():
    response = client.post(
        "/predict",
        json={"distance_km": "abc", "package_weight_kg": 3.2},
    )
    assert response.status_code == 422


def test_predict_missing_field():
    response = client.post("/predict", json={"distance_km": 12.5})
    assert response.status_code == 422


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text