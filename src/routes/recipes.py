from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from .. import models
from .. import repositories
from .. import schemas
from ..auth_utils import get_current_user
from ..database import get_db

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)

@router.post("")
def create_recipe(
    recipe: schemas.RecipeCreate,
    _current_user: Annotated[models.Member, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    try:
        db_recipe = repositories.recipe_repository.save_recipe(
            db,
            recipe_name=recipe.name,
            time_of_day=recipe.time_of_day,
            complexity=recipe.complexity,
            description=recipe.description
        )
        return schemas.Recipe.from_orm(db_recipe)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)) -> schemas.Recipe:
    db_recipe = repositories.recipe_repository.get(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return schemas.Recipe.from_orm(db_recipe)

@router.get("/all")
def get_all_recipes(db: Session = Depends(get_db)) -> list[schemas.Recipe]:
    db_recipes = repositories.recipe_repository.get_all(db)
    return [schemas.Recipe.from_orm(recipe) for recipe in db_recipes]

@router.delete("")
def delete_recipe(
    _current_user: Annotated[models.Member, Depends(get_current_user)],
    db: Session = Depends(get_db),
    recipe_id: int = None,
    recipe_name: str = None
):
    try:
        repositories.recipe_repository.delete_recipe(db, recipe_id=recipe_id, recipe_name=recipe_name)
        return {"detail": "Recipe deleted successfully"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))