from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Auth(Base):
    __tablename__ = 'auth'

    member_id: Mapped[int] = mapped_column(Integer, ForeignKey('members.id'), primary_key=True)
    pw_hash: Mapped[str] = mapped_column(String)
    user_name: Mapped[str] = mapped_column(String, unique=True)
