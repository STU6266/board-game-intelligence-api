from app.schemas.bgg import BggGameData, BggRatingData
from app.services.data_quality_service import validate_bgg_game_data


def build_valid_game() -> BggGameData:
    return BggGameData(
        bgg_id=999001,
        name="Sample Quest Island",
        description="A valid sample game.",
        min_players=2,
        max_players=5,
        playing_time=45,
        min_playtime=30,
        max_playtime=45,
        min_age=8,
        rating=BggRatingData(
            average_rating=7.62,
            bayes_average=7.31,
            users_rated=825,
            average_weight=2.18,
            rank_overall=418,
        ),
    )


def test_valid_game_data_passes_quality_check() -> None:
    game = build_valid_game()

    result = validate_bgg_game_data(game)

    assert result.is_valid is True
    assert result.errors == []
    assert result.warnings == []


def test_invalid_player_range_is_reported_as_error() -> None:
    game = build_valid_game()
    game.min_players = 5
    game.max_players = 2

    result = validate_bgg_game_data(game)

    assert result.is_valid is False
    assert any(issue.field == "players" for issue in result.errors)


def test_invalid_playtime_and_rating_are_reported_as_errors() -> None:
    game = build_valid_game()
    game.playing_time = -20
    game.rating.average_rating = 12.5

    result = validate_bgg_game_data(game)

    assert result.is_valid is False
    assert any(issue.field == "playing_time" for issue in result.errors)
    assert any(issue.field == "average_rating" for issue in result.errors)


def test_missing_optional_data_creates_warnings_but_remains_valid() -> None:
    game = build_valid_game()
    game.description = None
    game.rating = None

    result = validate_bgg_game_data(game)

    assert result.is_valid is True
    assert result.errors == []
    assert any(issue.field == "description" for issue in result.warnings)
    assert any(issue.field == "rating" for issue in result.warnings)