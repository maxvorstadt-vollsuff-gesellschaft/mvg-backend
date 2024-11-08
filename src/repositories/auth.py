from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Auth
from ..database import get_db


class CRUDAuth(CRUDBase[Auth]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(Auth, db)

    def get_by_username(self, username: str) -> Auth | None:
        return self.db.query(Auth).filter(self.model.user_name == username).first()


def get_auth_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDAuth:
    return CRUDAuth(db)
