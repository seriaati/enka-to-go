from enka.gi import EquipmentType, StatType

GO_EQUIPMENT_TYPE_MAP: dict[EquipmentType, str] = {
    EquipmentType.FLOWER: "flower",
    EquipmentType.FEATHER: "plume",
    EquipmentType.SANDS: "sands",
    EquipmentType.GOBLET: "goblet",
    EquipmentType.CIRCLET: "circlet",
}

GO_STAT_KEY_MAP: dict[StatType, str] = {
    StatType.FIGHT_PROP_HP: "hp",
    StatType.FIGHT_PROP_HP_PERCENT: "hp_",
    StatType.FIGHT_PROP_ATTACK: "atk",
    StatType.FIGHT_PROP_ATTACK_PERCENT: "atk_",
    StatType.FIGHT_PROP_DEFENSE: "def",
    StatType.FIGHT_PROP_DEFENSE_PERCENT: "def_",
    StatType.FIGHT_PROP_ELEMENT_MASTERY: "eleMas",
    StatType.FIGHT_PROP_CHARGE_EFFICIENCY: "enerRech_",
    StatType.FIGHT_PROP_HEAL_ADD: "heal_",
    StatType.FIGHT_PROP_CRITICAL: "critRate_",
    StatType.FIGHT_PROP_CRITICAL_HURT: "critDMG_",
    StatType.FIGHT_PROP_PHYSICAL_ADD_HURT: "physical_dmg_",
    StatType.FIGHT_PROP_WIND_ADD_HURT: "anemo_dmg_",
    StatType.FIGHT_PROP_ELEC_ADD_HURT: "electro_dmg_",
    StatType.FIGHT_PROP_WATER_ADD_HURT: "hydro_dmg_",
    StatType.FIGHT_PROP_FIRE_ADD_HURT: "pyro_dmg_",
    StatType.FIGHT_PROP_ICE_ADD_HURT: "cryo_dmg_",
    StatType.FIGHT_PROP_ROCK_ADD_HURT: "geo_dmg_",
    StatType.FIGHT_PROP_GRASS_ADD_HURT: "dendro_dmg_",
}
