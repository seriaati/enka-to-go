import json
from typing import Any, Dict, List

from ..enka.models.character import Character
from .maps import GO_ELEMENT_MAP, GO_EQUIPMENT_TYPE_MAP, GO_STAT_KEY_MAP

with open("data/text_map.json", "r") as f:
    TEXT_MAP: Dict[str, str] = json.load(f)
with open("data/avatar_excel_config_data.json", "r") as f:
    AVATAR_EXCEL: List[Dict[str, Any]] = json.load(f)
with open("data/characters.json", "r") as f:
    CHARACTER_DATA: Dict[str, Dict[str, Any]] = json.load(f)


class EnkaToGOConverter:
    @staticmethod
    def _get_text(key: str) -> str:
        key = str(key)
        text = (
            TEXT_MAP.get(key, key)
            .replace("'", "")
            .replace('"', "")
            .replace("-", " ")
            .title()
            .replace(" ", "")
        )
        return text

    @staticmethod
    def _get_talent_order(character_id: int) -> List[int]:
        return CHARACTER_DATA[str(character_id)]["SkillOrder"]

    @classmethod
    def _get_character_name(cls, character_id: int, skill_depot_id: int) -> str:
        excel = next((x for x in AVATAR_EXCEL if x["id"] == character_id), None)
        if excel is None:
            return "Unknown"
        name = cls._get_text(excel["nameTextMapHash"])
        if character_id in (10000005, 10000007):
            element = next(
                (
                    v["Element"]
                    for k, v in CHARACTER_DATA.items()
                    if k == f"{character_id}-{skill_depot_id}"
                ),
                None,
            )
            if element is None:
                return f"{name}Anemo"
            return f"{name}{GO_ELEMENT_MAP[element]}"
        return name

    @classmethod
    def _get_talent_levels(
        cls, character_id: int, talents: Dict[str, int]
    ) -> List[int]:
        return [talents.get(str(x), 1) for x in cls._get_talent_order(character_id)]

    @classmethod
    def convert(cls, characters: List[Character]) -> Dict[str, Any]:
        base = {
            "format": "GOOD",
            "version": 2,
            "source": "Enka.Network",
            "characters": [],
            "artifacts": [],
            "weapons": [],
        }

        for character in characters:
            # character
            character_key = cls._get_character_name(
                character.id, character.skill_depot_id
            )
            talent_levels = cls._get_talent_levels(character.id, character.skills)
            base["characters"].append(
                {
                    "key": character_key,
                    "level": character.level,
                    "ascension": character.ascension,
                    "talent": {
                        "auto": talent_levels[0],
                        "skill": talent_levels[1],
                        "burst": talent_levels[2],
                    },
                }
            )

            # weapon
            weapon = character.weapon
            base["weapons"].append(
                {
                    "key": cls._get_text(weapon.detailed_info.name_text_map_hash),
                    "level": weapon.base_info.level,
                    "ascension": weapon.base_info.ascension,
                    "refinement": weapon.base_info.refinement,
                    "location": character_key,
                    "lock": False,
                }
            )

            # artifacts
            for artifact in character.artifacts:
                base["artifacts"].append(
                    {
                        "setKey": cls._get_text(
                            artifact.detailed_info.set_name_text_map_hash
                        ),
                        "slotKey": GO_EQUIPMENT_TYPE_MAP[
                            artifact.detailed_info.equip_type
                        ],
                        "rarity": artifact.detailed_info.rarity,
                        "level": artifact.base_info.level,
                        "mainStatKey": GO_STAT_KEY_MAP[
                            artifact.detailed_info.main_stat.type
                        ],
                        "location": character_key,
                        "substats": [
                            {
                                "key": GO_STAT_KEY_MAP[ss.type],
                                "value": ss.value,
                            }
                            for ss in artifact.detailed_info.sub_stats
                        ],
                        "lock": False,
                    }
                )

        return base
