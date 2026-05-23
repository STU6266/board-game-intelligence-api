import pytest

from app.models import Game, Rating

from app.services.report_service import (
    build_family_friendly_report,
    build_low_complexity_high_rating_report,
    calculate_family_score,
    get_age_group,
    get_complexity_label,
    get_playtime_label,
)


@pytest.mark.parametrize(
    ("average_weight", "expected_label"),
    [
        (1.2, "Very Light"),
        (2.1, "Light / Medium"),
        (3.0, "Medium / Heavy"),
        (4.0, "Heavy"),
        (None, None),
    ],
)
def test_get_complexity_label(
    average_weight: float | None,
    expected_label: str | None,
) -> None:
    assert get_complexity_label(average_weight) == expected_label


@pytest.mark.parametrize(
    ("playing_time", "expected_label"),
    [
        (20, "Quick"),
        (45, "Standard"),
        (90, "Long"),
        (150, "Very Long"),
        (None, None),
    ],
)
def test_get_playtime_label(
    playing_time: int | None,
    expected_label: str | None,
) -> None:
    assert get_playtime_label(playing_time) == expected_label


@pytest.mark.parametrize(
    ("min_age", "expected_group"),
    [
        (6, "Kids"),
        (8, "Family"),
        (14, "Teen"),
        (16, "Adult"),
        (None, None),
    ],
)
def test_get_age_group(
    min_age: int | None,
    expected_group: str | None,
) -> None:
    assert get_age_group(min_age) == expected_group


def test_calculate_family_score_for_family_friendly_game() -> None:
    score = calculate_family_score(
        average_rating=7.4,
        average_weight=1.7,
        min_age=8,
        playing_time=35,
        min_players=2,
        max_players=5,
    )

    assert score == 82


def test_calculate_family_score_penalizes_heavy_long_game() -> None:
    score = calculate_family_score(
        average_rating=8.0,
        average_weight=3.8,
        min_age=14,
        playing_time=150,
        min_players=2,
        max_players=4,
    )

    assert score == 20


def test_calculate_family_score_never_drops_below_zero() -> None:
    score = calculate_family_score(
        average_rating=None,
        average_weight=5.0,
        min_age=18,
        playing_time=240,
        min_players=1,
        max_players=1,
    )

    assert score == 0

def test_build_family_friendly_report_filters_and_sorts_games() -> None:
    high_score_game = Game(
        id=1,
        bgg_id=-1,
        name="Family Forest Adventure",
        min_age=8,
        min_players=2,
        max_players=5,
        playing_time=35,
        rating=Rating(
            average_rating=7.4,
            average_weight=1.7,
        ),
    )

    lower_score_game = Game(
        id=2,
        bgg_id=-2,
        name="Dungeon Team Escape",
        min_age=10,
        min_players=2,
        max_players=4,
        playing_time=50,
        rating=Rating(
            average_rating=7.8,
            average_weight=2.3,
        ),
    )

    excluded_game = Game(
        id=3,
        bgg_id=-3,
        name="Kingdom Strategy Council",
        min_age=14,
        min_players=2,
        max_players=4,
        playing_time=150,
        rating=Rating(
            average_rating=8.0,
            average_weight=3.8,
        ),
    )

    report = build_family_friendly_report(
        [excluded_game, lower_score_game, high_score_game]
    )

    assert [item.name for item in report] == [
        "Family Forest Adventure",
        "Dungeon Team Escape",
    ]
    assert report[0].family_score == 82
    assert report[0].complexity_label == "Light / Medium"
    assert report[0].playtime_label == "Standard"
    assert report[0].age_group == "Family"

def test_build_low_complexity_high_rating_report_filters_and_sorts_games() -> None:
    family_game = Game(
        id=1,
        bgg_id=-1,
        name="Family Forest Adventure",
        min_age=8,
        playing_time=35,
        rating=Rating(
            average_rating=7.4,
            average_weight=1.7,
        ),
    )

    cooperative_game = Game(
        id=2,
        bgg_id=-2,
        name="Dungeon Team Escape",
        min_age=10,
        playing_time=50,
        rating=Rating(
            average_rating=7.8,
            average_weight=2.3,
        ),
    )

    heavy_game = Game(
        id=3,
        bgg_id=-3,
        name="Kingdom Strategy Council",
        min_age=14,
        playing_time=150,
        rating=Rating(
            average_rating=8.0,
            average_weight=3.8,
        ),
    )

    report = build_low_complexity_high_rating_report(
        [family_game, heavy_game, cooperative_game]
    )

    assert [item.name for item in report] == [
        "Dungeon Team Escape",
        "Family Forest Adventure",
    ]
    assert report[0].average_rating == 7.8
    assert report[0].complexity_label == "Light / Medium"
    assert report[0].playtime_label == "Standard"