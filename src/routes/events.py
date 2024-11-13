from collections import defaultdict
from datetime import timedelta
import json
from typing import Annotated, Tuple
import uuid

from fastapi import APIRouter, Depends, HTTPException, Response
from icalendar import Calendar, Event as ICalEvent
from fastapi_keycloak import OIDCUser

from .. import models, schemas
from ..auth_utils import get_current_user, idp
from ..services.event import EventService, get_event_service
from ..repositories import get_calendar_link_repository, CRUDCalendarLink, CRUDDrink, get_drink_repository
from ..database import get_db

router = APIRouter(
    prefix="/events",
    tags=["events", "mvg"]
)

@router.get("", operation_id="list_events")
def events(
    event_service: Annotated[EventService, Depends(get_event_service)],
    user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[schemas.Event]:
    oidc_user, _ = user_info
    db_events = event_service.get_events(oidc_user, skip=skip, limit=limit)
    return [schemas.Event.model_validate(event) for event in db_events]

@router.get("/past", operation_id="list_past_events")
def past_events(
    event_service: Annotated[EventService, Depends(get_event_service)],
    user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
) -> list[schemas.Event]:
    oidc_user, _ = user_info
    db_events = event_service.get_past_events(oidc_user, skip=skip, limit=limit)
    return [schemas.Event.model_validate(event) for event in db_events]

@router.get("/upcoming", operation_id="list_upcoming_events")
def upcoming_events(
    event_service: Annotated[EventService, Depends(get_event_service)],
    user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    limit: int = 100
) -> list[schemas.Event]:
    oidc_user, _ = user_info
    db_events = event_service.get_upcoming_events(oidc_user, limit=limit)
    return [schemas.Event.model_validate(event) for event in db_events]

@router.post("", operation_id="create_event")
def create_event(
    event: schemas.EventCreate,
    user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    event_service: Annotated[EventService, Depends(get_event_service)]
) -> schemas.Event:
    oidc_user, _ = user_info
    db_event = event_service.create_event(event, oidc_user)
    return schemas.Event.model_validate(db_event)

@router.get("/event/{id}", operation_id="get_event_by_id")
def get_event(
    id: int,
    event_service: Annotated[EventService, Depends(get_event_service)]
) -> schemas.Event:
    db_event = event_service.get_event(id)
    return schemas.Event.model_validate(db_event)

@router.delete("/event/{id}", operation_id="delete_event_by_id")
def delete_event(
    id: int,
    user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    event_service: Annotated[EventService, Depends(get_event_service)]
) -> schemas.Event:
    oidc_user, _ = user_info
    db_event = event_service.delete_event(id, oidc_user)
    return schemas.Event.model_validate(db_event)

@router.post("/{event_id}/participate", operation_id="add_event_participant")
def participate(
    event_id: int,
    user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    event_service: Annotated[EventService, Depends(get_event_service)]
) -> schemas.Event:
    oidc_user, _ = user_info
    db_event = event_service.participate_in_event(event_id, oidc_user)
    return schemas.Event.from_orm(db_event)

@router.delete("/{event_id}/participate", operation_id="remove_event_participant")
def remove_participant(
    event_id: int,
    user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    event_service: Annotated[EventService, Depends(get_event_service)]
) -> schemas.Event:
    oidc_user, _ = user_info
    db_event = event_service.remove_participant(event_id, oidc_user)
    return schemas.Event.from_orm(db_event)

def _build_calendar_url(tag: str) -> str:
    return f"https://api.mvg.life/events/calendar/{tag}"

@router.post("/calendar", operation_id="create_calendar_link", description="Create a calendar link for the user. If the user already has a link, the existing link is returned.")
def create_calendar_link(
    user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    calendar_link_repository: Annotated[CRUDCalendarLink, Depends(get_calendar_link_repository)],
    force: bool = False
) -> str:
    oidc_user, _ = user_info
    
    if not force:
        if existing_link := calendar_link_repository.get_by_member_sub(oidc_user.sub):
            return _build_calendar_url(existing_link.tag)
    
    new_tag = uuid.uuid4()
    calendar_link = models.CalendarLink(member_sub=oidc_user.sub, tag=new_tag)
    db_cal_link = calendar_link_repository.create(calendar_link)
    
    return _build_calendar_url(db_cal_link.tag)

@router.get("/calendar/{tag}", operation_id="get_calendar_events", response_class=Response)
def get_calendar_events(
    tag: str,
    event_service: Annotated[EventService, Depends(get_event_service)],
    calendar_link_repository: Annotated[CRUDCalendarLink, Depends(get_calendar_link_repository)]
) -> Response:
    db_calendar_link = calendar_link_repository.get_by_tag(tag)
    if not db_calendar_link:
        raise HTTPException(status_code=404, detail="Calendar link not found")
    roles = idp.get_user_roles(db_calendar_link.member_sub)
    roles = [role.name for role in roles]
    db_events = event_service.get_accessible_events_by_role(roles, skip=0, limit=100)
    
    cal = Calendar()
    cal.add('prodid', '-//MVG Calendar//mvg.life//')
    cal.add('version', '2.0')
    cal.add('method', 'PUBLISH')

    for event in db_events:
        event_component = ICalEvent()
        event_component.add('summary', event.name)
        event_component.add('dtstart', event.start_time)
        event_component.add('dtend', event.start_time + timedelta(minutes=event.duration if event.duration else 60))
        event_component.add('location', event.location)
        event_component.add('description', f"created by {event.author.name}")
        
        for participant in event.participants:
            event_component.add('attendee', f'mailto:{participant.name}',
                              parameters={
                                  'PARTSTAT': 'ACCEPTED',
                                  'CN': participant.name,
                                  'ROLE': 'REQ-PARTICIPANT'
                              })
            
        cal.add_component(event_component)
    
    return Response(
        content=cal.to_ical(),
        media_type="text/calendar",
        headers={
            "Content-Disposition": "attachment; filename=calendar.ics"
        }
    )

# Note: This endpoint might be better moved to a drink service/routes
@router.get("/{event_id}/drinks", operation_id="list_event_drinks")
def get_drinks_for_event(
    event_id: int,
    drink_repository: Annotated[CRUDDrink, Depends(get_drink_repository)],
    grouped: bool = False,
) -> list[schemas.Drink] | dict[int, list[schemas.Drink]]:
    db_drinks = drink_repository.get_drink_event(event_id)
    if grouped:
        d = defaultdict(list)
        for drink in db_drinks:
            d[drink.consumer_id].append(schemas.Drink.model_validate(drink))
        return d
    return [schemas.Drink.model_validate(db_drink) for db_drink in db_drinks]
