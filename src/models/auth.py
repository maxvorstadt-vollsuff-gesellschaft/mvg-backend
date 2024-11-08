from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Auth(Base):
    __tablename__ = 'auth'

    member_id: Mapped[str] = mapped_column(String, ForeignKey('members.user_sub'), primary_key=True)
    pw_hash: Mapped[str] = mapped_column(String)
    user_name: Mapped[str] = mapped_column(String, unique=True)
