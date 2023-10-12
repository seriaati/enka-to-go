from typing import List

from pydantic import BaseModel, Field

from .character import Character
from .player import Player


class ShowcaseResponse(BaseModel):
    characters: List[Character] = Field(alias="avatarInfoList")
    player: Player = Field(alias="playerInfo")
    ttl: int
    uid: str
