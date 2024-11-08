from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from .. import models, schemas
from ..auth_utils import get_current_user, get_current_user_with_roles
from ..repositories import get_recipe_repository
from ..repositories.recipe import CRUDRecipe

router = APIRouter(
    prefix="/recipes",
    tags=["recipes", "mvg"]
)

@router.post("", operation_id="create_recipe")
def create_recipe(
    recipe: schemas.RecipeCreate,
    current_user: Annotated[models.Member, Depends(get_current_user_with_roles(required_roles=["mvg-member"]))],
    recipe_repository: Annotated[CRUDRecipe, Depends(get_recipe_repository)]
) -> schemas.Recipe:
    try:
        recipe.author_id = current_user.id
        db_recipe = recipe_repository.save_recipe(recipe)
        return schemas.Recipe.model_validate(db_recipe)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/{recipe_id}", operation_id="get_recipe_by_id")
def get_recipe(
    recipe_id: int,
    recipe_repository: Annotated[CRUDRecipe, Depends(get_recipe_repository)]
) -> schemas.Recipe:
    db_recipe = recipe_repository.get(recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return schemas.Recipe.model_validate(db_recipe)

@router.get("", operation_id="get_all_recipes")
def get_all_recipes(
    recipe_repository: Annotated[CRUDRecipe, Depends(get_recipe_repository)]
) -> List[schemas.Recipe]:
    db_recipes = recipe_repository.get_multi()
    return [schemas.Recipe.model_validate(recipe) for recipe in db_recipes]

@router.delete("", operation_id="delete_recipe")
def delete_recipe(
    current_user: Annotated[models.Member, Depends(get_current_user)],
    recipe_repository: Annotated[CRUDRecipe, Depends(get_recipe_repository)],
    recipe_id: int = None,
    recipe_name: str = None
) -> dict:
    try:
        recipe_repository.delete_recipe(recipe_id=recipe_id, recipe_name=recipe_name)
        return {"detail": "Recipe deleted successfully"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))