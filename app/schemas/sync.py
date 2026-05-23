from pydantic import BaseModel


class SyncResult(BaseModel):
    import_run_id: int
    status: str
    games_found: int
    games_created: int
    games_updated: int
    games_skipped: int
    errors_count: int
    message: str | None = None