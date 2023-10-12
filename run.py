import asyncio
import logging
import sys

import aiohttp
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

session = aiohttp.ClientSession()


async def main(page: ft.Page):
    page.title = "Enka to GO"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    web_app = EnkaToGOWebApp(page, session)
    await web_app.run(page)


ft.app(
    target=main,
    view=None if sys.platform == "linux" else ft.AppView.WEB_BROWSER,
    port=7091,
)


loop = asyncio.get_event_loop()
loop.run_until_complete(session.close())
loop.close()
