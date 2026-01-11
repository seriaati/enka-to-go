import flet as ft
import flet.fastapi as fta

from src.app.web_app.main import EnkaToGOWebApp


async def before_main(page: ft.Page) -> None:
    pass


async def main(page: ft.Page) -> None:
    page.title = "Enka to GO"
    page.scroll = ft.ScrollMode.ADAPTIVE
    web_app = EnkaToGOWebApp(page)
    await web_app.add_controls()


app = fta.app(
    main,
    before_main=before_main,
    app_name="Enka to GO",
    app_short_name="EnkaToGO",
    app_description="Export your Enka Network showcase to Genshin/Zenless Optimizer.",
)
