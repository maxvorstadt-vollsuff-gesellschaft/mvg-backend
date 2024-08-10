from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel
from .member import Member


class EventBase(BaseModel):
    name: str
    start_time: datetime
    location: Optional[str]
    duration: Optional[int] = Field(None, description="Duration in Minutes")


class EventCreate(EventBase):
    author_id: Optional[int]


class EventUpdate(EventBase):
    pass


class Event(EventBase):
    id: int
    participants: list[Member]
    author: Optional[Member]

    class Config:
        from_attributes = True
