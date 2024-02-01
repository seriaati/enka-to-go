import asyncio
import logging
import sys

import enka
import flet as ft

from enka_to_go.web_app.main import EnkaToGOWebApp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
    ],
)

loop = asyncio.get_event_loop()

api = enka.EnkaAPI(headers={"User-Agent": "EnkaToGO"})
loop.run_until_complete(api.start())


async def main(page: ft.Page) -> None:
    page.title = "Enka to GO"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    web_app = EnkaToGOWebApp(page, api)
    await web_app.add_controls()


ft.app(
    target=main,
    view=None if sys.platform == "linux" else ft.AppView.WEB_BROWSER,
    port=7091,
)

loop.run_until_complete(api.close())
loop.close()
