import json

import enka
import flet as ft
from loguru import logger

from src.app.go.converter import EnkaToGOConverter
from src.app.zo.converter import EnkaToZOConverter


class EnkaToGOWebApp:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.storage = ft.SharedPreferences()

        # control refs
        self.uid_text_field = ft.Ref[ft.TextField]()
        self.game_selector = ft.Ref[ft.Dropdown]()
        self.result_json = ft.Ref[ft.TextField]()

    async def _on_submit(self, _: ft.Event) -> None:
        self.page.show_dialog(
            ft.SnackBar(
                ft.Row(
                    [
                        ft.ProgressRing(
                            width=16,
                            height=16,
                            stroke_width=2,
                            color=ft.Colors.ON_SECONDARY_CONTAINER,
                        ),
                        ft.Text("Fetching data...", color=ft.Colors.ON_SECONDARY_CONTAINER),
                    ]
                ),
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
            )
        )

        uid = self.uid_text_field.current.value
        if not uid:
            return self.page.show_dialog(
                ft.SnackBar(
                    ft.Text("Please enter a UID.", color=ft.Colors.ON_ERROR_CONTAINER),
                    bgcolor=ft.Colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.Colors.ON_ERROR_CONTAINER,
                )
            )

        # save game to storage
        await self.storage.set("game", self.game_selector.current.value)

        # save uid to storage
        storage_uid = await self.storage.get("uid")
        if storage_uid != uid:
            await self.storage.set("uid", uid)

        # fetch and convert data
        game = self.game_selector.current.value
        try:
            if game == "Genshin Impact":
                async with enka.GenshinClient() as client:
                    response = await client.fetch_showcase(uid)
                    data_to_convert = response.characters
                    converter_cls = EnkaToGOConverter
            else:  # Zenless Zone Zero
                async with enka.ZZZClient() as client:
                    response = await client.fetch_showcase(uid)
                    data_to_convert = response.agents
                    converter_cls = EnkaToZOConverter
        except enka.errors.EnkaAPIError as e:
            logger.error(f"Enka API error: {e}")
            return self.page.show_dialog(
                ft.SnackBar(
                    ft.Text(f"Enka API error: {e}", color=ft.Colors.ON_ERROR_CONTAINER),
                    bgcolor=ft.Colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.Colors.ON_ERROR_CONTAINER,
                )
            )
        except Exception as e:
            logger.exception("Failed to fetch data.")
            return self.page.show_dialog(
                ft.SnackBar(
                    ft.Text(f"Error: {e}", color=ft.Colors.ON_ERROR_CONTAINER),
                    bgcolor=ft.Colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.Colors.ON_ERROR_CONTAINER,
                )
            )

        if not data_to_convert:
            return self.page.show_dialog(
                ft.SnackBar(
                    ft.Text(
                        "Error: No characters/agents found in Showcase.",
                        color=ft.Colors.ON_ERROR_CONTAINER,
                    ),
                    bgcolor=ft.Colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.Colors.ON_ERROR_CONTAINER,
                )
            )

        try:
            converted = converter_cls.convert(data_to_convert)  # pyright: ignore[reportArgumentType]
        except Exception:
            logger.exception("Failed to convert data.")
            return self.page.show_dialog(
                ft.SnackBar(
                    ft.Text(
                        "Error: Failed to convert data.",
                        color=ft.Colors.ON_ERROR_CONTAINER,
                    ),
                    bgcolor=ft.Colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.Colors.ON_ERROR_CONTAINER,
                )
            )

        converted_json = json.dumps(converted, indent=4)
        self.result_json.current.value = converted_json
        self.result_json.current.update()

        self.page.show_dialog(
            ft.SnackBar(
                ft.Text("Complete.", color=ft.Colors.ON_TERTIARY_CONTAINER),
                bgcolor=ft.Colors.TERTIARY_CONTAINER,
                show_close_icon=True,
                close_icon_color=ft.Colors.ON_TERTIARY_CONTAINER,
            )
        )

    async def _copy_to_clipboard(self, _: ft.Event) -> None:
        if result_json := self.result_json.current.value:
            self.page.show_dialog(
                ft.SnackBar(
                    ft.Text(
                        "Copied to clipboard.",
                        color=ft.Colors.ON_SECONDARY_CONTAINER,
                    ),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                )
            )
            await ft.Clipboard().set(result_json)
        else:
            self.page.show_dialog(
                ft.SnackBar(
                    ft.Text("There is nothing to copy.", color=ft.Colors.ON_ERROR_CONTAINER),
                    bgcolor=ft.Colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.Colors.ON_ERROR_CONTAINER,
                )
            )

    async def _popup_menu_item_on_click(self, e: ft.Event) -> None:
        await self.page.launch_url(e.control.data)

    async def add_controls(self) -> None:
        storage_game = await self.storage.get("game")
        storage_uid = await self.storage.get("uid")

        self.page.appbar = ft.AppBar(
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            title=ft.Container(
                ft.Text("Enka to GO", size=20, color=ft.Colors.ON_PRIMARY_CONTAINER),
                margin=ft.Margin.symmetric(vertical=10),
            ),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            icon=ft.Icons.CHAT_OUTLINED,
                            content="Contact me on Discord",
                            data="https://discord.com/users/410036441129943050",
                            on_click=self._popup_menu_item_on_click,
                        ),
                        ft.PopupMenuItem(
                            icon=ft.Icons.CODE_OUTLINED,
                            content="Source code",
                            data="https://github.com/seriaati/enka-to-go",
                            on_click=self._popup_menu_item_on_click,
                        ),
                    ]
                ),
            ],
            toolbar_height=64,
        )
        self.page.controls = [
            ft.Column(
                [
                    ft.Container(
                        ft.Column(
                            [
                                ft.Container(
                                    ft.Dropdown(
                                        ref=self.game_selector,
                                        label="Game",
                                        options=[
                                            ft.dropdown.Option("Genshin Impact"),
                                            ft.dropdown.Option("Zenless Zone Zero"),
                                        ],
                                        value=storage_game or "Genshin Impact",
                                    ),
                                ),
                                ft.Container(
                                    ft.TextField(
                                        ref=self.uid_text_field,
                                        label="UID",
                                        hint_text="901211014",
                                        max_length=10,
                                        value=storage_uid,
                                        on_submit=self._on_submit,
                                    ),
                                ),
                                ft.FilledButton("Submit", on_click=self._on_submit),
                            ],
                            spacing=16,
                        ),
                        margin=ft.Margin.only(top=16, left=16),
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.FilledTonalButton(
                                    content="Copy to clipboard",
                                    icon=ft.Icons.CONTENT_COPY_OUTLINED,
                                    on_click=self._copy_to_clipboard,
                                ),
                                ft.OutlinedButton(
                                    content="Enka Network",
                                    icon=ft.Icons.OPEN_IN_NEW_OUTLINED,
                                    url="https://enka.network/",
                                ),
                                ft.OutlinedButton(
                                    content="Genshin Optimizer",
                                    icon=ft.Icons.OPEN_IN_NEW_OUTLINED,
                                    url="https://frzyc.github.io/genshin-optimizer/#/setting",
                                ),
                                ft.OutlinedButton(
                                    content="Zenless Optimizer",
                                    icon=ft.Icons.OPEN_IN_NEW_OUTLINED,
                                    url="https://frzyc.github.io/zenless-optimizer/#/setting",
                                ),
                            ],
                            spacing=16,
                            wrap=True,
                        ),
                        margin=ft.Margin.only(top=16, left=16, bottom=16),
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                ft.TextField(
                                    ref=self.result_json,
                                    label="JSON",
                                    hint_text="The GOOD/ZOD JSON will be displayed here.",
                                    multiline=True,
                                    read_only=True,
                                ),
                                margin=ft.Margin.only(left=16),
                                expand=True,
                            )
                        ]
                    ),
                ],
            )
        ]
        self.page.update()
