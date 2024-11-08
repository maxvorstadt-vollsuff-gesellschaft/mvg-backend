import datetime
from typing import Annotated, Tuple

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi_keycloak import OIDCUser

from .services.event import EventService, get_event_service

from . import routes
from .auth_utils import get_current_user
from . import models
from . import schemas
from . import repositories
from . import database
from .database import engine, get_db

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

origins = [
    "https://mvg.life",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://nfconnect.pages.dev",
    "https://register.mvg.life"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.auth.router)
app.include_router(routes.events.router)
app.include_router(routes.member.router)
app.include_router(routes.quotes.router)
app.include_router(routes.chug.router)
app.include_router(routes.card.router)
app.include_router(routes.recipes.router)


@app.on_event("startup")
async def startup() -> None:
    await database.database.connect()


def get_next_quote(db: Session):
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


@app.post("/auth/hash", operation_id="hash_password", tags=["auth", "mvg"])
def set_password(pw: str):
    return pwd_context.hash(pw)


@app.post("/drinks", operation_id="create_drink", tags=["drinks", "mvg"])
async def post_drink(
        drink: schemas.DrinkCreate,
        _user: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
        db=Depends(get_db)
) -> schemas.Drink:
    drink = repositories.drink_repository.create(db, drink)
    return drink
