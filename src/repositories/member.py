from typing import Optional

from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models import Member


class CRUDMember(CRUDBase[Member]):
    def get_sub(self, db: Session, sub: str) -> Optional[Member]:
        return db.query(self.model).filter(self.model.user_sub == sub).first()

member_repository = CRUDMember(Member)
