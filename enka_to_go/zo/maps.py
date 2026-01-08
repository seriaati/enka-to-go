from enka.zzz import SkillType, StatType

# Mapping from ZZZ Equipment Slot (1-6) to JSON keys (1-6)
# Simple string conversion is enough, but explicit is good.
ZO_SLOT_MAP: dict[int, str] = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
}

ZO_STAT_KEY_MAP: dict[StatType, str] = {
    StatType.HP_FLAT: "hp",
    StatType.HP_PERCENT: "hp_",
    StatType.HP_BASE: "hp",
    StatType.ATK_FLAT: "atk",
    StatType.ATK_PERCENT: "atk_",
    StatType.ATK_BASE: "atk",
    StatType.DEF_FLAT: "def",
    StatType.DEF_PERCENT: "def_",
    StatType.DEF_BASE: "def",
    StatType.CRIT_RATE_FLAT: "crit_",
    StatType.CRIT_RATE_BASE: "crit_",
    StatType.CRIT_DMG_FLAT: "crit_dmg_",
    StatType.CRIT_DMG_BASE: "crit_dmg_",
    StatType.PEN_FLAT: "pen",
    StatType.PEN_BASE: "pen",
    StatType.PEN_RATIO_FLAT: "pen_",
    StatType.PEN_RATIO_BASE: "pen_",
    StatType.ANOMALY_PRO_FLAT: "anomProf",
    StatType.ANOMALY_PRO_BASE: "anomProf",
    StatType.ANOMALY_MASTERY_FLAT: "anomMas",
    StatType.ANOMALY_MASTERY_PERCENT: "anomMas_",
    StatType.ANOMALY_MASTERY_BASE: "anomMas",
    StatType.ENERGY_REGEN_FLAT: "enerRegen",
    StatType.ENERGY_REGEN_PERCENT: "enerRegen_",
    StatType.ENERGY_REGEN_BASE: "enerRegen",
    StatType.IMPACT_PERCENT: "impact_",
    StatType.IMPACT_BASE: "impact",
    StatType.PHYSICAL_DMG_BONUS_FLAT: "physical_dmg_",
    StatType.PHYSICAL_DMG_BONUS_BASE: "physical_dmg_",
    StatType.FIRE_DMG_BONUS_FLAT: "fire_dmg_",
    StatType.FIRE_DMG_BONUS_BASE: "fire_dmg_",
    StatType.ICE_DMG_BONUS_FLAT: "ice_dmg_",
    StatType.ICE_DMG_BONUS_BASE: "ice_dmg_",
    StatType.ELECTRIC_DMG_BONUS_FLAT: "electric_dmg_",
    StatType.ELECTRIC_DMG_BONUS_BASE: "electric_dmg_",
    StatType.ETHER_DMG_BONUS_FLAT: "ether_dmg_",
    StatType.ETHER_DMG_BONUS_BASE: "ether_dmg_",
}

# Derived from text_map.json (EquipmentSuit_{id}_name)
ZO_SETS_MAP: dict[int, str] = {}


ZO_SKILL_MAP: dict[SkillType, str] = {
    SkillType.BASIC_ATK: "basic",
    SkillType.DASH: "dodge",
    SkillType.SPECIAL_ATK: "special",
    SkillType.ULTIMATE: "chain",
    SkillType.ASSIST: "assist",
    SkillType.CORE_SKILL: "core",
}
