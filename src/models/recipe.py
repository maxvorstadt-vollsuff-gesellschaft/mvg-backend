from sqlalchemy import Integer, String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from enum import Enum as PyEnum

from .base import Base
from .member import Member  # Assuming you have a Member model

class TimeOfDay(PyEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"

class ComplexityLevel(PyEnum):
    EASY = "5-15"
    MEDIUM = "15-35"
    HARD = "40+"

class Recipe(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    time_of_day: Mapped[TimeOfDay] = mapped_column(Enum(TimeOfDay), nullable=False)
    complexity: Mapped[Optional[ComplexityLevel]] = mapped_column(Enum(ComplexityLevel), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('members.id'), nullable=False)
    author: Mapped[Member] = relationship("Member", back_populates="recipes")
