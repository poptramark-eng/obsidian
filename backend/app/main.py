from fastapi import FastAPI

app = FastAPI(
    title="Kenyan CBE Assessment Management API",
    version="0.1.0",
    description="Multi-tenant CBE assessment, learner portfolio and payment services.",
)


@app.get("/health", tags=["operations"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
