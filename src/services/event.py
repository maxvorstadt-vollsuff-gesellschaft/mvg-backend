from typing import Annotated, List, Literal
from fastapi import Depends, HTTPException
from fastapi_keycloak import OIDCUser

from ..models import Event
from ..repositories.event import CRUDEvent, get_event_repository
from ..schemas.event import EventCreate
from ..rbac import check_user_access, Roles

class EventService:
    def __init__(
        self,
        event_repository: Annotated[CRUDEvent, Depends(get_event_repository)]
    ):
        self.event_repository = event_repository

    def check_event_access(
        self, 
        event: Event, 
        user: OIDCUser, 
        required_role: Literal["view", "participate", "edit"]
    ) -> bool:
        # Author always has full access
        if user.sub == event.author_sub:
            return True
            
        if required_role == 'view':
            return any(check_user_access(role, event.view_role) for role in user.roles)
        elif required_role == 'participate':
            return any(check_user_access(role, event.participate_role) for role in user.roles)
        elif required_role == 'edit':
            return any(check_user_access(role, event.edit_role) for role in user.roles)

    def get_events(self, user: OIDCUser, skip: int = 0, limit: int = 100) -> List[Event]:
        events = self.event_repository.get_multi(skip=skip, limit=limit)
        return [e for e in events if self.check_event_access(e, user, 'view')]

    def get_event(self, id: int, user: OIDCUser) -> Event:
        event = self.event_repository.get(id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        if not self.check_event_access(event, user, 'view'):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return event

    def create_event(
        self,
        event: EventCreate,
        user: OIDCUser
    ) -> Event:
        print(user.roles)
        if not any(check_user_access(role, Roles.MVG_MEMBER.value) for role in user.roles):
            raise HTTPException(
                status_code=403, 
                detail="You don't have permission to create events"
            )
        
        event_data = event.model_dump()
        event_data['author_sub'] = user.sub
        return self.event_repository.create(event_data)

    def participate_in_event(self, event_id: int, user: OIDCUser) -> Event:
        event = self.event_repository.get(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        if not self.check_event_access(event, user, 'participate'):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        try:
            return self.event_repository.participate(event_id, user.sub)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

    def remove_participant(
        self,
        event_id: int,
        user: OIDCUser
    ) -> Event:
        try:
            return self.event_repository.remove_participant(event_id, user.sub)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

    def get_upcoming_events(
        self,
        user: OIDCUser,
        limit: int = 10
    ) -> List[Event]:
        events = self.event_repository.get_upcoming_events(limit=100) # hack but works for now
        return [e for e in events if self.check_event_access(e, user, 'view')][:limit]

    def get_accessible_events(
        self,
        user: OIDCUser,
        skip: int = 0,
        limit: int = 100
    ) -> List[Event]:
        events = self.event_repository.get_multi(skip=skip, limit=limit)
        return [e for e in events if self.check_event_access(e, user, 'view')]

    def delete_event(self, id: int, user: OIDCUser) -> Event:
        event = self.event_repository.get(id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        if not self.check_event_access(event, user, 'edit'):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return self.event_repository.remove(id)


def get_event_service(
    event_repo: Annotated[CRUDEvent, Depends(get_event_repository)]
) -> EventService:
    return EventService(event_repo)