from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Auth


class CRUDAuth(CRUDBase[Auth]):
    def get_by_username(self, db: Session, username: str) -> Auth | None:
        return db.query(Auth).filter(self.model.user_name == username).first()


auth_repository = CRUDAuth(Auth)
