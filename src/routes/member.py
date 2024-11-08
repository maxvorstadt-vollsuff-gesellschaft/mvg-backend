from collections import defaultdict
from typing import Annotated, List, Dict, Union

from fastapi import APIRouter, Depends, Query

from ..repositories import get_member_repository, get_drink_repository, CRUDMember, CRUDDrink
from .. import schemas

router = APIRouter(
    prefix="/members",
    tags=["members", "mvg"]
)


@router.get("", operation_id="list_members")
def members(
    member_repository: Annotated[CRUDMember, Depends(get_member_repository)]
) -> List[schemas.Member]:
    db_members = member_repository.get_multi()
    return [schemas.Member.model_validate(member) for member in db_members]


@router.get("/{member_id}/drinks", tags=["drinks"], operation_id="get_member_drinks")
def get_drinks_for_event(
    drink_repository: Annotated[CRUDDrink, Depends(get_drink_repository)],
    member_id: int,
    grouped: bool = Query(False, description="Group drinks consumed by event_id"),
) -> Union[List[schemas.Drink], Dict[int, List[schemas.Drink]]]:
    db_drinks = drink_repository.get_drinks_for(member_id)
    if grouped:
        d = defaultdict(list)
        for db_drink in db_drinks:
            d[db_drink.event_id].append(schemas.Drink.model_validate(db_drink))
        return d
    return [schemas.Drink.model_validate(db_drink) for db_drink in db_drinks]


