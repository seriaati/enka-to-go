import pytest

from enka_to_go.enka.request import EnkaNetworkAPI


@pytest.mark.asyncio
async def test_fetch_showcase():
    api = EnkaNetworkAPI()
    showcase = await api.fetch_showcase("901211014")
    assert showcase.uid == "901211014"


@pytest.mark.asyncio
async def test_empty_showcase():
    api = EnkaNetworkAPI()
    showcase = await api.fetch_showcase("123456789")
    assert showcase.uid == "123456789"
    assert showcase.characters == []


@pytest.mark.asyncio
async def test_traveler_showcase():
    api = EnkaNetworkAPI()
    showcase = await api.fetch_showcase("600001919")
    assert showcase.uid == "600001919"
