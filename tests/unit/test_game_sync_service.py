from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models import Game, ImportError, ImportRun

from app.services.game_sync_service import (
    sync_game_from_bgg_api,
    sync_game_from_xml_file,
)

SAMPLE_FILE = Path("sample_data/bgg_thing_sample.xml")


@pytest.fixture
def db_session(tmp_path: Path) -> Generator[Session, None, None]:
    database_file = tmp_path / "sync_test.db"
    engine = create_engine(f"sqlite+pysqlite:///{database_file}")

    Base.metadata.create_all(bind=engine)

    testing_session_local = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    db = testing_session_local()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_sync_creates_game_and_import_run(db_session: Session) -> None:
    result = sync_game_from_xml_file(db_session, SAMPLE_FILE)

    game = db_session.scalar(
        select(Game).where(Game.bgg_id == 999001)
    )
    import_run = db_session.scalar(
        select(ImportRun).where(ImportRun.id == result.import_run_id)
    )

    assert result.status == "completed"
    assert result.games_created == 1
    assert result.games_updated == 0
    assert result.errors_count == 0

    assert game is not None
    assert game.name == "Sample Quest Island"
    assert game.rating is not None
    assert game.rating.average_rating == 7.62
    assert {category.name for category in game.categories} == {
        "Adventure",
        "Deduction",
    }
    assert {mechanic.name for mechanic in game.mechanics} == {
        "Cooperative Game",
        "Dice Rolling",
    }

    assert import_run is not None
    assert import_run.status == "completed"


def test_sync_updates_existing_game_instead_of_creating_duplicate(
    db_session: Session,
) -> None:
    first_result = sync_game_from_xml_file(db_session, SAMPLE_FILE)
    second_result = sync_game_from_xml_file(db_session, SAMPLE_FILE)

    games = list(
        db_session.scalars(
            select(Game).where(Game.bgg_id == 999001)
        ).all()
    )

    assert first_result.games_created == 1
    assert second_result.games_created == 0
    assert second_result.games_updated == 1
    assert len(games) == 1


def test_sync_skips_invalid_data_and_stores_import_error(
    db_session: Session,
    tmp_path: Path,
) -> None:
    invalid_xml = SAMPLE_FILE.read_text(encoding="utf-8").replace(
        '<minplayers value="2" />',
        '<minplayers value="6" />',
    )

    invalid_file = tmp_path / "invalid_game.xml"
    invalid_file.write_text(invalid_xml, encoding="utf-8")

    result = sync_game_from_xml_file(db_session, invalid_file)

    game = db_session.scalar(
        select(Game).where(Game.bgg_id == 999001)
    )
    import_error = db_session.scalar(select(ImportError))

    assert result.status == "completed_with_errors"
    assert result.games_created == 0
    assert result.games_skipped == 1
    assert result.errors_count == 1

    assert game is None
    assert import_error is not None
    assert import_error.error_type == "data_quality"
    assert "players" in import_error.error_message


def test_sync_logs_technical_error_when_xml_file_does_not_exist(
    db_session: Session,
    tmp_path: Path,
) -> None:
    missing_file = tmp_path / "missing_game.xml"

    result = sync_game_from_xml_file(db_session, missing_file)

    import_error = db_session.scalar(select(ImportError))

    assert result.status == "failed"
    assert result.games_skipped == 1
    assert result.errors_count == 1

    assert import_error is not None
    assert import_error.error_type == "sync_error"

class FakeBggClient:
    def get_game_xml(self, bgg_id: int) -> str:
        assert bgg_id == 999001
        return SAMPLE_FILE.read_text(encoding="utf-8")


def test_sync_from_bgg_api_stores_game_using_client_response(
    db_session: Session,
) -> None:
    result = sync_game_from_bgg_api(
        db_session,
        999001,
        client=FakeBggClient(),
    )

    game = db_session.scalar(
        select(Game).where(Game.bgg_id == 999001)
    )

    assert result.status == "completed"
    assert result.games_created == 1
    assert game is not None
    assert game.name == "Sample Quest Island"