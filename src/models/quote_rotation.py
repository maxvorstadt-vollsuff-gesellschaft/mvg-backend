from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
from .quote import Quote


class QuoteRotation(Base):
    __tablename__ = 'quote_rotation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    quote_id: Mapped[int] = mapped_column(Integer, ForeignKey("quotes.id"), nullable=False)
    quote: Mapped[Quote] = relationship("Quote", back_populates="rotations")
    chosen_at: Mapped[datetime] = mapped_column(DateTime)
