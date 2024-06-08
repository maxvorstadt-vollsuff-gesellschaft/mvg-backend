from sqlalchemy import Integer, String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from .base import Base

if TYPE_CHECKING:
    from event import Event


association_table = Table(
    "participated",
    Base.metadata,
    Column("member_id", ForeignKey("members.id")),
    Column("event_id", ForeignKey("events.id")),
)


class Member(Base):
    __tablename__ = 'members'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    participated_in: Mapped[List["Event"]] = relationship(
        "Event",
        secondary=association_table,
        back_populates="participants",
        lazy='select'
    )
