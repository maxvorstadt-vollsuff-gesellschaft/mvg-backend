from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from .member import Member  # Assuming you have a Member model similar to the Event schema

class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = Field(None, description="A brief description of the recipe.")
    ingredients: List[str] = Field(..., description="List of ingredients required for the recipe.")
    instructions: str = Field(..., description="Step-by-step instructions for the recipe.")
    prep_time: Optional[int] = Field(None, description="Preparation time in minutes.")
    cook_time: Optional[int] = Field(None, description="Cooking time in minutes.")

class RecipeCreate(RecipeBase):
    author_id: Optional[int]

class RecipeUpdate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author: Optional[Member]

    class Config:
        orm_mode = True