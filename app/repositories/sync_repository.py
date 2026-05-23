from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.import_run import ImportRun


def get_import_runs(db: Session) -> list[ImportRun]:
    statement = select(ImportRun).order_by(ImportRun.started_at.desc())

    return list(db.scalars(statement).all())


def get_import_run_by_id(db: Session, import_run_id: int) -> ImportRun | None:
    statement = (
        select(ImportRun)
        .where(ImportRun.id == import_run_id)
        .options(selectinload(ImportRun.errors))
    )

    return db.scalar(statement)