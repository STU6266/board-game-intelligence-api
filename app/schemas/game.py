from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RatingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    average_rating: float | None = None
    bayes_average: float | None = None
    users_rated: int | None = None
    average_weight: float | None = None
    rank_overall: int | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class MechanicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class GameListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bgg_id: int
    name: str
    year_published: int | None = None
    min_players: int | None = None
    max_players: int | None = None
    playing_time: int | None = None
    min_age: int | None = None
    rating: RatingResponse | None = None


class GameDetailResponse(GameListItemResponse):
    description: str | None = None
    min_playtime: int | None = None
    max_playtime: int | None = None
    last_synced_at: datetime | None = None

    categories: list[CategoryResponse] = Field(default_factory=list)
    mechanics: list[MechanicResponse] = Field(default_factory=list)