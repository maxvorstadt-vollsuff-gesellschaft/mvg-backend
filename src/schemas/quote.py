from pydantic import BaseModel
from .member import Member


class QuoteBase(BaseModel):
    quote: str


class QuoteCreate(QuoteBase):
    author_id: int


class Quote(QuoteBase):
    id: int
    author: Member

    class Config:
        from_attributes = True
