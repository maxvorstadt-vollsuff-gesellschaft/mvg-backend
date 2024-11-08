from typing import Annotated, List
from fastapi import APIRouter, Depends

from ..repositories import get_chug_repository, get_card_repository
from ..repositories.chug import CRUDChug
from ..repositories.card import CRUDCard
from .. import schemas

router = APIRouter(
    prefix="/chugs",
    tags=["chugging", "mvg"]
)


@router.get("", operation_id="list_chugs")
def events(
    chug_repository: Annotated[CRUDChug, Depends(get_chug_repository)],
    skip: int = 0,
    limit: int = 100
) -> List[schemas.BaseChug]:
    db_chugs = chug_repository.get_multi(skip=skip, limit=limit)
    return [schemas.BaseChug.model_validate(chug) for chug in db_chugs]


@router.post("", operation_id="create_chugs")
def create_event(
    chugs: schemas.UploadChug,
    chug_repository: Annotated[CRUDChug, Depends(get_chug_repository)],
    card_repository: Annotated[CRUDCard, Depends(get_card_repository)]
):
    for i in range(len(chugs.id)):
        card = card_repository.get_by_card_uid(chugs.id[i])
        if not card:
            continue
        chug_repository.create({
            "member_id": card.member_id, 
            "time": chugs.time[i]
        })


@router.get("/top-player", operation_id="get_top_chuggers")
def top_player(
    chug_repository: Annotated[CRUDChug, Depends(get_chug_repository)],
    limit: int = 10,
) -> List[schemas.BaseChug]:
    db_chugs = chug_repository.get_ordered_unique(limit=limit)
    return [schemas.BaseChug.model_validate(chug) for chug in db_chugs]
