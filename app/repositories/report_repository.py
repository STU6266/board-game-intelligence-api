from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.game import Game


def get_games_for_reports(db: Session) -> list[Game]:
    statement = (
        select(Game)
        .options(selectinload(Game.rating))
        .order_by(Game.name.asc())
    )

    return list(db.scalars(statement).all())