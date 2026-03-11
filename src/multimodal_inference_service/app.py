"""多模态推理服务：HTTP + WebSocket，支持 vlm / t2i 模式。"""

from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel, model_validator

from multimodal_inference_service.config import get_service_mode
from multimodal_inference_service.vlm_pipeline import (
    decode_base64_image,
    get_image_info,
)

app = FastAPI()


class Item(BaseModel):
    text: str


class VLMRequest(BaseModel):
    """支持 image_b64 或 image_base64，任一带有效内容即可。"""
    prompt: str
    image_b64: str = ""
    image_base64: str = ""

    @model_validator(mode="after")
    def ensure_image(self) -> "VLMRequest":
        image = self.image_b64 or self.image_base64
        if not image or not image.strip():
            raise ValueError("Either image_b64 or image_base64 must be non-empty.")
        object.__setattr__(self, "image_b64", image)
        return self

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "multimodal-inference-service is running"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "mode": get_service_mode(),
    }

@app.post("/echo")
async def echo(item: Item) -> Item:
    item.text += ", content Modified!"
    return item


@app.websocket("/ws")
async def websocket_echo(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        await websocket.send_text(f"echo: {message}")

@app.post("/infer")
async def infer(request: VLMRequest) -> dict[str, object]:
    mode = get_service_mode()

    if mode == "vlm":
        try:
            image = decode_base64_image(request.image_b64)
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to decode base64 image: {exc}",
            )
        image_info = get_image_info(image)
        return {
            "mode": mode,
            "prompt": request.prompt,
            "image_info": image_info,
            "result": f"vlm placeholder: {request.prompt}",
        }
    
    if mode == "t2i":
        return {
            "mode": mode,
            "result": f"t2i placeholder: {request.prompt}",
        }
    
    raise HTTPException(status_code=500, detail="Invalid service mode")

