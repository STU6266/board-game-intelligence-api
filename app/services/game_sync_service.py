from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category, Game, ImportError, ImportRun, Mechanic, Rating
from app.schemas.bgg import BggGameData
from app.schemas.sync import SyncResult
from app.services.bgg_parser import parse_bgg_thing_file
from app.services.data_quality_service import validate_bgg_game_data


def _get_or_create_category(db: Session, name: str) -> Category:
    category = db.scalar(select(Category).where(Category.name == name))

    if category is not None:
        return category

    category = Category(name=name)
    db.add(category)
    db.flush()

    return category


def _get_or_create_mechanic(db: Session, name: str) -> Mechanic:
    mechanic = db.scalar(select(Mechanic).where(Mechanic.name == name))

    if mechanic is not None:
        return mechanic

    mechanic = Mechanic(name=name)
    db.add(mechanic)
    db.flush()

    return mechanic


def _apply_game_data(db: Session, game: Game, data: BggGameData) -> None:
    game.name = data.name
    game.year_published = data.year_published
    game.description = data.description
    game.min_players = data.min_players
    game.max_players = data.max_players
    game.playing_time = data.playing_time
    game.min_playtime = data.min_playtime
    game.max_playtime = data.max_playtime
    game.min_age = data.min_age
    game.last_synced_at = datetime.now(timezone.utc)

    game.categories = [
        _get_or_create_category(db, name)
        for name in data.categories
    ]

    game.mechanics = [
        _get_or_create_mechanic(db, name)
        for name in data.mechanics
    ]

    if data.rating is None:
        game.rating = None
        return

    if game.rating is None:
        game.rating = Rating()

    game.rating.average_rating = data.rating.average_rating
    game.rating.bayes_average = data.rating.bayes_average
    game.rating.users_rated = data.rating.users_rated
    game.rating.average_weight = data.rating.average_weight
    game.rating.rank_overall = data.rating.rank_overall


def _create_sync_result(import_run: ImportRun) -> SyncResult:
    return SyncResult(
        import_run_id=import_run.id,
        status=import_run.status,
        games_found=import_run.games_found,
        games_created=import_run.games_created,
        games_updated=import_run.games_updated,
        games_skipped=import_run.games_skipped,
        errors_count=import_run.errors_count,
        message=import_run.message,
    )


def sync_game_from_xml_file(db: Session, file_path: str | Path) -> SyncResult:
    import_run = ImportRun(
        source="local_xml_fixture",
        status="started",
        message=f"Sync started from {file_path}.",
    )
    db.add(import_run)
    db.flush()

    try:
        data = parse_bgg_thing_file(file_path)
        import_run.games_found = 1

        quality_result = validate_bgg_game_data(data)

        if not quality_result.is_valid:
            import_run.status = "completed_with_errors"
            import_run.games_skipped = 1
            import_run.errors_count = len(quality_result.errors)
            import_run.finished_at = datetime.now(timezone.utc)
            import_run.message = "Game was not stored because data quality validation failed."

            for issue in quality_result.errors:
                db.add(
                    ImportError(
                        import_run_id=import_run.id,
                        bgg_id=data.bgg_id,
                        error_type="data_quality",
                        error_message=f"{issue.field}: {issue.message}",
                    )
                )

            db.commit()
            db.refresh(import_run)

            return _create_sync_result(import_run)

        existing_game = db.scalar(
            select(Game).where(Game.bgg_id == data.bgg_id)
        )

        if existing_game is None:
            game = Game(
                bgg_id=data.bgg_id,
                name=data.name,
            )
            db.add(game)
            _apply_game_data(db, game, data)
            import_run.games_created = 1
        else:
            _apply_game_data(db, existing_game, data)
            import_run.games_updated = 1

        import_run.status = "completed"
        import_run.finished_at = datetime.now(timezone.utc)
        import_run.message = "Game synchronized successfully."

        db.commit()
        db.refresh(import_run)

        return _create_sync_result(import_run)

    except Exception as exc:
        db.rollback()

        failed_run = ImportRun(
            source="local_xml_fixture",
            status="failed",
            finished_at=datetime.now(timezone.utc),
            games_skipped=1,
            errors_count=1,
            message="Sync failed before the game could be stored.",
        )
        db.add(failed_run)
        db.flush()

        db.add(
            ImportError(
                import_run_id=failed_run.id,
                error_type="sync_error",
                error_message=str(exc),
            )
        )

        db.commit()
        db.refresh(failed_run)

        return _create_sync_result(failed_run)