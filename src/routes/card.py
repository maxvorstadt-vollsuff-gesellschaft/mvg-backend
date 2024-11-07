from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..repositories import card_repository
from ..schemas import CreateCard


router = APIRouter(
    prefix="/card",
    tags=["card", "mvg"]
)


@router.get("", operation_id="get_all_cards")
def get_cards(db: Session = Depends(get_db)):
    return card_repository.get_multi(db, skip=0, limit=100)


@router.post("", operation_id="create_new_card")
def create_card(card: CreateCard, db: Session = Depends(get_db)):
    return card_repository.create(db, card)

@router.delete("/{member_id}", operation_id="delete_card_by_member_id")
def delete_card(member_id: int, db: Session = Depends(get_db)):
    return card_repository.remove(db, member_id)
