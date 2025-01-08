from typing import Annotated, List, Optional, Tuple

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi_keycloak import OIDCUser

from .. import models, schemas
from ..auth_utils import get_current_user, get_current_user_with_roles
from ..repositories import get_date_idea_repository
from ..repositories.dates import CRUDDateIdea
from ..minio_client import upload_recipe_image as upload_image

router = APIRouter(
    prefix="/dates",
    tags=["dates", "mvg"]
)

@router.post("", operation_id="create_date_idea")
def create_date_idea(
    name: str,
    season: models.Jahreszeit,
    description: str,
    date_no: int,
    _user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user_with_roles(required_roles=["mvg-member"]))],
    date_idea_repository: Annotated[CRUDDateIdea, Depends(get_date_idea_repository)],
    image: Optional[UploadFile] = File(None),
) -> schemas.DateIdea:
    _, member = _user_info
    image_url = None
    date_idea = schemas.DateIdeaCreate(
        name=name,
        season=season,
        description=description,
        date_no=date_no,
        author_id=member.user_sub,
        image_url=image_url
    )

    if image:
        image_url = upload_image(image.file.read(), image.filename)

    try:
        date_idea.image_url = image_url
        
        db_date_idea = date_idea_repository.save_date_idea(date_idea)
        return schemas.DateIdea.model_validate(db_date_idea)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/{date_idea_id}", operation_id="get_date_idea_by_id")
def get_date_idea(
    date_idea_id: int,
    date_idea_repository: Annotated[CRUDDateIdea, Depends(get_date_idea_repository)]
) -> schemas.DateIdea:
    db_date_idea = date_idea_repository.get(date_idea_id)
    if not db_date_idea:
        raise HTTPException(status_code=404, detail="Date idea not found")
    return schemas.DateIdea.model_validate(db_date_idea)
        
@router.get("", operation_id="get_all_date_ideas")
def get_all_date_ideas(
    date_idea_repository: Annotated[CRUDDateIdea, Depends(get_date_idea_repository)]
) -> List[schemas.DateIdea]:
    db_date_ideas = date_idea_repository.get_multi()
    return [schemas.DateIdea.model_validate(date_idea) for date_idea in db_date_ideas]

@router.delete("", operation_id="delete_date_idea")
def delete_date_idea(
    _user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    date_idea_repository: Annotated[CRUDDateIdea, Depends(get_date_idea_repository)],
    date_idea_id: int = None,
    date_idea_name: str = None
) -> dict:
    try:
        oidc_user, member = _user_info
        date_idea_repository.delete_date_idea(date_idea_id=date_idea_id, date_idea_name=date_idea_name)
        return {"detail": "Date idea deleted successfully"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))
    

@router.post("/image", operation_id="upload_date_idea_image")
def upload_date_idea_image(
    image: UploadFile
) -> str:
    content = image.file.read()
    url = upload_image(content, image.filename)
    return url
