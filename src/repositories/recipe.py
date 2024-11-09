from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .base import CRUDBase
from ..models import Recipe
from ..schemas import RecipeCreate
from ..database import get_db


class CRUDRecipe(CRUDBase[Recipe]):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        super().__init__(Recipe, db)

    def save_recipe(self, recipe: RecipeCreate) -> Recipe:
        if not recipe.name or not recipe.situation:
            raise ValueError("Recipe name and situation are required")

        recipe_db = Recipe(
            name=recipe.name,
            situation=recipe.situation,
            time=recipe.time,
            description=recipe.description,
            author_id=recipe.author_id,
            image_url=recipe.image_url
        )
        self.db.add(recipe_db)
        self.db.commit()
        self.db.refresh(recipe_db)
        return recipe_db
    
    def delete_recipe(self, recipe_id: Optional[int] = None, recipe_name: Optional[str] = None) -> None:
        if not recipe_id and not recipe_name:
            raise ValueError("Either recipe_id or recipe_name must be provided")

        query = self.db.query(self.model)
        if recipe_id:
            query = query.filter(self.model.id == recipe_id)
        elif recipe_name:
            query = query.filter(self.model.name == recipe_name)

        try:
            recipe = query.one()
            self.db.delete(recipe)
            self.db.commit()
        except NoResultFound:
            raise ValueError("Recipe not found")


def get_recipe_repository(db: Annotated[Session, Depends(get_db)]) -> CRUDRecipe:
    return CRUDRecipe(db)
