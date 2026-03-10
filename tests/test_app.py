from fastapi.testclient import TestClient

from multimodal_inference_service.app import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_echo() -> None:
    response = client.post("/echo", json={"text": "hello"})
    assert response.status_code == 200
    assert response.json() == {"text": "hello, content Modified!"}


def test_get_item() -> None:
    response = client.get("/items/123")
    assert response.status_code == 200
    assert response.json() == {"item_id": 123}


def test_search() -> None:
    response = client.get("/search", params={"q": "test-query"})
    assert response.status_code == 200
    assert response.json() == {"query": "test-query"}

from fastapi.testclient import TestClient

from multimodal_inference_service.app import app

client = TestClient(app)

def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_echo() -> None:
    response = client.post("/echo", json={"text": "hello"})
    assert response.status_code == 200
    assert response.json() == {"text": "hello, content Modified!"}

