from typing import Type, TypeVar, Generic, Annotated, List
from fastapi import Depends
from sqlalchemy.orm import Session
from ..models.base import Base
from ..database import get_db

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        db: Annotated[Session, Depends(get_db)]
    ):
        self.model = model
        self.db = db

    def get(self, id: int) -> ModelType | None:
        return self.db.query(self.model).filter(self.model.id == id).first()


    def get_tkt_top_players(self, skip: int = 0, limit: int = 10) -> List[ModelType]:
        return self.db.query(self.model).order_by(self.model.tkt_elo_rating.desc()).offset(skip).limit(limit).all()

    def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in) -> ModelType:
        db_obj = obj_in
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        elif not isinstance(obj_in, self.model):
            db_obj = self.model(**obj_in.__dict__)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def create_batch(self, obj_in_list: List[ModelType]) -> None:
        self.db.bulk_save_objects([self.model(**obj_in.dict()) for obj_in in obj_in_list])
        self.db.commit()

    def update(self, db_obj: ModelType, obj_in) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, id: int) -> ModelType:
        obj = self.db.query(self.model).get(id)
        if obj is None:
            raise ValueError("Object not found")
        self.db.delete(obj)
        self.db.commit()
        return obj
