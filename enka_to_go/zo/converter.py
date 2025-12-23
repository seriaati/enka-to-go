from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .maps import ZO_SLOT_MAP, ZO_STAT_KEY_MAP, ZO_SETS_MAP, ZO_SKILL_MAP

if TYPE_CHECKING:
    from enka.zzz import Agent, DriveDisc, WEngine


class EnkaToZOConverter:
    @classmethod
    def _format_key(cls, key: str) -> str:
        # Standard GO/ZO formatting: Remove spaces/special chars, CamelCase often implied by input but simple removal works for most
        # e.g. "Deep Sea Visitor" -> "DeepSeaVisitor"
        # "Soldier 11" -> "Soldier11"
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

        # Counters for generating unique IDs if needed, though using charID+slot usually safer for dedup
        # But sample uses 'zzz_disc_0'. I'll use 'enka_disc_{id}' to avoid collisions if merged?
        # Actually user creates a NEW db usually. I'll use a simple counter or ID based.
        # Using ID from Enka is best if available. Disc has ID.

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
                    "modification": we.modification, # Rank/Modification? Verify terminology. Enka has modification level?
                    # Sample: "modification": 5. "phase": 1.
                    # Enka WEngine has 'modification' (rank?) and 'phase' (ascension?)
                    # Let's check w_engine attrs in fetch_debug output:
                    # modification=5, phase=1. Matches sample.
                    "phase": we.phase,
                    "location": char_key,
                    "lock": we.is_locked,
                    "id": we_id,
                })

            # Discs
            for disc in agent.discs:
                slot_key = ZO_SLOT_MAP.get(disc.slot, str(disc.slot)) # Enka slot 1-6
                disc_id = f"enka_disc_{disc.id}"
                equipped_discs[slot_key] = disc_id

                # Set Key
                set_key = ZO_SETS_MAP.get(disc.set_id, f"UnknownSet_{disc.set_id}")

                # Substats
                # Sample: [{"key": "hp", "upgrades": 2}, ...]
                # Upgrade count is tricky. Enka provides `roll_times`?
                # fetch_debug output: sub_stat=DriveDiscStat(..., roll_times=3, ...)
                # Yes, roll_times exists!

                substats = []
                for ss in disc.sub_stats:
                    substats.append({
                        "key": ZO_STAT_KEY_MAP.get(ss.type, f"Unknown_{ss.type.name}"),
                        "upgrades": ss.roll_times, # Sample uses key 'upgrades'? Sample: "upgrades": 2
                        # Wait, sample substats don't have value?
                        # Sample: "substats": [{"key": "hp", "upgrades": 2}, {"key": "atk_", "upgrades": 3}]
                        # It seems ZZZ Optimizer MIGHT deduce value from upgrades + type + rarity?
                        # OR simply doesn't care about exact value for input?
                        # Actually let's check Sample again.
                        # "substats": [{"key": "hp", "upgrades": 2}, ...]
                        # NO VALUE field. Interesting.
                        # But wait, Enka provides value.
                        # Maybe I should provide value if possible or just roll_times.
                        # If format requires NO value, I stick to sample.
                        # But standard formatting usually includes value.
                        # ZZZ discs have fixed values per roll?
                        # If sample lacks value, I will NOT include it to be safe (strict schema?).
                        # Or maybe `value` is optional.
                        # I'll stick to sample structure: key, upgrades.
                    })

                base["discs"].append({
                    "setKey": set_key,
                    "rarity": "S", # Hardcode to S?
                    # Enka has 'rarity_num'. Sample has 'rarity': "S".
                    # Mapping: 4 -> S, 3 -> A, 2 -> B.
                    # fetch_debug output: rarity_num=4, rarity='S'.
                    # Enka DriveDisc has .rarity (returns 'S' string?)
                    # fetch_debug: rarity='S'. yes!
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
            # Sample: "dodge": 1, "basic": 1, ...
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
            # Sample has "core": 6.
            # Enka Agent has 'core_skill_level_num'? Or skill with type CORE_SKILL?
            # fetch_debug output: AgentSkill(level=7, type=CORE_SKILL).
            # So I can get it from skills map too.
            core_val = skills_map.get("core", 1)
            # Note: Sample "core": 6.

            base["characters"].append({
                "key": char_key,
                "level": agent.level,
                "promotion": agent.promotion, # Promotion level (0-5?)
                # Sample: "promotion": 5.
                "mindscape": agent.mindscape,
                "core": core_val,
                "dodge": skills_map["dodge"],
                "basic": skills_map["basic"],
                "chain": skills_map["chain"],
                "special": skills_map["special"],
                "assist": skills_map["assist"],
                "id": char_key, # Sample uses ID = Name (Key)
                "equippedDiscs": equipped_discs,
                "equippedWengine": equipped_wengine,
            })

        return base
