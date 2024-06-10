from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from . import models
from . import schemas
from . import repositories
from . import database
from .database import engine, get_db

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = [
    "https://mvg.life",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    await database.database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.database.disconnect()


@app.get("/members")
def members(db=Depends(get_db)) -> list[schemas.Member]:
    db_members = repositories.member_repository.get_multi(db)
    return [schemas.Member.from_orm(member) for member in db_members]


@app.get("/events")
def events(skip: int = 0, limit: int = 10, db=Depends(get_db)) -> list[schemas.Event]:
    db_events = repositories.event_repository.get_multi(db, skip=skip, limit=limit)
    return [schemas.Event.from_orm(event) for event in db_events]


@app.post("/events")
def create_event(event: schemas.EventCreate, db=Depends(get_db)):
    db_event = repositories.event_repository.create(db, event)
    return schemas.Event.from_orm(db_event)


@app.get("/events/{id}")
def get_event(id: int, db=Depends(get_db)) -> schemas.Event:
    db_event = repositories.event_repository.get(db, id)
    if not db_event:
        raise HTTPException(status_code=404)
    return schemas.Event.from_orm(db_event)


@app.get("/upcoming_events")
def get_next_event(limit: int = 1, db=Depends(get_db)) -> list[schemas.Event]:
    db_events = repositories.event_repository.get_next_upcoming_event(db, limit=limit)
    if len(db_events) == 0:
        raise HTTPException(status_code=400, detail="No upcoming events found")
    return [schemas.Event.from_orm(event) for event in db_events]


@app.post("/events/{event_id}/participate")
def participate(event_id: int, member: int, db=Depends(get_db)) -> schemas.Event:
    try:
        db_event = repositories.event_repository.participate(db, event_id, member)
        return schemas.Event.from_orm(db_event)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@app.delete("/events/{event_id}/participate")
def remove_participant(event_id: int, member: int, db=Depends(get_db)) -> schemas.Event:
    try:
        db_event = repositories.event_repository.remove_participant(db, event_id, member)
        return schemas.Event.from_orm(db_event)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
