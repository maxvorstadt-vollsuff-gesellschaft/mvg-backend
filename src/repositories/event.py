from datetime import datetime
from typing import Annotated, List
from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Member, Event
from .base import CRUDBase

class CRUDEvent(CRUDBase[Event]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(Event, db)

    def get_next_upcoming_event(self, limit: int = 1) -> List[Event]:
        return (self.db.query(self.model)
                .filter(self.model.start_time > datetime.now())
                .order_by(desc(self.model.start_time))
                .limit(limit)
                .all())

    def participate(self, event_id: int, member_id: int) -> Event:
        event = self.db.query(Event).get(event_id)
        member = self.db.query(Member).get(member_id)
        
        if event is None or member is None:
            raise ValueError("Event or Member not found")
            
        if member not in event.participants:
            event.participants.append(member)
            self.db.commit()
        else:
            raise ValueError("Member already participating in the event")
            
        return event

    def remove_participant(self, event_id: int, member_id: int) -> Event:
        event = self.db.query(Event).get(event_id)
        member = self.db.query(Member).get(member_id)
        
        if event is None or member is None:
            raise ValueError("Event or Member not found")
            
        if member in event.participants:
            event.participants.remove(member)
            self.db.commit()
        else:
            raise ValueError("Member not participating in the event")
            
        return event

    def get_upcoming_events(self, limit: int = 10) -> List[Event]:
        return (self.db.query(self.model)
                .filter(self.model.start_time > datetime.now())
                .order_by(self.model.start_time)
                .limit(limit)
                .all())

    def get_multi(self, skip: int = 0, limit: int = 10) -> List[Event]:
        return (self.db.query(self.model)
                .order_by(desc(self.model.start_time))
                .offset(skip)
                .limit(limit)
                .all())

def get_event_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDEvent:
    return CRUDEvent(db)
