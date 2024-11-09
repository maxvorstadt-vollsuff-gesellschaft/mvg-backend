from datetime import datetime
from typing import Optional, List

from fastapi import UploadFile
from pydantic import BaseModel, Field
from .member import Member  
from ..models.recipe import Situation

class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = Field(None, description="A brief description of the recipe.")
    time: Optional[int]
    situation: Situation
    image_url: Optional[str]

class RecipeCreate(RecipeBase):
    author_id: str

class RecipeUpdate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    author: Optional[Member]
    class Config:
        from_attributes = True