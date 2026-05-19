from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    average_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bayes_average: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    users_rated: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    average_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rank_overall: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    game: Mapped["Game"] = relationship(back_populates="rating")
    