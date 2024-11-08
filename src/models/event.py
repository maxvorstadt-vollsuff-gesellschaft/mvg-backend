from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, List

from .base import Base
from .member import association_table
from ..rbac import Roles

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
    author_sub: Mapped[str] = mapped_column(
        String, 
        ForeignKey("members.user_sub"), 
        nullable=False,
        index=True
    )
    author: Mapped["Member"] = relationship(
        "Member", 
        foreign_keys=[author_sub],
        primaryjoin="Event.author_sub == Member.user_sub",
        back_populates="events"
    )
    duration: Mapped[int] = mapped_column(Integer, nullable=True)  # duration in minutes, null=open ended
    
    # RBAC fields
    view_role: Mapped[str] = mapped_column(
        SQLEnum(Roles), 
        nullable=False, 
        default=Roles.GUEST.value
    )
    participate_role: Mapped[str] = mapped_column(
        SQLEnum(Roles), 
        nullable=False, 
        default=Roles.MVG_MEMBER.value
    )
    edit_role: Mapped[str] = mapped_column(
        SQLEnum(Roles), 
        nullable=False, 
        default=Roles.MVG_MEMBER.value
    )

    def can_view(self, user_roles: list[str]) -> bool:
        return self.view_role in user_roles

    def can_participate(self, user_roles: list[str]) -> bool:
        return self.participate_role in user_roles

    def can_edit(self, user_roles: list[str], user_id: int) -> bool:
        return self.edit_role in user_roles or self.author_id == user_id
