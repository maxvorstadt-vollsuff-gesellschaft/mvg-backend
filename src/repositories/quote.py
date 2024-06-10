from sqlalchemy import func
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Quote


class QuoteRepository(CRUDBase[Quote]):
    @staticmethod
    def get_random(db: Session):
        return db.query(Quote).order_by(func.random()).first()


quote_repository = QuoteRepository(Quote)
