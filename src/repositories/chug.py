from typing import Annotated, List
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Chug
from ..database import get_db


class CRUDChug(CRUDBase[Chug]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(Chug, db)

    def get_ordered(self, limit: int = 10) -> List[Chug]:
        return (self.db.query(self.model)
                .order_by(Chug.time.asc())
                .limit(limit)
                .all())

    def get_ordered_unique(self, limit: int = 10) -> List[Chug]:
        subquery = (self.db.query(
            Chug.member_id,
            func.min(Chug.time).label('min_time')
        )
        .group_by(Chug.member_id)
        .subquery())

        result = (self.db.query(Chug)
                 .join(
                     subquery,
                     (Chug.member_id == subquery.c.member_id) & 
                     (Chug.time == subquery.c.min_time)
                 )
                 .order_by(Chug.time.asc())
                 .limit(limit)
                 .all())
    
        return result


def get_chug_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDChug:
    return CRUDChug(db)
