from collections import defaultdict

from fastapi import APIRouter, Depends, Query

from .. import repositories
from .. import schemas
from ..database import get_db

router = APIRouter(
    prefix="/members",
    tags=["members", "mvg"]
)


@router.get("", operation_id="list_members")
def members(db=Depends(get_db)) -> list[schemas.Member]:
    db_members = repositories.member_repository.get_multi(db)
    return [schemas.Member.model_validate(member) for member in db_members]


@router.get("/{member_id}/drinks", tags=["drinks"], operation_id="get_member_drinks")
def get_drinks_for_event(
        member_id: int,
        grouped: bool = Query(False, description="Group drinks consumed by event_id"),
        db=Depends(get_db)
) -> list[schemas.Drink] | dict[int, list[schemas.Drink]]:
    db_drinks = repositories.drink_repository.get_drinks_for(db, member_id)
    if grouped:
        d = defaultdict(list)
        for db_drink in db_drinks:
            d[db_drink.event_id].append(schemas.Drink.model_validate(db_drink))
            return d
    return [schemas.Drink.model_validate(db_drink) for db_drink in db_drinks]


