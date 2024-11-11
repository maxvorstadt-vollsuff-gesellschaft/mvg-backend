from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import CalendarLink
from ..database import get_db


class CRUDCalendarLink(CRUDBase[CalendarLink]):
    def get_by_tag(self, tag: str) -> Optional[CalendarLink]:
        return self.db.query(self.model).filter(self.model.tag == tag).first()
    
    def get_by_member_sub(self, member_sub: str) -> Optional[CalendarLink]:
        return self.db.query(self.model).filter(self.model.member_sub == member_sub).first()


def get_calendar_link_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDCalendarLink:
    return CRUDCalendarLink(CalendarLink, db)
