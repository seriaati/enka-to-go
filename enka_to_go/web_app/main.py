import json
import logging

import aiohttp
import flet as ft

from ..enka.request import EnkaNetworkAPI
from ..go.converter import EnkaToGOConverter


class EnkaToGOWebApp:
    def __init__(self, page: ft.Page, session: aiohttp.ClientSession):
        self.page = page
        assert self.page.client_storage
        self.storage = self.page.client_storage
        self.session = session
        self.api = EnkaNetworkAPI(self.session)
        self.converter: EnkaToGOConverter

        # control refs
        self.uid_text_field = ft.Ref[ft.TextField]()
        self.result_json = ft.Ref[ft.TextField]()

    async def _update_text_map(self) -> None:
        async with self.session.get(
            "https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/TextMap/TextMapEN.json"
        ) as resp:
            text = await resp.text()
        data = json.loads(text)
        with open("data/text_map.json", "w") as f:
            json.dump(data, f)

    async def _update_avatar_excel_config_data(self) -> None:
        async with self.session.get(
            "https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/ExcelBinOutput/AvatarExcelConfigData.json"
        ) as resp:
            text = await resp.text()
        data = json.loads(text)
        with open("data/avatar_excel_config_data.json", "w") as f:
            json.dump(data, f)

    async def _update_characters_json(self) -> None:
        async with self.session.get(
            "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/characters.json"
        ) as resp:
            text = await resp.text()
        data = json.loads(text)
        with open("data/characters.json", "w") as f:
            json.dump(data, f)

    async def _update_data(self) -> None:
        await self._update_text_map()
        await self._update_avatar_excel_config_data()
        await self._update_characters_json()

    async def _on_submit(self, _: ft.ControlEvent) -> None:
        await self.page.show_snack_bar_async(
            ft.SnackBar(
                ft.Row(
                    [
                        ft.ProgressRing(
                            width=16,
                            height=16,
                            stroke_width=2,
                            color=ft.colors.ON_SECONDARY_CONTAINER,
                        ),
                        ft.Text(
                            "Fetching data...", color=ft.colors.ON_SECONDARY_CONTAINER
                        ),
                    ]
                ),
                bgcolor=ft.colors.SECONDARY_CONTAINER,
            )
        )

        uid = self.uid_text_field.current.value
        if not uid:
            return await self.page.show_snack_bar_async(
                ft.SnackBar(
                    ft.Text("Please enter a UID."),
                    bgcolor=ft.colors.RED_300,
                    show_close_icon=True,
                )
            )

        # save uid to storage
        storage_uid = await self.storage.get_async("uid")
        if storage_uid != uid:
            await self.storage.set_async("uid", uid)

        # fetch and convert data
        try:
            response = await self.api.fetch_showcase(uid)
        except Exception as e:
            logging.exception(e)
            return await self.page.show_snack_bar_async(
                ft.SnackBar(
                    ft.Text(f"Error: {e}"),
                    bgcolor=ft.colors.RED_300,
                    show_close_icon=True,
                )
            )
        try:
            converted = self.converter.convert(response.characters)
        except Exception as e:
            logging.exception(e)
            return await self.page.show_snack_bar_async(
                ft.SnackBar(
                    ft.Text("Error: Failed to convert data."),
                    bgcolor=ft.colors.RED_300,
                    show_close_icon=True,
                )
            )

        converted_json = json.dumps(converted, indent=4)
        self.result_json.current.value = converted_json
        await self.result_json.current.update_async()

        await self.page.show_snack_bar_async(
            ft.SnackBar(
                ft.Text("Complete."),
                bgcolor=ft.colors.GREEN_300,
                show_close_icon=True,
            )
        )

    async def _copy_to_clipboard(self, _: ft.ControlEvent) -> None:
        if result_json := self.result_json.current.value:
            await self.page.show_snack_bar_async(
                ft.SnackBar(
                    ft.Text(
                        "Copied to clipboard.",
                        color=ft.colors.ON_SECONDARY_CONTAINER,
                    ),
                    bgcolor=ft.colors.SECONDARY_CONTAINER,
                )
            )
            await self.page.set_clipboard_async(result_json)
        else:
            await self.page.show_snack_bar_async(
                ft.SnackBar(
                    ft.Text("There is nothing to copy."),
                    bgcolor=ft.colors.RED_300,
                    show_close_icon=True,
                )
            )

    async def _add_controls(self) -> None:
        self.page.appbar = ft.AppBar(
            title=ft.Container(
                ft.Text("Enka to GO (Genshin Optimizer)", size=20),
                margin=ft.margin.symmetric(vertical=10),
            ),
            actions=[
                ft.IconButton(
                    icon=ft.icons.CHAT_OUTLINED,
                    url="https://discord.com/users/410036441129943050",
                ),
                ft.IconButton(
                    icon=ft.icons.CODE_OUTLINED,
                    url="https://github.com/seriaati/enka-to-go",
                ),
                ft.IconButton(
                    icon=ft.icons.COFFEE_OUTLINED, url="https://ko-fi.com/chatmind"
                ),
            ],
            toolbar_height=64,
        )
        self.page.controls = [
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Container(
                                    ft.TextField(
                                        ref=self.uid_text_field,
                                        label="UID",
                                        hint_text="901211014",
                                        max_length=9,
                                        value=await self.storage.get_async("uid"),
                                        on_submit=self._on_submit,
                                    ),
                                    margin=ft.margin.only(right=16),
                                ),
                                ft.FilledButton("Submit", on_click=self._on_submit),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            wrap=True,
                        ),
                        margin=ft.margin.only(top=16, left=16),
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.FilledTonalButton(
                                    text="Copy to clipboard",
                                    icon=ft.icons.CONTENT_COPY_OUTLINED,
                                    on_click=self._copy_to_clipboard,
                                ),
                                ft.OutlinedButton(
                                    text="Enka Network",
                                    icon=ft.icons.OPEN_IN_NEW_OUTLINED,
                                    url="https://enka.network/",
                                ),
                                ft.OutlinedButton(
                                    text="Genshin Optimizer",
                                    icon=ft.icons.OPEN_IN_NEW_OUTLINED,
                                    url="https://frzyc.github.io/genshin-optimizer/#/setting",
                                ),
                            ],
                            spacing=16,
                            run_spacing=16,
                            wrap=True,
                        ),
                        margin=ft.margin.only(top=16, left=16, bottom=16),
                    ),
                    ft.Container(
                        ft.TextField(
                            ref=self.result_json,
                            label="JSON",
                            hint_text="The GOOD JSON data will be displayed here.",
                            multiline=True,
                            read_only=True,
                        ),
                        margin=ft.margin.only(left=16),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]
        await self.page.update_async()

    async def run(self, page: ft.Page) -> None:
        self.page = page
        assert self.page.client_storage
        self.storage = self.page.client_storage

        self.page.controls = [
            ft.Row(
                [
                    ft.ProgressRing(width=16, height=16, stroke_width=2),
                    ft.Text("Updating data..."),
                ]
            )
        ]
        await self.page.update_async()

        await self._update_data()
        await self._add_controls()
        self.converter = EnkaToGOConverter()