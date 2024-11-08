from datetime import datetime
from typing import Annotated, List
from fastapi import Depends, HTTPException
from ..models import Event, Member
from ..repositories.event import CRUDEvent, get_event_repository
from ..schemas.event import EventCreate

class EventService:
    def __init__(
        self,
        event_repository: Annotated[CRUDEvent, Depends(get_event_repository)]
    ):
        self.event_repository = event_repository

    def get_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        return self.event_repository.get_multi(skip=skip, limit=limit)

    def get_event(self, id: int) -> Event:
        event = self.event_repository.get(id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    def get_upcoming_events(
        self,
        limit: int = 10
    ) -> List[Event]:
        return self.event_repository.get_upcoming_events(limit=limit)

    def create_event(
        self,
        event: EventCreate,
        author: Member
    ) -> Event:
        event_data = event.dict()
        event_data['author_id'] = author.id
        return self.event_repository.create(event_data)

    def participate_in_event(
        self,
        event_id: int,
        member: Member
    ) -> Event:
        try:
            return self.event_repository.participate(event_id, member.id)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

    def remove_participant(
        self,
        event_id: int,
        member: Member
    ) -> Event:
        try:
            return self.event_repository.remove_participant(event_id, member.id)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

def get_event_service(
    event_repo: Annotated[CRUDEvent, Depends(get_event_repository)]
) -> EventService:
    return EventService(event_repo)