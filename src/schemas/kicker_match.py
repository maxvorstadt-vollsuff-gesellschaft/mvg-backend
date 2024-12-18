from pydantic import BaseModel
from typing import Optional

from .member import Member

class KickerMatchBase(BaseModel):
    team_a_score: int
    team_b_score: int
    team_a_player_1: str
    team_a_player_2: Optional[str] = None
    team_b_player_1: str
    team_b_player_2: Optional[str] = None

class KickerMatchCreate(KickerMatchBase):
    pass

class KickerMatch(KickerMatchBase):
    id: int
    team_a_player_1_member: Member
    team_a_player_2_member: Optional[Member] = None
    team_b_player_1_member: Member
    team_b_player_2_member: Optional[Member] = None

    class Config:
        from_attributes = True