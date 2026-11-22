from fastapi.testclient import TestClient

from project1.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_metrics() -> None:
    client.get("/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests" in response.text or "http_request" in response.text
