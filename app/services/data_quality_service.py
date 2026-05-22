from app.schemas.bgg import BggGameData
from app.schemas.data_quality import DataQualityIssue, DataQualityResult


def validate_bgg_game_data(game: BggGameData) -> DataQualityResult:
    errors: list[DataQualityIssue] = []
    warnings: list[DataQualityIssue] = []

    if (
        game.min_players is not None
        and game.max_players is not None
        and game.min_players > game.max_players
    ):
        errors.append(
            DataQualityIssue(
                field="players",
                message="min_players cannot be greater than max_players.",
            )
        )

    playtime_fields = {
        "playing_time": game.playing_time,
        "min_playtime": game.min_playtime,
        "max_playtime": game.max_playtime,
    }

    for field_name, value in playtime_fields.items():
        if value is not None and value < 0:
            errors.append(
                DataQualityIssue(
                    field=field_name,
                    message=f"{field_name} cannot be negative.",
                )
            )

    if (
        game.min_playtime is not None
        and game.max_playtime is not None
        and game.min_playtime > game.max_playtime
    ):
        errors.append(
            DataQualityIssue(
                field="playtime",
                message="min_playtime cannot be greater than max_playtime.",
            )
        )

    if game.min_age is not None and game.min_age < 0:
        errors.append(
            DataQualityIssue(
                field="min_age",
                message="min_age cannot be negative.",
            )
        )

    if game.rating is None:
        warnings.append(
            DataQualityIssue(
                field="rating",
                message="Rating data is missing.",
            )
        )
    else:
        if (
            game.rating.average_rating is not None
            and not 0 <= game.rating.average_rating <= 10
        ):
            errors.append(
                DataQualityIssue(
                    field="average_rating",
                    message="average_rating must be between 0 and 10.",
                )
            )

        if (
            game.rating.bayes_average is not None
            and not 0 <= game.rating.bayes_average <= 10
        ):
            errors.append(
                DataQualityIssue(
                    field="bayes_average",
                    message="bayes_average must be between 0 and 10.",
                )
            )

        if (
            game.rating.average_weight is not None
            and not 0 <= game.rating.average_weight <= 5
        ):
            errors.append(
                DataQualityIssue(
                    field="average_weight",
                    message="average_weight must be between 0 and 5.",
                )
            )

        if game.rating.users_rated is not None and game.rating.users_rated < 0:
            errors.append(
                DataQualityIssue(
                    field="users_rated",
                    message="users_rated cannot be negative.",
                )
            )

    if game.description is None:
        warnings.append(
            DataQualityIssue(
                field="description",
                message="Description is missing.",
            )
        )

    return DataQualityResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )