from sqlalchemy import Float, Integer, String, Table, Column, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from .base import Base

if TYPE_CHECKING:
    from event import Event
    from quote import Quote
    from recipe import Recipe


association_table = Table(
    "participated",
    Base.metadata,
    Column("member_id", ForeignKey("members.user_sub", ondelete="CASCADE")),
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE")),
    Column("vollsuff", Boolean)
)


class Member(Base):
    __tablename__ = 'members'

    id: Mapped[int] = mapped_column(Integer, index=True, autoincrement=True, nullable=True, default=0)
    user_sub: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    participated_in: Mapped[List["Event"]] = relationship(
        "Event",
        secondary=association_table,
        back_populates="participants",
        lazy='select'
    )
    quotes: Mapped[List["Quote"]] = relationship("Quote", lazy='select', back_populates="author")
    events: Mapped[List["Event"]] = relationship("Event", lazy='select', back_populates="author")
    recipes: Mapped[list["Recipe"]] = relationship("Recipe", back_populates="author")
    tkt_elo_rating: Mapped[float] = mapped_column(Float, default=1000)
