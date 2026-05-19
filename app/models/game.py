from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bgg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    year_published: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    min_players: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_players: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    playing_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    min_playtime: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_playtime: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    min_age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    rating: Mapped["Rating"] = relationship(
        back_populates="game",
        uselist=False,
        cascade="all, delete-orphan",
    )

    categories: Mapped[list["Category"]] = relationship(
        secondary="game_categories",
        back_populates="games",
    )

    mechanics: Mapped[list["Mechanic"]] = relationship(
        secondary="game_mechanics",
        back_populates="games",
    )
    