from pydantic import BaseModel
from typing import Optional

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

    class Config:
        orm_mode = True 