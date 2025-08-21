from fastapi.testclient import TestClient
import importlib


def test_health_endpoint():
    module = importlib.import_module("src.api.main")
    app = getattr(module, "app")
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
