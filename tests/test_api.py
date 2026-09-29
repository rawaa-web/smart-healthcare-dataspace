"""S4 smoke tests — the FastAPI gateway is a working stub (owner S4)."""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    """GET /health answers 200 with the mock-mode flag."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert isinstance(body["mock_mode"], bool)


def test_metrics_roundtrip():
    """POST /metrics stores a round, GET /metrics returns it."""
    metric = {"round": 1, "accuracy": 0.75, "loss": 0.5, "time": 1.2}
    assert client.post("/metrics", json=metric).status_code == 200
    assert metric in client.get("/metrics").json()
