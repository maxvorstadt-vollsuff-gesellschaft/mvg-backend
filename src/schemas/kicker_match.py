import datetime
from pydantic import BaseModel, field_validator
from typing import Optional

from .member import Member

class KickerMatchBase(BaseModel):
    team_a_score: int
    team_b_score: int
    team_a_player_1: str
    team_a_player_2: Optional[str] = None
    team_b_player_1: str
    team_b_player_2: Optional[str] = None
    history: Optional[str] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    history: Optional[str] = None

    @field_validator('start_time', 'end_time')
    def parse_datetime(cls, value):
        if isinstance(value, int):
            return datetime.datetime.fromtimestamp(value)
        return value
    
    @field_validator('history')
    def parse_history(cls, value):
        if value is not None and not all(c in 'AB' for c in value):
            raise ValueError("History can only contain the letters 'A' and 'B'.")
        return value

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