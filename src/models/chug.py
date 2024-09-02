from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .member import Member
from .base import Base


class Chug(Base):
    __tablename__ = "chugs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("members.id"), nullable=False)
    member: Mapped[Member] = relationship("Member", foreign_keys=[member_id])
    time: Mapped[int] = mapped_column(Integer, nullable=False)
