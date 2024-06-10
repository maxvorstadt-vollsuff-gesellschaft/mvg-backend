from pydantic import BaseModel
from .member import Member


class QuoteBase(BaseModel):
    quote: str
    author: Member


class QuoteCreate(QuoteBase):
    pass


class Quote(QuoteBase):
    id: int

    class Config:
        from_attributes = True
