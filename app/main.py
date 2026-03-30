from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
import app.models

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/health/db")
def health_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }