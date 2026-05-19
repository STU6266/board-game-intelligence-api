from fastapi import FastAPI

from app.api.v1.endpoints.health import router as health_router

app = FastAPI(
    title="Board Game Intelligence API",
    description="Backend and data integration API for board game data.",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api/v1", tags=["Health"])


@app.get("/")
def root():
    return {
        "message": "Board Game Intelligence API",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


