from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Member
from ..database import get_db


class CRUDMember(CRUDBase[Member]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(Member, db)

    def get_sub(self, sub: str) -> Optional[Member]:
        return self.db.query(self.model).filter(self.model.user_sub == sub).first()


def get_member_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDMember:
    return CRUDMember(db)
