from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories import game_repository
from app.schemas.game import GameDetailResponse, GameListItemResponse

router = APIRouter(prefix="/games")


@router.get("", response_model=list[GameListItemResponse])
def list_games(db: Session = Depends(get_db)):
    return game_repository.get_games(db)


@router.get("/{game_id}", response_model=GameDetailResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = game_repository.get_game_by_id(db, game_id)

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    return game