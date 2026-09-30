from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "parcelpulse-api"}


def test_predict_valid():
    response = client.post(
        "/predict",
        json={"distance_km": 12.5, "package_weight_kg": 3.2},
    )
    assert response.status_code == 200
    assert "risk" in response.json()


def test_predict_invalid():
    response = client.post(
        "/predict",
        json={"distance_km": "abc", "package_weight_kg": 3.2},
    )
    assert response.status_code != 200


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
