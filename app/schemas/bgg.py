from pydantic import BaseModel, Field


class BggRatingData(BaseModel):
    average_rating: float | None = None
    bayes_average: float | None = None
    users_rated: int | None = None
    average_weight: float | None = None
    rank_overall: int | None = None


class BggGameData(BaseModel):
    bgg_id: int
    name: str
    year_published: int | None = None
    description: str | None = None

    min_players: int | None = None
    max_players: int | None = None
    playing_time: int | None = None
    min_playtime: int | None = None
    max_playtime: int | None = None
    min_age: int | None = None

    rating: BggRatingData | None = None

    categories: list[str] = Field(default_factory=list)
    mechanics: list[str] = Field(default_factory=list)
    designers: list[str] = Field(default_factory=list)
    publishers: list[str] = Field(default_factory=list)