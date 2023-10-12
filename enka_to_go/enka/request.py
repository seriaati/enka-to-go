from typing import Any, Dict

import aiohttp
import cachetools

from .exceptions import raise_for_retcode
from .models.response import ShowcaseResponse


class EnkaNetworkAPI:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.base_url = "https://enka.network/api/uid/{uid}/"
        self._cache: cachetools.TTLCache[str, Dict[str, Any]] = cachetools.TTLCache(
            maxsize=100, ttl=60
        )

    async def fetch_showcase(self, uid: str) -> ShowcaseResponse:
        if cached := self._cache.get(uid):
            return ShowcaseResponse(**cached)

        url = self.base_url.format(uid=uid)
        async with self.session.get(url, headers={"User-Agent": "Enka to GO"}) as resp:
            if resp.status != 200:
                raise_for_retcode(resp.status)

            data: Dict[str, Any] = await resp.json()
            self._cache[uid] = data
            return ShowcaseResponse(**data)
