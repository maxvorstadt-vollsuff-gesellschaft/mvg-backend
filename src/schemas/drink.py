from datetime import datetime
from typing import Optional
from .member import Member
from .event import Event
from pydantic import BaseModel


class BaseDrink(BaseModel):
    drink: str
    ml_alc: int


class DrinkCreate(BaseDrink):
    time: Optional[datetime]
    consumer_id: int
    event_id: Optional[int]


class Drink(BaseDrink):
    id: int
    time: datetime
    consumer: Member
    event: Event

    class Config:
        from_attributes = True
