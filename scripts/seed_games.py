from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Category, Game, Mechanic, Rating


def get_or_create_category(db: Session, name: str) -> Category:
    category = db.scalar(select(Category).where(Category.name == name))

    if category is not None:
        return category

    category = Category(name=name)
    db.add(category)
    db.flush()
    return category


def get_or_create_mechanic(db: Session, name: str) -> Mechanic:
    mechanic = db.scalar(select(Mechanic).where(Mechanic.name == name))

    if mechanic is not None:
        return mechanic

    mechanic = Mechanic(name=name)
    db.add(mechanic)
    db.flush()
    return mechanic


def seed_game(
    db: Session,
    *,
    bgg_id: int,
    name: str,
    year_published: int,
    description: str,
    min_players: int,
    max_players: int,
    playing_time: int,
    min_playtime: int,
    max_playtime: int,
    min_age: int,
    average_rating: float,
    bayes_average: float,
    users_rated: int,
    average_weight: float,
    categories: list[str],
    mechanics: list[str],
) -> None:
    existing_game = db.scalar(select(Game).where(Game.bgg_id == bgg_id))

    if existing_game is not None:
        print(f"Skipped existing demo game: {name}")
        return

    game = Game(
        bgg_id=bgg_id,
        name=name,
        year_published=year_published,
        description=description,
        min_players=min_players,
        max_players=max_players,
        playing_time=playing_time,
        min_playtime=min_playtime,
        max_playtime=max_playtime,
        min_age=min_age,
        categories=[get_or_create_category(db, category) for category in categories],
        mechanics=[get_or_create_mechanic(db, mechanic) for mechanic in mechanics],
    )

    game.rating = Rating(
        average_rating=average_rating,
        bayes_average=bayes_average,
        users_rated=users_rated,
        average_weight=average_weight,
        rank_overall=None,
    )

    db.add(game)
    print(f"Created demo game: {name}")


def seed_demo_games() -> None:
    db = SessionLocal()

    try:
        seed_game(
            db,
            bgg_id=-1,
            name="Family Forest Adventure",
            year_published=2026,
            description="Development seed record for testing a quick family-friendly adventure game.",
            min_players=2,
            max_players=5,
            playing_time=35,
            min_playtime=25,
            max_playtime=40,
            min_age=8,
            average_rating=7.4,
            bayes_average=7.1,
            users_rated=420,
            average_weight=1.7,
            categories=["Family", "Adventure"],
            mechanics=["Cooperative Game", "Dice Rolling"],
        )

        seed_game(
            db,
            bgg_id=-2,
            name="Dungeon Team Escape",
            year_published=2026,
            description="Development seed record for testing a cooperative fantasy dungeon game.",
            min_players=2,
            max_players=4,
            playing_time=50,
            min_playtime=40,
            max_playtime=60,
            min_age=10,
            average_rating=7.8,
            bayes_average=7.5,
            users_rated=710,
            average_weight=2.3,
            categories=["Fantasy", "Adventure"],
            mechanics=["Cooperative Game", "Dice Rolling"],
        )

        seed_game(
            db,
            bgg_id=-3,
            name="Kingdom Strategy Council",
            year_published=2026,
            description="Development seed record for testing a heavier strategy game.",
            min_players=2,
            max_players=4,
            playing_time=110,
            min_playtime=90,
            max_playtime=120,
            min_age=14,
            average_rating=8.0,
            bayes_average=7.7,
            users_rated=860,
            average_weight=3.8,
            categories=["Strategy", "Fantasy"],
            mechanics=["Worker Placement", "Hand Management"],
        )

        db.commit()
        print("Demo seed completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_games()