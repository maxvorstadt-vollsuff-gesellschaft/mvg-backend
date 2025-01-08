from datetime import datetime
from typing import Optional, List

from fastapi import UploadFile
from pydantic import BaseModel, Field
from .member import Member  
from ..models.dates import Jahreszeit

class DateIdeaBase(BaseModel):
    name: str
    description: Optional[str] = Field(None, description="A brief description of the recipe.")
    time: Optional[int]
    season: Jahreszeit
    image_url: Optional[str]
    date_no: int

class DateIdeaCreate(DateIdeaBase):
    author_id: str

class DateIdeaUpdate(DateIdeaBase):
    pass

class DateIdea(DateIdeaBase):
    id: int
    author: Optional[Member]
    class Config:
        from_attributes = True