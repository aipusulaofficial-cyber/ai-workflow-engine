from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis import strategies as st

from service import app

client = TestClient(app)


def test_contract():
    assert client.get("/health/live").status_code == 200


@given(st.text(min_size=1, max_size=32).filter(lambda value: value.strip()))
def test_property(key: str):
    response = client.post(
        "/v1/workflows",
        json={"key": key, "payload": {"steps": ["a"]}},
    )
    assert response.status_code == 200, response.text
    assert response.json()["state"] == "running"


def test_rejects_empty_steps():
    response = client.post(
        "/v1/workflows",
        json={"key": "workflow-1", "payload": {"steps": []}},
    )
    assert response.status_code == 422


def test_rejects_oversized_workflow():
    response = client.post(
        "/v1/workflows",
        json={
            "key": "workflow-1",
            "payload": {"steps": ["step"] * 1_001},
        },
    )
    assert response.status_code == 422


def test_rejects_blank_key():
    response = client.post(
        "/v1/workflows",
        json={"key": "   ", "payload": {"steps": ["step"]}},
    )
    assert response.status_code == 422
