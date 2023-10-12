import asyncio
import json

import aiohttp


async def update_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/TextMap/TextMapEN.json"
        ) as resp:
            text = await resp.text()
        data = json.loads(text)
        with open("data/text_map.json", "w") as f:
            json.dump(data, f)

        async with session.get(
            "https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/ExcelBinOutput/AvatarExcelConfigData.json"
        ) as resp:
            text = await resp.text()
        data = json.loads(text)
        with open("data/avatar_excel_config_data.json", "w") as f:
            json.dump(data, f)

        async with session.get(
            "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/characters.json"
        ) as resp:
            text = await resp.text()
        data = json.loads(text)
        with open("data/characters.json", "w") as f:
            json.dump(data, f)


asyncio.run(update_data())
