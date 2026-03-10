from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel

from multimodal_inference_service.config import get_service_mode

app = FastAPI()

class Item(BaseModel):
    text: str

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "multimodal-inference-service is running"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok",
            "mode": get_service_mode(),
    }

@app.post("/echo")
async def echo(item: Item):
    item.text += ", content Modified!"
    return item

# @app.get("/items/{item_id}")
# async def get_item(item_id: int) -> dict[str, int]:
#     return {"item_id": item_id}


# @app.get("/search")
# async def search(q: str) -> dict[str, str]:
#     return {"query": q}

@app.websocket("/ws")
async def websocket_echo(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        await websocket.send_text(f"echo: {message}")

@app.post("/infer")
async def infer(item: Item) -> dict[str, str]:
    mode = get_service_mode()

    if mode == "vlm":
        return{
            "mode": mode,
            "result": f"vlm placeholder: {item.text}",
        }
    
    if mode == "t2i":
        return {
            "mode": mode,
            "result": f"t2i placeholder: {item.text}",
        }
    
    raise HTTPException(status_code=500, detail="Invalid service mode")

