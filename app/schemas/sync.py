from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SyncResult(BaseModel):
    import_run_id: int
    status: str
    games_found: int
    games_created: int
    games_updated: int
    games_skipped: int
    errors_count: int
    message: str | None = None


class ImportErrorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bgg_id: int | None = None
    error_type: str
    error_message: str
    created_at: datetime


class ImportRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    status: str
    search_query: str | None = None
    started_at: datetime
    finished_at: datetime | None = None
    games_found: int
    games_created: int
    games_updated: int
    games_skipped: int
    errors_count: int
    message: str | None = None


class ImportRunDetailResponse(ImportRunResponse):
    errors: list[ImportErrorResponse]