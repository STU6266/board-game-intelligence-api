from app.models.game import Game
from app.schemas.report import (
    FamilyFriendlyGameResponse,
    LowComplexityHighRatingGameResponse,
)

def get_complexity_label(average_weight: float | None) -> str | None:
    if average_weight is None:
        return None

    if average_weight <= 1.5:
        return "Very Light"

    if average_weight <= 2.5:
        return "Light / Medium"

    if average_weight <= 3.5:
        return "Medium / Heavy"

    return "Heavy"


def get_playtime_label(playing_time: int | None) -> str | None:
    if playing_time is None:
        return None

    if playing_time <= 30:
        return "Quick"

    if playing_time <= 60:
        return "Standard"

    if playing_time <= 120:
        return "Long"

    return "Very Long"


def get_age_group(min_age: int | None) -> str | None:
    if min_age is None:
        return None

    if min_age <= 7:
        return "Kids"

    if min_age <= 12:
        return "Family"

    if min_age <= 15:
        return "Teen"

    return "Adult"


def calculate_family_score(
    *,
    average_rating: float | None,
    average_weight: float | None,
    min_age: int | None,
    playing_time: int | None,
    min_players: int | None,
    max_players: int | None,
) -> int:
    score = 0

    if average_rating is not None:
        score += round((average_rating / 10) * 40)

    if average_weight is not None:
        if average_weight <= 1.5:
            score += 20
        elif average_weight <= 2.5:
            score += 15
        elif average_weight <= 3.5:
            score += 7
        else:
            score -= 10

    if min_age is not None:
        if min_age <= 8:
            score += 15
        elif min_age <= 10:
            score += 12
        elif min_age <= 12:
            score += 6

    if playing_time is not None:
        if playing_time <= 30:
            score += 15
        elif playing_time <= 60:
            score += 12
        elif playing_time <= 120:
            score += 5
        else:
            score -= 10

    if min_players is not None and max_players is not None:
        if min_players <= 2 and max_players >= 5:
            score += 10
        elif min_players <= 2 and max_players >= 4:
            score += 8
        elif min_players <= 2 and max_players >= 3:
            score += 5

    return max(0, min(score, 100))

def build_family_friendly_report(
    games: list[Game],
    minimum_score: int = 60,
) -> list[FamilyFriendlyGameResponse]:
    report_items: list[FamilyFriendlyGameResponse] = []

    for game in games:
        rating = game.rating

        average_rating = rating.average_rating if rating else None
        average_weight = rating.average_weight if rating else None

        family_score = calculate_family_score(
            average_rating=average_rating,
            average_weight=average_weight,
            min_age=game.min_age,
            playing_time=game.playing_time,
            min_players=game.min_players,
            max_players=game.max_players,
        )

        if family_score < minimum_score:
            continue

        report_items.append(
            FamilyFriendlyGameResponse(
                id=game.id,
                bgg_id=game.bgg_id,
                name=game.name,
                min_age=game.min_age,
                min_players=game.min_players,
                max_players=game.max_players,
                playing_time=game.playing_time,
                average_rating=average_rating,
                average_weight=average_weight,
                complexity_label=get_complexity_label(average_weight),
                playtime_label=get_playtime_label(game.playing_time),
                age_group=get_age_group(game.min_age),
                family_score=family_score,
            )
        )

    return sorted(
        report_items,
        key=lambda item: (
            -item.family_score,
            -(item.average_rating or 0),
            item.name.lower(),
        ),
    )

def build_low_complexity_high_rating_report(
    games: list[Game],
    minimum_rating: float = 7.0,
    maximum_complexity: float = 2.5,
) -> list[LowComplexityHighRatingGameResponse]:
    report_items: list[LowComplexityHighRatingGameResponse] = []

    for game in games:
        rating = game.rating

        if rating is None:
            continue

        if rating.average_rating is None or rating.average_weight is None:
            continue

        if rating.average_rating < minimum_rating:
            continue

        if rating.average_weight > maximum_complexity:
            continue

        report_items.append(
            LowComplexityHighRatingGameResponse(
                id=game.id,
                bgg_id=game.bgg_id,
                name=game.name,
                min_age=game.min_age,
                playing_time=game.playing_time,
                average_rating=rating.average_rating,
                average_weight=rating.average_weight,
                complexity_label=get_complexity_label(rating.average_weight),
                playtime_label=get_playtime_label(game.playing_time),
            )
        )

    return sorted(
        report_items,
        key=lambda item: (
            -item.average_rating,
            item.average_weight,
            item.name.lower(),
        ),
    )