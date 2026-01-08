from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .maps import GO_EQUIPMENT_TYPE_MAP, GO_STAT_KEY_MAP

if TYPE_CHECKING:
    from enka.gi import Character, Talent

TRAVELER_IDS = {10000005, 10000007}


def is_traveler(character_id: int) -> bool:
    return character_id in TRAVELER_IDS


class EnkaToGOConverter:
    @classmethod
    def _format_key(cls, key: str) -> str:
        return key.replace("'", "").replace('"', "").replace("-", " ").title().replace(" ", "")

    @classmethod
    def _get_talent_levels(cls, talents: list[Talent], talent_order: list[int]) -> list[int]:
        talent_levels: list[int] = [1, 1, 1]
        for i, talent_id in enumerate(talent_order):
            talent = next((t for t in talents if t.id == talent_id), None)
            if talent is None:
                continue
            talent_levels[i] = talent.level

        return talent_levels

    @classmethod
    def convert(cls, characters: list[Character]) -> dict[str, Any]:
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
            if is_traveler(character.id):
                character_name = f"Traveler{character.element.name.title()}"
            else:
                character_name = character.name

            talent_levels = cls._get_talent_levels(character.talents, character.talent_order)
            base["characters"].append(
                {
                    "key": cls._format_key(character_name),
                    "level": character.level,
                    "ascension": character.ascension,
                    "talent": {
                        "auto": talent_levels[0],
                        "skill": talent_levels[1],
                        "burst": talent_levels[2],
                    },
                    "constellation": character.constellations_unlocked,
                }
            )

            # resset character name because GO uses Traveler for location, not TravelerDendro or TravelerAnemo
            character_name = "Traveler" if is_traveler(character.id) else character.name

            # weapon
            weapon = character.weapon
            base["weapons"].append(
                {
                    "key": cls._format_key(weapon.name),
                    "level": weapon.level,
                    "ascension": weapon.ascension,
                    "refinement": weapon.refinement,
                    "location": cls._format_key(character_name),
                    "lock": False,
                }
            )

            # artifacts
            for artifact in character.artifacts:
                base["artifacts"].append(
                    {
                        "setKey": cls._format_key(artifact.set_name),
                        "slotKey": GO_EQUIPMENT_TYPE_MAP[artifact.equip_type],
                        "rarity": artifact.rarity,
                        "level": artifact.level,
                        "mainStatKey": GO_STAT_KEY_MAP[artifact.main_stat.type],
                        "location": cls._format_key(character_name),
                        "substats": [
                            {
                                "key": GO_STAT_KEY_MAP[ss.type],
                                "value": ss.value,
                            }
                            for ss in artifact.sub_stats
                        ],
                        "lock": False,
                    }
                )

        return base
