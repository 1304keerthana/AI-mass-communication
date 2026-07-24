from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.router import router
from app.core.config import get_settings
from app.database.base import Base
from app.database.session import engine

settings = get_settings()
app = FastAPI(title="AI-Based Multilingual Mass Communication Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


app.include_router(router, prefix="/api/v1")
