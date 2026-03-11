"""API 路由与 /infer 的测试。"""

from fastapi.testclient import TestClient

from multimodal_inference_service.app import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["mode"] in ("vlm", "t2i")


def test_echo() -> None:
    response = client.post("/echo", json={"text": "hello"})
    assert response.status_code == 200
    assert response.json() == {"text": "hello, content Modified!"}


def test_infer_vlm_accepts_image_base64() -> None:
    """POST /infer 在 vlm 模式下接受 image_base64 或 image_b64。"""
    # 1x1 透明 PNG 的 base64
    tiny_png_b64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    )
    response = client.post(
        "/infer",
        json={"prompt": "describe", "image_base64": tiny_png_b64},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "vlm"
    assert "image_info" in data
    assert data["image_info"]["width"] == 1
    assert data["image_info"]["height"] == 1
