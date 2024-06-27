from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, List

from .base import Base
from .member import association_table

if TYPE_CHECKING:
    from member import Member


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    participants: Mapped[List["Member"]] = relationship(
        "Member",
        secondary=association_table,
        back_populates="participated_in"
    )
    location: Mapped[str] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("members.id"), nullable=False)
    author: Mapped["Member"] = relationship("Member", back_populates="events")
