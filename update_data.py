import asyncio

import enka


async def update_data() -> None:
    async with enka.EnkaAPI() as api:
        await api.update_assets()


asyncio.run(update_data())
