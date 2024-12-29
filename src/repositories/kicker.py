from typing import Annotated, List
from fastapi import Depends
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.kicker_match import KickerMatch
from ..database import get_db


class CRUDKickerMatch(CRUDBase[KickerMatch]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(KickerMatch, db)

    def get_multi(self, skip: int = 0, limit: int = 10) -> List[KickerMatch]:
        return self.db.query(KickerMatch).order_by(KickerMatch.start_time.desc()).offset(skip).limit(limit).all()


def get_kicker_match_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDKickerMatch:
    return CRUDKickerMatch(db)
