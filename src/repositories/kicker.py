from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.kicker_match import KickerMatch
from ..database import get_db


class KickerMatchRepository(CRUDBase[KickerMatch]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(KickerMatch, db)


def get_kicker_match_repository(db: Annotated[Session, Depends(get_db)]) -> KickerMatchRepository:
    return KickerMatchRepository(db)
