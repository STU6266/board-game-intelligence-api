from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Board Game Intelligence API"
    app_env: str = "development"

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    database_url: str

    bgg_base_url: str = "https://boardgamegeek.com/xmlapi2"
    bgg_api_token: str | None = None
    bgg_request_delay_seconds: float = 5.0
    bgg_request_timeout_seconds: float = 15.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()