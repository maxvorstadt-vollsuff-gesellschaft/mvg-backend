from typing import Annotated

from fastapi import APIRouter, Depends

from .. import repositories
from .. import schemas
from ..auth_utils import get_current_user
from ..database import get_db

router = APIRouter(
    prefix="/chugs",
    tags=["chugging"]
)


@router.get("")
def events(skip: int = 0, limit: int = 100, db=Depends(get_db)) -> list[schemas.BaseChug]:
    db_chugs = repositories.chug_repository.get_multi(db, skip, limit)
    return [schemas.BaseChug.model_validate(chug) for chug in db_chugs]


@router.post("")
def create_event(
        chugs: schemas.UploadChug,
        db=Depends(get_db)
):
    pass