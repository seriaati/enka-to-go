import aiohttp
import pytest

from enka_to_go.enka.request import EnkaNetworkAPI


@pytest.mark.asyncio
async def test_fetch_showcase():
    async with aiohttp.ClientSession() as session:
        api = EnkaNetworkAPI(session)
        showcase = await api.fetch_showcase("901211014")
        assert showcase.uid == "901211014"
