from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session
from ..models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> ModelType:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in) -> ModelType:
        db_obj = obj_in
        if type(obj_in) is dict:
            db_obj = self.model(**obj_in)
        elif type(obj_in) is not self.model:
            db_obj = self.model(**obj_in.__dict__)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_batch(self, db, obj_in_list):
        db.bulk_save_objects([self.model(**obj_in.dict()) for obj_in in obj_in_list])
        db.commit()

    @staticmethod
    def update(db: Session, db_obj: ModelType, obj_in) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_db_model(db: Session, db_obj: ModelType):
        db.commit()

    def remove(self, db: Session, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        if obj is None:
            raise ValueError("Object not found")
        db.delete(obj)
        db.commit()
        return obj
