from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .member import Member
from .event import Event


class Drink(Base):
    __tablename__ = 'drinks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    drink: Mapped[str] = mapped_column(String, nullable=False)
    ml_alc: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    consumer_id: Mapped[str] = mapped_column(String, ForeignKey("members.user_sub"), nullable=False)
    consumer: Mapped[Member] = relationship("Member", foreign_keys=[consumer_id])
    event: Mapped[Optional[Event]] = relationship("Event")
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), nullable=True)
    posted_by: Mapped[str] = mapped_column(String, ForeignKey("members.user_sub"), nullable=True)
