from fastapi import FastAPI
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