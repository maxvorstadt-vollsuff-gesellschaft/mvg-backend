from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .base import CRUDBase
from ..models import DateIdea
from ..schemas import DateIdeaCreate
from ..database import get_db


class CRUDDateIdea(CRUDBase[DateIdea]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(DateIdea, db)

    def save_date_idea(self, date_idea: DateIdeaCreate) -> DateIdea:
        if not date_idea.name or not date_idea.season:
            raise ValueError("Date idea name and season are required")

        date_idea_db = DateIdea(
            name=date_idea.name,
            season=date_idea.season,
            time=date_idea.time,
            description=date_idea.description,
            author_id=date_idea.author_id,
            image_url=date_idea.image_url,
            date_no=date_idea.date_no
        )
        self.db.add(date_idea_db)
        self.db.commit()
        self.db.refresh(date_idea_db)
        return date_idea_db
    
    def delete_date_idea(self, date_idea_id: Optional[int] = None, date_idea_name: Optional[str] = None) -> None:
        if not date_idea_id and not date_idea_name:
            raise ValueError("Either date_idea_id or date_idea_name must be provided")

        query = self.db.query(self.model)
        if date_idea_id:
            query = query.filter(self.model.id == date_idea_id)
        elif date_idea_name:
            query = query.filter(self.model.name == date_idea_name)

        try:
            date_idea = query.one()
            self.db.delete(date_idea)
            self.db.commit()
        except NoResultFound:
            raise ValueError("Date idea not found")


def get_date_idea_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDDateIdea:
    return CRUDDateIdea(db)