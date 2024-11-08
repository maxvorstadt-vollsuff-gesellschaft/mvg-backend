from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Card
from ..database import get_db


class CRUDCard(CRUDBase[Card]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(Card, db)

    def get_by_card_uid(self, uid: str) -> Optional[Card]:
        return self.db.query(self.model).filter(self.model.card_uid == uid).first()


def get_card_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDCard:
    return CRUDCard(db)
