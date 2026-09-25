from fastapi.testclient import TestClient
from service import app


def test_http_contract_and_domain():
    c = TestClient(app)
    assert c.get("/health/live").status_code == 200
    r = c.post("/v1/workflows", json={"key": "integration", "payload": {"steps": ["a"]}})
    assert r.status_code == 200, r.text
