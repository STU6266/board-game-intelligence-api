from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.import_run import ImportRun
    
class ImportError(Base):
    __tablename__ = "import_errors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    import_run_id: Mapped[int] = mapped_column(
        ForeignKey("import_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    bgg_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    error_type: Mapped[str] = mapped_column(String(100), nullable=False)
    error_message: Mapped[str] = mapped_column(Text, nullable=False)
    raw_payload: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    import_run: Mapped["ImportRun"] = relationship(back_populates="errors")