from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Card(Base):
    __tablename__ = 'cards'

    member_id: Mapped[int] = mapped_column(Integer, ForeignKey('members.id'), primary_key=True)
    card_uid: Mapped[str] = mapped_column(String, index=True, unique=True)
