from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def health() -> dict[str, str]:
    return {"message": "multimodal-inference-service is running"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
