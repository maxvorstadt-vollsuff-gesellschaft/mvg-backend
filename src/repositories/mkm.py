from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.mkm import MKM
from ..database import get_db


class MKMRepository(CRUDBase[MKM]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(MKM, db)


def get_mkm_repository(db: Annotated[Session, Depends(get_db)]) -> MKMRepository:
    return MKMRepository(db)
