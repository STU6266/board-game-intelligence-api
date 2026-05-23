from pydantic import BaseModel


class FamilyFriendlyGameResponse(BaseModel):
    id: int
    bgg_id: int
    name: str

    min_age: int | None = None
    min_players: int | None = None
    max_players: int | None = None
    playing_time: int | None = None

    average_rating: float | None = None
    average_weight: float | None = None

    complexity_label: str | None = None
    playtime_label: str | None = None
    age_group: str | None = None

    family_score: int

class LowComplexityHighRatingGameResponse(BaseModel):
    id: int
    bgg_id: int
    name: str

    min_age: int | None = None
    playing_time: int | None = None

    average_rating: float
    average_weight: float

    complexity_label: str
    playtime_label: str | None = None