from __future__ import annotations

import re
import string

from enka.zzz import ZZZClient

from .maps import ZO_SETS_MAP


def _format_name(name: str) -> str:
    """
    Format the set name to match the expected format (e.g. "Moonlight Lullaby" -> "MoonlightLullaby").
    Removes spaces and non-alphanumeric characters.
    """
    return re.sub(r"[^a-zA-Z0-9]", "", string.capwords(name))


async def load_data() -> None:
    """
    Fetch ZZZ assets and populate the ZO_SETS_MAP with dynamic data.
    """
    async with ZZZClient() as client:
        # Access assets. accessing text_map property might trigger load
        # ZZZClient seems to use _assets
        assets = client._assets

        text_map = assets.text_map
        if not text_map:
            return

        # If text_map is a dict of languages (raw struct), pick 'en'
        # Check if the first value is a dict
        if text_map:
            first_val = next(iter(text_map.values()))
            if isinstance(first_val, dict):
                text_map = text_map.get("en", text_map)

        # Pattern to match EquipmentSuit_{id}_Name
        # Actual key in text_map.json seems to be "EquipmentSuit_{id}_name" (lowercase n)

        for key, value in text_map.items():
            # Check for keys like EquipmentSuit_{id}_name / _Name
            # And exclude 2pc/4pc keys like EquipmentSuit_{id}_2_Name
            if key.startswith("EquipmentSuit_"):
                # Case insensitive check for suffix
                if key.lower().endswith("_name") and "_2_" not in key and "_4_" not in key:
                    parts = key.split("_")
                    # Expected: EquipmentSuit, ID, name
                    if len(parts) >= 3:
                        try:
                            set_id = int(parts[1])
                            formatted_name = _format_name(value)
                            ZO_SETS_MAP[set_id] = formatted_name
                        except ValueError:
                            continue
