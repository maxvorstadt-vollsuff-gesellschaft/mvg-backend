from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Drink


class CRUDDrink(CRUDBase[Drink]):
    def get_drinks_for(self, db: Session, member_id: int) -> list[Drink]:
        return db.query(self.model).filter(self.model.consumer_id == member_id).all()

    def get_drink_event(self, db: Session, event_id: int) -> list[Drink]:
        return db.query(self.model).filter(self.model.event_id == event_id)


drink_repository = CRUDDrink(Drink)
