import sys

import flet as ft

from enka_to_go.web_app.main import EnkaToGOWebApp


async def main(page: ft.Page) -> None:
    page.title = "Enka to GO"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    web_app = EnkaToGOWebApp(page)
    await web_app.add_controls()


ft.app(
    target=main,
    view=None if sys.platform == "linux" else ft.AppView.WEB_BROWSER,
    port=7091,
)
