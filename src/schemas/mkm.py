from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator
from .recipe import Recipe
from .event import Event, EventCreate


class MKMBase(BaseModel):
    title: str
    description: str
    theme: Optional[str] = None
    image_url: Optional[str] = None
    recipe_id: Optional[int] = None


class MKMCreate(MKMBase):
    """
    Either event_id or event_create must be provided.
    """
    event_id: Optional[int] = None
    event_create: Optional[EventCreate] = None

    @model_validator(mode='after')
    def validate_event_fields(self) -> 'MKMCreate':
        event_id = self.event_id
        event_create = self.event_create
        
        if event_id is None and event_create is None:
            raise ValueError("Either event_id or event_create must be provided")
            
        if event_id is not None and event_create is not None:
            raise ValueError("Only one of event_id or event_create can be provided")
            
        return self

class MKMUpdate(MKMBase):
    title: Optional[str] = None
    description: Optional[str] = None
    event_id: Optional[int] = None


class MKM(MKMBase):
    id: int
    created_at: datetime
    updated_at: datetime
    recipe: Optional[Recipe] = None
    event: Event

    class Config:
        from_attributes = True
