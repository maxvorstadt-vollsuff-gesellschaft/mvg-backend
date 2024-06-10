import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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
    "http://localhost:3000"
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


def get_next_quote(db: Session):
    print("getting quote")
    quote = repositories.quote_repository.get_random(db)
    if quote:
        rotation = models.QuoteRotation(quote=quote, chosen_at=datetime.datetime.now())
        repositories.rotation_repository.create(db, rotation)


@app.on_event("startup")
def schedule():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_next_quote, 'interval', days=1, args=[next(get_db())])
    scheduler.start()


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


@app.get("/quotes")
def get_quotes(limit: int = 10, skip: int = 0, db=Depends(get_db)):
    db_quotes = repositories.quote_repository.get_multi(db, limit=limit, skip=skip)
    return [schemas.Quote.from_orm(db_quote) for db_quote in db_quotes]
