from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..repositories import get_card_repository, CRUDCard
from ..schemas import Card, CreateCard

router = APIRouter(
    prefix="/card",
    tags=["card", "mvg"]
)


@router.get("", operation_id="get_all_cards")
def get_cards(
    card_repository: Annotated[CRUDCard, Depends(get_card_repository)]
) -> List[Card]:
    return card_repository.get_multi(skip=0, limit=100)


@router.post("", operation_id="create_new_card")
def create_card(
    card: CreateCard,
    card_repository: Annotated[CRUDCard, Depends(get_card_repository)]
) -> Card:
    return card_repository.create(card)


@router.delete("/{member_id}", operation_id="delete_card_by_member_id")
def delete_card(
    member_id: int,
    card_repository: Annotated[CRUDCard, Depends(get_card_repository)]
) -> Card:
    return card_repository.remove(member_id)
