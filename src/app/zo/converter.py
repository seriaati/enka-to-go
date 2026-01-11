from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .maps import ZO_SKILL_MAP, ZO_STAT_KEY_MAP

if TYPE_CHECKING:
    from enka.zzz import Agent


class EnkaToZOConverter:
    @classmethod
    def _format_key(cls, key: str) -> str:
        return (
            key.replace("'", "")
            .replace('"', "")
            .replace("-", " ")
            .replace("&", "")
            .title()
            .replace(" ", "")
        )

    @classmethod
    def convert(cls, agents: list[Agent]) -> dict[str, Any]:
        base = {
            "format": "ZOD",
            "dbVersion": 2,
            "source": "Enka to GO",
            "version": 1,
            "characters": [],
            "discs": [],
            "wengines": [],
        }

        zod_disc_id = 0
        zod_wengine_id = 0

        for agent in agents:
            # Character
            char_key = cls._format_key(agent.name)

            equipped_discs = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": ""}
            equipped_wengine = ""

            # WEngine
            if (wengine := agent.w_engine) is not None:
                equipped_wengine = f"zzz_wengine_{zod_wengine_id}"
                zod_wengine_id += 1

                base["wengines"].append(
                    {
                        "key": cls._format_key(wengine.name),
                        "level": wengine.level,
                        "modification": wengine.modification,
                        "phase": wengine.phase,
                        "location": char_key,
                        "lock": wengine.is_locked,
                        "id": equipped_wengine,
                    }
                )

            # Discs
            for disc in agent.discs:
                slot_key = str(disc.slot)
                disc_id = f"zzz_disc_{zod_disc_id}"
                equipped_discs[slot_key] = disc_id
                zod_disc_id += 1

                # Set Key
                set_key = cls._format_key(disc.set_name)

                # Substats
                substats = [
                    {
                        "key": ZO_STAT_KEY_MAP.get(ss.type, f"Unknown_{ss.type.name}"),
                        "upgrades": ss.roll_times,
                    }
                    for ss in disc.sub_stats
                ]

                base["discs"].append(
                    {
                        "setKey": set_key,
                        "rarity": disc.rarity,
                        "level": disc.level,
                        "slotKey": slot_key,
                        "mainStatKey": ZO_STAT_KEY_MAP.get(
                            disc.main_stat.type, f"Unknown_{disc.main_stat.type.name}"
                        ),
                        "substats": substats,
                        "location": char_key,
                        "lock": disc.is_locked,
                        "trash": disc.is_trash,
                        "id": disc_id,
                    }
                )

            # Skills
            skills_map = dict.fromkeys(ZO_SKILL_MAP.values(), 1)
            for skill in agent.skills:
                s_key = ZO_SKILL_MAP.get(skill.type)
                if s_key:
                    skills_map[s_key] = skill.level

            base["characters"].append(
                {
                    "key": char_key,
                    "level": agent.level,
                    "promotion": agent.promotion,
                    "mindscape": agent.mindscape,
                    "core": skills_map["core"],
                    "dodge": skills_map["dodge"],
                    "basic": skills_map["basic"],
                    "chain": skills_map["chain"],
                    "special": skills_map["special"],
                    "assist": skills_map["assist"],
                    "id": char_key,
                    "equippedDiscs": equipped_discs,
                    "equippedWengine": equipped_wengine,
                    "potential": agent.potential,
                }
            )

        return base
