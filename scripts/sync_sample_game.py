from app.db.session import SessionLocal
from app.services.game_sync_service import sync_game_from_xml_file


def main() -> None:
    db = SessionLocal()

    try:
        result = sync_game_from_xml_file(
            db,
            "sample_data/bgg_thing_sample.xml",
        )

        print(result.model_dump())

    finally:
        db.close()


if __name__ == "__main__":
    main()