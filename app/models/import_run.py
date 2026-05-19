from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ImportRun(Base):
    __tablename__ = "import_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    source: Mapped[str] = mapped_column(String(100), nullable=False, default="boardgamegeek")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="started")

    search_query: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    games_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    games_created: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    games_updated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    games_skipped: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    errors_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    errors: Mapped[list["ImportError"]] = relationship(
        back_populates="import_run",
        cascade="all, delete-orphan",
    )