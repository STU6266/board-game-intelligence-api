from pathlib import Path

import pytest

from app.services.bgg_parser import parse_bgg_thing_file, parse_bgg_thing_xml


SAMPLE_FILE = Path("sample_data/bgg_thing_sample.xml")


def test_parse_bgg_thing_file_extracts_basic_game_data() -> None:
    game = parse_bgg_thing_file(SAMPLE_FILE)

    assert game.bgg_id == 999001
    assert game.name == "Sample Quest Island"
    assert game.year_published == 2024
    assert game.min_players == 2
    assert game.max_players == 5
    assert game.playing_time == 45
    assert game.min_age == 8


def test_parse_bgg_thing_file_extracts_rating_and_links() -> None:
    game = parse_bgg_thing_file(SAMPLE_FILE)

    assert game.rating is not None
    assert game.rating.average_rating == 7.62
    assert game.rating.bayes_average == 7.31
    assert game.rating.users_rated == 825
    assert game.rating.average_weight == 2.18
    assert game.rating.rank_overall == 418

    assert game.categories == ["Adventure", "Deduction"]
    assert game.mechanics == ["Cooperative Game", "Dice Rolling"]
    assert game.designers == ["Sample Designer"]
    assert game.publishers == ["Sample Publisher"]


def test_parse_bgg_thing_xml_allows_missing_rating_data() -> None:
    xml_content = """
    <items totalitems="1">
        <item type="boardgame" id="123">
            <name type="primary" value="Game Without Ratings" />
            <minplayers value="1" />
            <maxplayers value="4" />
        </item>
    </items>
    """

    game = parse_bgg_thing_xml(xml_content)

    assert game.bgg_id == 123
    assert game.name == "Game Without Ratings"
    assert game.rating is None
    assert game.categories == []
    assert game.mechanics == []


def test_parse_bgg_thing_xml_raises_error_when_primary_name_is_missing() -> None:
    xml_content = """
    <items totalitems="1">
        <item type="boardgame" id="456">
            <minplayers value="2" />
            <maxplayers value="4" />
        </item>
    </items>
    """

    with pytest.raises(ValueError, match="primary name"):
        parse_bgg_thing_xml(xml_content)