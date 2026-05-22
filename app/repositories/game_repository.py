from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.game import Game


def get_games(db: Session) -> list[Game]:
    statement = (
        select(Game)
        .options(selectinload(Game.rating))
        .order_by(Game.name.asc())
    )

    return list(db.scalars(statement).all())


def get_game_by_id(db: Session, game_id: int) -> Game | None:
    statement = (
        select(Game)
        .where(Game.id == game_id)
        .options(
            selectinload(Game.rating),
            selectinload(Game.categories),
            selectinload(Game.mechanics),
        )
    )

    return db.scalar(statement)