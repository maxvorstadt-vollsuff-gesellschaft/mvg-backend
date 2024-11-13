from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .event import Event
    from .recipe import Recipe


class MKM(Base):
    __tablename__ = "mkm"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    theme: Mapped[str] = mapped_column(String, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    recipe_id: Mapped[int] = mapped_column(Integer, nullable=True)
    recipe: Mapped["Recipe"] = relationship(
        "Recipe",
        foreign_keys=[recipe_id]
    )

    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'), nullable=False)
    event: Mapped["Event"] = relationship(
        "Event", 
        foreign_keys=[event_id]
    )
