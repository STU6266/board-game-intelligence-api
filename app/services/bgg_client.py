import time

import httpx

from app.core.config import settings


class BggClientError(Exception):
    """Raised when a BoardGameGeek API request cannot be completed."""


class BggClient:
    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_token: str | None = None,
        request_delay_seconds: float | None = None,
        timeout_seconds: float | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.base_url = (base_url or settings.bgg_base_url).rstrip("/")
        self.api_token = api_token if api_token is not None else settings.bgg_api_token
        self.request_delay_seconds = (
            request_delay_seconds
            if request_delay_seconds is not None
            else settings.bgg_request_delay_seconds
        )
        self.timeout_seconds = (
            timeout_seconds
            if timeout_seconds is not None
            else settings.bgg_request_timeout_seconds
        )
        self.transport = transport
        self._last_request_time: float | None = None

    def _build_headers(self) -> dict[str, str]:
        if not self.api_token:
            raise BggClientError(
                "BGG_API_TOKEN is missing. Add an authorized BoardGameGeek application token to .env."
            )

        return {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/xml",
            "User-Agent": "BoardGameIntelligenceAPI/0.1",
        }

    def _respect_request_delay(self) -> None:
        if self._last_request_time is None:
            return

        elapsed = time.monotonic() - self._last_request_time
        remaining_delay = self.request_delay_seconds - elapsed

        if remaining_delay > 0:
            time.sleep(remaining_delay)

    def _get(self, endpoint: str, params: dict[str, str | int]) -> str:
        self._respect_request_delay()

        try:
            with httpx.Client(
                base_url=self.base_url,
                headers=self._build_headers(),
                timeout=self.timeout_seconds,
                transport=self.transport,
            ) as client:
                response = client.get(endpoint, params=params)

            self._last_request_time = time.monotonic()

            if response.status_code in {500, 503}:
                raise BggClientError(
                    "BoardGameGeek temporarily rejected the request. Try again later."
                )

            response.raise_for_status()

            return response.text

        except httpx.HTTPStatusError as exc:
            raise BggClientError(
                f"BoardGameGeek request failed with HTTP {exc.response.status_code}."
            ) from exc
        except httpx.RequestError as exc:
            raise BggClientError(
                "BoardGameGeek request failed because the service could not be reached."
            ) from exc

    def get_game_xml(self, bgg_id: int) -> str:
        return self._get(
            "/thing",
            {
                "id": bgg_id,
                "type": "boardgame",
                "stats": 1,
            },
        )

    def search_games_xml(self, query: str) -> str:
        return self._get(
            "/search",
            {
                "query": query,
                "type": "boardgame",
            },
        )