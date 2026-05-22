from pathlib import Path
from xml.etree import ElementTree as ET

from app.schemas.bgg import BggGameData, BggRatingData


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned_value = " ".join(value.split())

    return cleaned_value or None


def _get_value_as_int(element: ET.Element | None) -> int | None:
    if element is None:
        return None

    value = element.attrib.get("value")

    if value is None or value == "":
        return None

    return int(value)


def _get_value_as_float(element: ET.Element | None) -> float | None:
    if element is None:
        return None

    value = element.attrib.get("value")

    if value is None or value == "":
        return None

    return float(value)


def _get_link_values(item: ET.Element, link_type: str) -> list[str]:
    return [
        link.attrib["value"]
        for link in item.findall("link")
        if link.attrib.get("type") == link_type and link.attrib.get("value")
    ]


def _get_primary_name(item: ET.Element) -> str:
    for name_element in item.findall("name"):
        if name_element.attrib.get("type") == "primary":
            name = name_element.attrib.get("value")

            if name:
                return name

    raise ValueError("BGG item does not contain a primary name.")


def _get_overall_rank(item: ET.Element) -> int | None:
    rank_elements = item.findall("./statistics/ratings/ranks/rank")

    for rank_element in rank_elements:
        if rank_element.attrib.get("name") == "boardgame":
            value = rank_element.attrib.get("value")

            if value is None or value == "Not Ranked":
                return None

            return int(value)

    return None


def _parse_rating(item: ET.Element) -> BggRatingData | None:
    ratings = item.find("./statistics/ratings")

    if ratings is None:
        return None

    return BggRatingData(
        users_rated=_get_value_as_int(ratings.find("usersrated")),
        average_rating=_get_value_as_float(ratings.find("average")),
        bayes_average=_get_value_as_float(ratings.find("bayesaverage")),
        average_weight=_get_value_as_float(ratings.find("averageweight")),
        rank_overall=_get_overall_rank(item),
    )


def parse_bgg_thing_xml(xml_content: str) -> BggGameData:
    root = ET.fromstring(xml_content)
    item = root.find("item")

    if item is None:
        raise ValueError("BGG XML response does not contain an item.")

    bgg_id = item.attrib.get("id")

    if bgg_id is None:
        raise ValueError("BGG item does not contain an id.")

    return BggGameData(
        bgg_id=int(bgg_id),
        name=_get_primary_name(item),
        year_published=_get_value_as_int(item.find("yearpublished")),
        description=_clean_text(item.findtext("description")),
        min_players=_get_value_as_int(item.find("minplayers")),
        max_players=_get_value_as_int(item.find("maxplayers")),
        playing_time=_get_value_as_int(item.find("playingtime")),
        min_playtime=_get_value_as_int(item.find("minplaytime")),
        max_playtime=_get_value_as_int(item.find("maxplaytime")),
        min_age=_get_value_as_int(item.find("minage")),
        rating=_parse_rating(item),
        categories=_get_link_values(item, "boardgamecategory"),
        mechanics=_get_link_values(item, "boardgamemechanic"),
        designers=_get_link_values(item, "boardgamedesigner"),
        publishers=_get_link_values(item, "boardgamepublisher"),
    )


def parse_bgg_thing_file(file_path: str | Path) -> BggGameData:
    xml_content = Path(file_path).read_text(encoding="utf-8")

    return parse_bgg_thing_xml(xml_content)