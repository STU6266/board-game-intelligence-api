import httpx
import pytest

from app.services.bgg_client import BggClient, BggClientError


def test_get_game_xml_sends_required_query_parameters_and_token() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-token"
        assert request.url.params["id"] == "999001"
        assert request.url.params["type"] == "boardgame"
        assert request.url.params["stats"] == "1"

        return httpx.Response(
            200,
            text="<items><item id='999001' /></items>",
        )

    client = BggClient(
        api_token="test-token",
        request_delay_seconds=0,
        transport=httpx.MockTransport(handler),
    )

    xml_content = client.get_game_xml(999001)

    assert "<item id='999001'" in xml_content


def test_client_requires_api_token() -> None:
    client = BggClient(
        api_token="",
        request_delay_seconds=0,
    )

    with pytest.raises(BggClientError, match="BGG_API_TOKEN"):
        client.get_game_xml(999001)


def test_client_handles_temporary_bgg_server_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="Service unavailable")

    client = BggClient(
        api_token="test-token",
        request_delay_seconds=0,
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(BggClientError, match="temporarily rejected"):
        client.get_game_xml(999001)