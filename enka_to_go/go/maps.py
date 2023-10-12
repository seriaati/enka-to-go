from typing import Dict

from ..enka.enums import EquipmentType, StatType

GO_EQUIPMENT_TYPE_MAP: Dict[EquipmentType, str] = {
    EquipmentType.FLOWER: "flower",
    EquipmentType.FEATHER: "plume",
    EquipmentType.SANDS: "sands",
    EquipmentType.GOBLET: "goblet",
    EquipmentType.CIRCLET: "circlet",
}

GO_STAT_KEY_MAP: Dict[StatType, str] = {
    StatType.FLAT_HP: "hp",
    StatType.HP_PERCENT: "hp_",
    StatType.FLAT_ATK: "atk",
    StatType.ATK_PERCENT: "atk_",
    StatType.FLAT_DEF: "def",
    StatType.DEF_PERCENT: "def_",
    StatType.ELEMENTAL_MASTERY: "eleMas",
    StatType.ENERGY_RECHARGE: "enerRech_",
    StatType.HEALING_BONUS: "heal_",
    StatType.CRIT_RATE: "critRate_",
    StatType.CRIT_DMG: "critDMG_",
    StatType.PHYSICAL_DMG_BONUS: "physical_dmg_",
    StatType.ANEMO_DMG_BONUS: "anemo_dmg_",
    StatType.ELECTRO_DMG_BONUS: "electro_dmg_",
    StatType.HYDRO_DMG_BONUS: "hydro_dmg_",
    StatType.PYRO_DMG_BONUS: "pyro_dmg_",
    StatType.CRYO_DMG_BONUS: "cryo_dmg_",
    StatType.GEO_DMG_BONUS: "geo_dmg_",
    StatType.DENDRO_DMG_BONUS: "dendro_dmg_",
}
