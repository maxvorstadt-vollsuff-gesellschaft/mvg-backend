from sqlalchemy import func

from .base import CRUDBase
from ..models import Chug


class CRUDChug(CRUDBase[Chug]):
    def get_ordered(self, db, limit=10):
        return db.query(self.model).order_by(Chug.time.asc()).limit(limit).all()

    def get_ordered_unique(self, db, limit=10):
        subquery = db.query(
            Chug.member_id,
            func.min(Chug.time).label('min_time')
        ).group_by(Chug.member_id).subquery()

        result = db.query(Chug).join(
            subquery,
            (Chug.member_id == subquery.c.member_id) & (Chug.time == subquery.c.min_time)
        ).order_by(Chug.time.asc()).limit(limit).all()
    
        return result

chug_repository = CRUDChug(Chug)
