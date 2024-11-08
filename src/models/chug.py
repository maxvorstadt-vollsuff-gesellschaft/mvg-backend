from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .member import Member
from .base import Base


class Chug(Base):
    __tablename__ = "chugs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[str] = mapped_column(String, ForeignKey("members.user_sub"), nullable=False)
    member: Mapped[Member] = relationship("Member", foreign_keys=[member_id])
    time: Mapped[int] = mapped_column(Integer, nullable=False)
