from datetime import datetime
from typing import Optional

from pydantic import Field, field_validator
from pydantic.main import BaseModel
from .member import Member
from ..rbac import Roles


class EventBase(BaseModel):
    name: str
    start_time: datetime
    location: Optional[str]
    duration: Optional[int] = Field(None, description="Duration in Minutes. Null means open end.")
    view_role: Roles = Field(
        default=Roles.GUEST, 
        description="Minimum role required to view this event"
    )
    participate_role: Roles = Field(
        default=Roles.MVG_MEMBER, 
        description="Minimum role required to participate in this event"
    )
    edit_role: Roles = Field(
        default=Roles.MVG_MEMBER, 
        description="Minimum role required to edit this event"
    )

    """ @field_validator('edit_role', 'participate_role')
    def role_hierarchy_check(cls, v, values):
        # Ensure that edit and participate roles are at least as restrictive as view role
        view_role = values.get('view_role')
        if view_role and v.value < view_role.value:
            raise ValueError(f"Role must be at least as restrictive as view_role ({view_role})")
        return v
 """

class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    location: Optional[str] = None
    duration: Optional[int] = None
    view_role: Optional[Roles] = None
    participate_role: Optional[Roles] = None
    edit_role: Optional[Roles] = None


class Event(EventBase):
    id: int
    participants: list[Member]
    author: Optional[Member]

    class Config:
        from_attributes = True
