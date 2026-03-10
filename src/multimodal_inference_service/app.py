from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "multimodal-inference-service is running"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

class Item(BaseModel):
    text: str

@app.post("/echo")
async def echo(item: Item):
    item.text += ", content Modified!"
    return item

@app.get("/items/{item_id}")
async def get_item(item_id: int) -> dict[str, int]:
    return {"item_id": item_id}


@app.get("/search")
async def search(q: str) -> dict[str, str]:
    return {"query": q}

@app.websocket("/ws")
async def websocket_echo(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        await websocket.send_text(f"echo: {message}")

