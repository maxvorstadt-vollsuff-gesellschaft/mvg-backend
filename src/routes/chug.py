from fastapi import APIRouter, Depends

from .. import repositories
from .. import schemas
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
    for i in range(len(chugs.id)):
        repositories.chug_repository.create(db, {"member_id": chugs.id[i], "time": chugs.time[i]})


@router.get("/top-player")
def top_player(limit: int = 10, db=Depends(get_db)) -> list[schemas.BaseChug]:
    db_chugs = repositories.chug_repository.get_ordered_unique(db, limit)
    return [schemas.BaseChug.model_validate(chug) for chug in db_chugs]
