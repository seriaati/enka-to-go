import flet as ft

from enka_to_go.web_app.main import EnkaToGOWebApp
from enka_to_go.zo.loader import load_data


async def main(page: ft.Page) -> None:
    await load_data()
    page.title = "Enka to GO"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    web_app = EnkaToGOWebApp(page)
    await web_app.add_controls()


ft.app(target=main, view=None, port=7091)
