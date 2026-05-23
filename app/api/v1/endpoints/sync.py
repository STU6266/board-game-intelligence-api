from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories import sync_repository
from app.schemas.sync import (
    ImportRunDetailResponse,
    ImportRunResponse,
    SyncResult,
)
from app.services.game_sync_service import sync_game_from_bgg_api

router = APIRouter()


@router.post("/sync/games/{bgg_id}", response_model=SyncResult)
def sync_game_from_bgg(
    bgg_id: int,
    db: Session = Depends(get_db),
):
    if bgg_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="bgg_id must be a positive integer.",
        )

    return sync_game_from_bgg_api(db, bgg_id)


@router.get("/import-runs", response_model=list[ImportRunResponse])
def list_import_runs(db: Session = Depends(get_db)):
    return sync_repository.get_import_runs(db)


@router.get("/import-runs/{import_run_id}", response_model=ImportRunDetailResponse)
def get_import_run(
    import_run_id: int,
    db: Session = Depends(get_db),
):
    import_run = sync_repository.get_import_run_by_id(db, import_run_id)

    if import_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import run not found.",
        )

    return import_run