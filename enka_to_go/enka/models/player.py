from typing import Dict

from pydantic import BaseModel, Field, field_validator


class Player(BaseModel):
    achievements: int = Field(alias="finishAchievementNum")
    level: int
    name_card_id: int = Field(alias="nameCardId")
    nickname: str
    signature: str
    abyss_floor: int = Field(alias="towerFloorIndex")
    abyss_level: int = Field(alias="towerLevelIndex")
    world_level: int = Field(alias="worldLevel")
    profile_picture_avatar_id: int = Field(alias="profilePicture")

    @field_validator("profile_picture_avatar_id", mode="before")
    def _extract_avatar_id(cls, v: Dict[str, int]) -> int:
        return v["avatarId"]
