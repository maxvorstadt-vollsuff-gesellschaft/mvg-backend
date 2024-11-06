from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from .member import Member  
from ..models.recipe import TimeOfDay, ComplexityLevel

class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = Field(None, description="A brief description of the recipe.")
    time_of_day: TimeOfDay
    complexity: Optional[ComplexityLevel]

class RecipeCreate(RecipeBase):
    author_id: Optional[int]

class RecipeUpdate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    author: Optional[Member]

    class Config:
        from_attributes = True