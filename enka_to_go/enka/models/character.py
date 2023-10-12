from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from ..enums import EquipmentType, ItemType, StatType


class MainStat(BaseModel):
    type: StatType = Field(alias="mainPropId")
    value: float = Field(alias="statValue")


class SubStat(BaseModel):
    type: StatType = Field(alias="appendPropId")
    value: float = Field(alias="statValue")


class ArtifactDetailedInfo(BaseModel):
    equip_type: EquipmentType = Field(alias="equipType")
    icon: str
    item_type: ItemType = Field(alias="itemType")
    name_text_map_hash: str = Field(alias="nameTextMapHash")
    rarity: int = Field(alias="rankLevel")
    main_stat: MainStat = Field(alias="reliquaryMainstat")
    sub_stats: List[SubStat] = Field(alias="reliquarySubstats")
    set_name_text_map_hash: str = Field(alias="setNameTextMapHash")


class ArtifactBaseInfo(BaseModel):
    main_stat_id: int = Field(alias="mainPropId")
    sub_stat_id_list: List[int] = Field(alias="appendPropIdList")
    level: int

    @field_validator("level", mode="before")
    def _convert_level(cls, v: int) -> int:
        return v - 1


class Artifact(BaseModel):
    item_id: int = Field(alias="itemId")
    detailed_info: ArtifactDetailedInfo = Field(alias="flat")
    base_info: ArtifactBaseInfo = Field(alias="reliquary")


class WeaponStat(BaseModel):
    type: StatType = Field(alias="appendPropId")
    value: float = Field(alias="statValue")


class WeaponDetailedInfo(BaseModel):
    icon: str
    item_type: ItemType = Field(alias="itemType")
    name_text_map_hash: str = Field(alias="nameTextMapHash")
    rarity: int = Field(alias="rankLevel")
    stats: List[WeaponStat] = Field(alias="weaponStats")


class WeaponBaseInfo(BaseModel):
    refinement: int = Field(1, alias="affixMap")
    level: int
    ascension: int = Field(0, alias="promoteLevel")

    @field_validator("refinement", mode="before")
    def _extract_refinement(cls, v: Dict[str, int]) -> int:
        return list(v.values())[0]


class Weapon(BaseModel):
    item_id: int = Field(alias="itemId")
    detailed_info: WeaponDetailedInfo = Field(alias="flat")
    base_info: WeaponBaseInfo = Field(alias="weapon")


class Character(BaseModel):
    id: int = Field(alias="avatarId")
    artifacts: List[Artifact]
    weapon: Weapon
    stat_map: Dict[str, float] = Field(alias="fightPropMap")
    constellations: int = Field(0, alias="talentIdList")
    skills: Dict[str, int] = Field(alias="skillLevelMap")
    ascension: int
    level: int
    skill_depot_id: int = Field(alias="skillDepotId")

    @field_validator("constellations", mode="before")
    def _convert_constellations(cls, v: Optional[List[int]]) -> int:
        if v is None:
            return 0
        return len(v)

    @model_validator(mode="before")
    def _transform_values(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        # convert prop map to level and ascension
        prop_map = v["propMap"]
        try:
            v["level"] = prop_map["4001"]["val"]
        except KeyError:
            v["level"] = 1
        try:
            v["ascension"] = prop_map["1002"]["val"]
        except KeyError:
            v["ascension"] = 0

        # convert equipment list to weapon and artifacts
        equip_list = v["equipList"]
        v["artifacts"] = []

        for equipment in equip_list:
            if "weapon" in equipment:
                v["weapon"] = equipment
            elif "reliquary" in equipment:
                v["artifacts"].append(equipment)
            else:
                raise ValueError("Unknown item type")

        return v
