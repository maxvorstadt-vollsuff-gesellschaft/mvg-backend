from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..repositories import card_repository
from ..schemas import CreateCard


router = APIRouter(
    prefix="/card",
    tags=["card"]
)


@router.get("")
def get_cards(db: Session = Depends(get_db)):
    return card_repository.get_multi(db, skip=0, limit=100)


@router.post("")
def create_card(card: CreateCard, db: Session = Depends(get_db)):
    return card_repository.create(db, card)
