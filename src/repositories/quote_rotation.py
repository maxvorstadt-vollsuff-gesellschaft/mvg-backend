from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import QuoteRotation
from ..database import get_db


class CRUDQuoteRotation(CRUDBase[QuoteRotation]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(QuoteRotation, db)


def get_quote_rotation_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDQuoteRotation:
    return CRUDQuoteRotation(db)
