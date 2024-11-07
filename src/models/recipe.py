from sqlalchemy import Integer, String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from enum import Enum as PyEnum

from .base import Base
from .member import Member  

class Situation(PyEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"

class Recipe(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    situation: Mapped[Situation] = mapped_column(Enum(Situation), nullable=False)
    time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('members.id'), nullable=False)
    author: Mapped[Member] = relationship("Member", back_populates="recipes")
