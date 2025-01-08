from sqlalchemy import Integer, String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from enum import Enum as PyEnum

from .base import Base
from .member import Member  

class Jahreszeit(PyEnum):
    WINTER = "winter"
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    ALL = "all"

class DateIdea(Base):
    __tablename__ = 'date_ideas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    season: Mapped[Jahreszeit] = mapped_column(Enum(Jahreszeit), nullable=False)
    time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    author_id: Mapped[str] = mapped_column(String, ForeignKey('members.user_sub'), nullable=False)
    author: Mapped[Member] = relationship("Member")
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_no: Mapped[int] = mapped_column(Integer, nullable=False)
