from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class CalendarLink(Base):
    __tablename__ = "calendar_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    member_sub: Mapped[str] = mapped_column(String, nullable=False)
    tag: Mapped[str] = mapped_column(String, nullable=False)
