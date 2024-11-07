from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from .. import models
from .. import repositories
from .. import schemas
from ..auth_utils import get_current_user, get_current_user_with_roles
from ..database import get_db

router = APIRouter(
    prefix="/recipes",
    tags=["recipes", "mvg"]
)

@router.post("", operation_id="create_recipe")
def create_recipe(
    recipe: schemas.RecipeCreate,
    current_user: Annotated[models.Member, Depends(get_current_user_with_roles(required_roles=["mvg-member"]))],
    db: Session = Depends(get_db)
):
    try:
        db_recipe = repositories.recipe_repository.save_recipe(
            db,
            recipe
        )
        return schemas.Recipe.from_orm(db_recipe)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/{recipe_id}", operation_id="get_recipe_by_id")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)) -> schemas.Recipe:
    db_recipe = repositories.recipe_repository.get(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return schemas.Recipe.from_orm(db_recipe)

@router.get("", operation_id="get_all_recipes")
def get_all_recipes(db: Session = Depends(get_db)) -> list[schemas.Recipe]:
    db_recipes = repositories.recipe_repository.get_multi(db)
    return [schemas.Recipe.from_orm(recipe) for recipe in db_recipes]

@router.delete("", operation_id="delete_recipe")
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