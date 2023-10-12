import pytest

from enka_to_go.enka.request import EnkaNetworkAPI


@pytest.mark.asyncio
async def test_fetch_showcase():
    api = EnkaNetworkAPI()
    showcase = await api.fetch_showcase("901211014")
    assert showcase.uid == "901211014"
