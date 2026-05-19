from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "board-game-intelligence-api",
    }


@router.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "database": "connected",
    }