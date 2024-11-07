from collections import defaultdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from .. import models
from .. import repositories
from .. import schemas
from ..auth_utils import get_current_user
from ..database import get_db

router = APIRouter(
    prefix="/events",
    tags=["events", "mvg"]
)


@router.get("", operation_id="list_events")
def events(skip: int = 0, limit: int = 100, db=Depends(get_db)) -> list[schemas.Event]:
    db_events = repositories.event_repository.get_multi(db, skip=skip, limit=limit)
    return [schemas.Event.model_validate(event) for event in db_events]


@router.post("", operation_id="create_event")
def create_event(
        event: schemas.EventCreate,
        _current_user: Annotated[models.Member, Depends(get_current_user)],
        db=Depends(get_db)
):
    db_event = repositories.event_repository.create(db, event)
    return schemas.Event.model_validate(db_event)


@router.get("/event/{id}", operation_id="get_event_by_id")
def get_event(id: int, db=Depends(get_db)) -> schemas.Event:
    db_event = repositories.event_repository.get(db, id)
    if not db_event:
        raise HTTPException(status_code=404)
    return schemas.Event.model_validate(db_event)


@router.delete("/event/{id}", operation_id="delete_event_by_id")
def delete_event(
        id: int,
        _current_user: Annotated[models.Member, Depends(get_current_user)],
        db=Depends(get_db),
) -> schemas.Event:
    try:
        db_event = repositories.event_repository.remove(db, id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Event does not exist")
    return schemas.Event.model_validate(db_event)


@router.post("/{event_id}/participate", operation_id="add_event_participant")
def participate(
        event_id: int,
        member: int,
        current_user: Annotated[models.Member, Depends(get_current_user)],
        db=Depends(get_db)
) -> schemas.Event:
    if current_user.id != member:
        raise HTTPException(status_code=403, detail="You can only sign up yourself!")
    try:
        db_event = repositories.event_repository.participate(db, event_id, member)
        return schemas.Event.from_orm(db_event)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.delete("/{event_id}/participate", operation_id="remove_event_participant")
def remove_participant(
        event_id: int,
        member: int,
        current_user: Annotated[models.Member, Depends(get_current_user)],
        db=Depends(get_db)
) -> schemas.Event:
    if current_user.id != member:
        raise HTTPException(status_code=403, detail="You can only remove your participation")
    try:
        db_event = repositories.event_repository.remove_participant(db, event_id, member)
        return schemas.Event.from_orm(db_event)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get("/{event_id}/drinks", operation_id="list_event_drinks")
def get_drinks_for_event(
        event_id: int,
        grouped: bool = False,
        db=Depends(get_db)
) -> list[schemas.Drink] | dict[int, list[schemas.Drink]]:
    db_drinks = repositories.drink_repository.get_drink_event(db, event_id)
    if grouped:
        d = defaultdict(list)
        for drink in db_drinks:
            d[drink.consumer_id].append(schemas.Drink.model_validate(drink))
        return d
    return [schemas.Drink.model_validate(db_drink) for db_drink in db_drinks]


@router.get("/upcoming", operation_id="list_upcoming_events")
def events(limit: int = 10, db=Depends(get_db)) -> list[schemas.Event]:
    db_events = repositories.event_repository.get_upcoming_events(db, limit=limit)
    return [schemas.Event.from_orm(event) for event in db_events]


