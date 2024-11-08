from typing import Annotated, List
from fastapi import Depends
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Drink
from ..database import get_db


class CRUDDrink(CRUDBase[Drink]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(Drink, db)

    def get_drinks_for(self, member_id: int) -> List[Drink]:
        return (self.db.query(self.model)
                .filter(self.model.consumer_id == member_id)
                .all())

    def get_drink_event(self, event_id: int) -> List[Drink]:
        return (self.db.query(self.model)
                .filter(self.model.event_id == event_id)
                .all())


def get_drink_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDDrink:
    return CRUDDrink(db)
