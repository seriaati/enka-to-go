import json
import logging
from typing import TYPE_CHECKING

import flet as ft

from ..go.converter import EnkaToGOConverter

if TYPE_CHECKING:
    from enka import EnkaAPI

LOGGER_ = logging.getLogger(__name__)


class EnkaToGOWebApp:
    def __init__(self, page: ft.Page, api: "EnkaAPI") -> None:
        self.page = page
        assert self.page.client_storage
        self.storage = self.page.client_storage
        self.api = api

        # control refs
        self.uid_text_field = ft.Ref[ft.TextField]()
        self.result_json = ft.Ref[ft.TextField]()

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
                        ft.Text("Fetching data...", color=ft.colors.ON_SECONDARY_CONTAINER),
                    ]
                ),
                bgcolor=ft.colors.SECONDARY_CONTAINER,
            )
        )

        uid = self.uid_text_field.current.value
        if not uid:
            return await self.page.show_snack_bar_async(
                ft.SnackBar(
                    ft.Text("Please enter a UID.", color=ft.colors.ON_ERROR_CONTAINER),
                    bgcolor=ft.colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.colors.ON_ERROR_CONTAINER,
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
            LOGGER_.exception("Failed to fetch data.")
            return await self.page.show_snack_bar_async(
                ft.SnackBar(
                    ft.Text(f"Error: {e}", color=ft.colors.ON_ERROR_CONTAINER),
                    bgcolor=ft.colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.colors.ON_ERROR_CONTAINER,
                )
            )
        if not response.characters:
            return await self.page.show_snack_bar_async(
                ft.SnackBar(
                    ft.Text(
                        "Error: No characters found in Character Showcase.",
                        color=ft.colors.ON_ERROR_CONTAINER,
                    ),
                    bgcolor=ft.colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.colors.ON_ERROR_CONTAINER,
                )
            )
        try:
            converted = EnkaToGOConverter.convert(response.characters)
        except Exception:
            LOGGER_.exception("Failed to convert data.")
            return await self.page.show_snack_bar_async(
                ft.SnackBar(
                    ft.Text(
                        "Error: Failed to convert data.",
                        color=ft.colors.ON_ERROR_CONTAINER,
                    ),
                    bgcolor=ft.colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.colors.ON_ERROR_CONTAINER,
                )
            )

        converted_json = json.dumps(converted, indent=4)
        self.result_json.current.value = converted_json
        await self.result_json.current.update_async()

        await self.page.show_snack_bar_async(
            ft.SnackBar(
                ft.Text("Complete.", color=ft.colors.ON_TERTIARY_CONTAINER),
                bgcolor=ft.colors.TERTIARY_CONTAINER,
                show_close_icon=True,
                close_icon_color=ft.colors.ON_TERTIARY_CONTAINER,
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
                    ft.Text("There is nothing to copy.", color=ft.colors.ON_ERROR_CONTAINER),
                    bgcolor=ft.colors.ERROR_CONTAINER,
                    show_close_icon=True,
                    close_icon_color=ft.colors.ON_ERROR_CONTAINER,
                )
            )

    async def _popup_menu_item_on_click(self, e: ft.ControlEvent) -> None:
        await self.page.launch_url_async(e.control.data)

    async def add_controls(self) -> None:
        storage_uid = await self.storage.get_async("uid")
        self.page.appbar = ft.AppBar(
            title=ft.Container(
                ft.Text("Enka to GO", size=20),
                margin=ft.margin.symmetric(vertical=10),
            ),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            icon=ft.icons.CHAT_OUTLINED,
                            text="Contact me on Discord",
                            data="https://discord.com/users/410036441129943050",
                            on_click=self._popup_menu_item_on_click,
                        ),
                        ft.PopupMenuItem(
                            icon=ft.icons.CODE_OUTLINED,
                            text="Source code",
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
                        ft.Row(
                            [
                                ft.Container(
                                    ft.TextField(
                                        ref=self.uid_text_field,
                                        label="UID",
                                        hint_text="901211014",
                                        max_length=9,
                                        value=storage_uid,
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
