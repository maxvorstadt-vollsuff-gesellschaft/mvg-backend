from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from .member import Member


class QuoteBase(BaseModel):
    quote: str
    date: Optional[datetime]
    location: Optional[str]


class QuoteCreate(QuoteBase):
    author_id: int


class Quote(QuoteBase):
    id: int
    author: Member

    class Config:
        from_attributes = True
