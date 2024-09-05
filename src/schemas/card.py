from pydantic import BaseModel


class BaseCard(BaseModel):
    member_id: int
    card_uid: str


class Card(BaseCard):
    pass


class CreateCard(BaseCard):
    pass
