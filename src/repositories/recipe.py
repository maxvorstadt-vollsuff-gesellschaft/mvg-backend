from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from ..models import Recipe
from ..schemas import RecipeCreate
from .base import CRUDBase

class CRUDRecipe(CRUDBase[Recipe]):
    def save_recipe(self, db: Session, recipe: RecipeCreate) -> Recipe:
        if not recipe.name or not recipe.time_of_day:
            raise ValueError("Recipe name and time of day are required")

        valid_times = {"breakfast", "lunch", "dinner"}
        if not set(recipe.time_of_day.split(",")).issubset(valid_times):
            raise ValueError("Invalid time of day. Must be 'breakfast', 'lunch', or 'dinner'")

        valid_complexities = {"5-15", "15-35", "40+"}
        if recipe.complexity and recipe.complexity not in valid_complexities:
            raise ValueError("Invalid complexity. Must be '5-15', '15-35', or '40+'")

        recipe = Recipe(
            name=recipe.name,
            time_of_day=recipe.time_of_day,
            complexity=recipe.complexity,
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
