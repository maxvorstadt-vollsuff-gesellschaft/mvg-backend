from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Quote
from ..database import get_db


class CRUDQuote(CRUDBase[Quote]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(Quote, db)

    def get_random(self) -> Optional[Quote]:
        return self.db.query(self.model).order_by(func.random()).first()


def get_quote_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDQuote:
    return CRUDQuote(db)
