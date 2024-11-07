from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from ..models import Recipe
from ..schemas import RecipeCreate
from .base import CRUDBase

class CRUDRecipe(CRUDBase[Recipe]):
    def save_recipe(self, db: Session, recipe: RecipeCreate) -> Recipe:
        if not recipe.name or not recipe.situation:
            raise ValueError("Recipe name and situation are required")

        recipe = Recipe(
            name=recipe.name,
            situation=recipe.situation,
            time=recipe.time,
            description=recipe.description,
            author_id=recipe.author_id
        )
        db.add(recipe)
        db.commit()
        db.refresh(recipe)
        return recipe
    
    def delete_recipe(self, db: Session, recipe_id: int = None, recipe_name: str = None) -> None:
        if not recipe_id and not recipe_name:
            raise ValueError("Either recipe_id or recipe_name must be provided")

        query = db.query(self.model)
        if recipe_id:
            query = query.filter(self.model.id == recipe_id)
        elif recipe_name:
            query = query.filter(self.model.name == recipe_name)

        try:
            recipe = query.one()
            db.delete(recipe)
            db.commit()
        except NoResultFound:
            raise ValueError("Recipe not found")

recipe_repository = CRUDRecipe(Recipe)
