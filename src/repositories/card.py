from typing import Optional

from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Card


class CRUDCard(CRUDBase[Card]):
    def get_by_card_uid(self, db: Session, uid: str) -> Optional[Card]:
        return db.query(self.model).filter(self.model.card_uid == uid).first()

card_repository = CRUDCard(Card)
