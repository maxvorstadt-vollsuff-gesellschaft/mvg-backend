from typing import Annotated, List, Optional, Tuple

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi_keycloak import OIDCUser

from .. import models, schemas
from ..auth_utils import get_current_user, get_current_user_with_roles
from ..repositories import get_recipe_repository
from ..repositories.recipe import CRUDRecipe
from ..minio_client import upload_recipe_image as upload_image

router = APIRouter(
    prefix="/recipes",
    tags=["recipes", "mvg"]
)

@router.post("", operation_id="create_recipe")
def create_recipe(
    name: str,
    situation: models.Situation,
    description: str,
    time: int,
    _user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user_with_roles(required_roles=["mvg-member"]))],
    recipe_repository: Annotated[CRUDRecipe, Depends(get_recipe_repository)],
    image: Optional[UploadFile] = File(None),
) -> schemas.Recipe:
    _, member = _user_info
    image_url = None
    recipe = schemas.RecipeCreate(
        name=name,
        situation=situation,
        description=description,
        time=time,
        author_id=member.user_sub,
        image_url=image_url
    )

    if image:
        image_url = upload_image(image.file.read(), image.filename)

    try:
        recipe.image_url = image_url
        
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
    _user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    recipe_repository: Annotated[CRUDRecipe, Depends(get_recipe_repository)],
    recipe_id: int = None,
    recipe_name: str = None
) -> dict:
    try:
        oidc_user, member = _user_info
        recipe_repository.delete_recipe(recipe_id=recipe_id, recipe_name=recipe_name)
        return {"detail": "Recipe deleted successfully"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))
    

@router.post("/image", operation_id="upload_recipe_image")
def upload_recipe_image(
    image: UploadFile
) -> str:
    content = image.file.read()
    url = upload_image(content, image.filename)
    return {"url": url}