from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from member import Member
    from quote_rotation import QuoteRotation


class Quote(Base):
    __tablename__ = 'quotes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    quote: Mapped[str] = mapped_column(String)
    author_id: Mapped[str] = mapped_column(String, ForeignKey("members.user_sub"), nullable=False)
    author: Mapped["Member"] = relationship("Member", back_populates="quotes")
    rotations: Mapped[list["QuoteRotation"]] = relationship("QuoteRotation", back_populates="quote", lazy='select')
    date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    location: Mapped[str] = mapped_column(String)
