from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .maps import ZO_SETS_MAP, ZO_SKILL_MAP, ZO_SLOT_MAP, ZO_STAT_KEY_MAP

if TYPE_CHECKING:
    from enka.zzz import Agent


class EnkaToZOConverter:
    @classmethod
    def _format_key(cls, key: str) -> str:
        return key.replace("'", "").replace('"', "").replace("-", " ").title().replace(" ", "")

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

        for agent in agents:
            # Character
            char_key = cls._format_key(agent.name)

            equipped_discs = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": ""}
            equipped_wengine = ""

            # WEngine
            if agent.w_engine:
                we = agent.w_engine
                we_id = f"enka_wengine_{we.id}"
                equipped_wengine = we_id

                base["wengines"].append({
                    "key": cls._format_key(we.name),
                    "level": we.level,
                    "modification": we.modification,
                    "phase": we.phase,
                    "location": char_key,
                    "lock": we.is_locked,
                    "id": we_id,
                })

            # Discs
            for disc in agent.discs:
                slot_key = ZO_SLOT_MAP.get(disc.slot, str(disc.slot))
                disc_id = f"enka_disc_{disc.id}"
                equipped_discs[slot_key] = disc_id

                # Set Key
                set_key = ZO_SETS_MAP.get(disc.set_id, f"UnknownSet_{disc.set_id}")

                # Substats
                substats = []
                for ss in disc.sub_stats:
                    substats.append({
                        "key": ZO_STAT_KEY_MAP.get(ss.type, f"Unknown_{ss.type.name}"),
                        "upgrades": ss.roll_times,
                    })

                base["discs"].append({
                    "setKey": set_key,
                    "rarity": disc.rarity,
                    "level": disc.level,
                    "slotKey": slot_key,
                    "mainStatKey": ZO_STAT_KEY_MAP.get(disc.main_stat.type, f"Unknown_{disc.main_stat.type.name}"),
                    "substats": substats,
                    "location": char_key,
                    "lock": disc.is_locked,
                    "trash": disc.is_trash,
                    "id": disc_id,
                })

            # Skills
            skills_map = {}
            if agent.skills:
                for skill in agent.skills:
                    s_key = ZO_SKILL_MAP.get(skill.type)
                    if s_key:
                        skills_map[s_key] = skill.level

            # Fill defaults 1 if missing
            for k in ["dodge", "basic", "chain", "special", "assist"]:
                 if k not in skills_map:
                     skills_map[k] = 1
            # Core
            core_val = skills_map.get("core", 1)

            base["characters"].append({
                "key": char_key,
                "level": agent.level,
                "promotion": agent.promotion,
                "mindscape": agent.mindscape,
                "core": core_val,
                "dodge": skills_map["dodge"],
                "basic": skills_map["basic"],
                "chain": skills_map["chain"],
                "special": skills_map["special"],
                "assist": skills_map["assist"],
                "id": char_key,
                "equippedDiscs": equipped_discs,
                "equippedWengine": equipped_wengine,
            })

        return base
