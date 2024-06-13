from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel
from .member import Member


class EventBase(BaseModel):
    name: str
    start_time: datetime
    location: Optional[str]


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class Event(EventBase):
    id: int
    participants: list[Member]

    class Config:
        from_attributes = True
