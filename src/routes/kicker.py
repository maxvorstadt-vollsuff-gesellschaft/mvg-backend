from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..repositories import get_kicker_match_repository, CRUDKickerMatch, get_member_repository, CRUDMember
from ..kicker_elo import job_queue as kicker_elo_queue

router = APIRouter(
    prefix="/goal_tracker",
    tags=["kicker", "mvg"]
)

@router.post("/matches", response_model=str, operation_id="create_match")
def create_match(
    match: schemas.KickerMatchCreate,
) -> str:
    kicker_elo_queue.put(match.model_dump())
    return "success"

@router.get("/matches", response_model=List[schemas.KickerMatch], operation_id="list_matches")
def list_matches(
    skip: int = 0,
    limit: int = 1000,
    match_repository: CRUDKickerMatch = Depends(get_kicker_match_repository)
) -> List[schemas.KickerMatch]:
    db_matches = match_repository.get_multi(skip=skip, limit=limit)
    return [schemas.KickerMatch.model_validate(match) for match in db_matches]


@router.get("/top_players", response_model=List[schemas.Member], operation_id="list_top_players")
def list_top_players(
    skip: int = 0,
    limit: int = 1000,
    member_repository: CRUDMember = Depends(get_member_repository)
) -> List[schemas.Member]:
    db_members = member_repository.get_tkt_top_players(skip=skip, limit=limit)
    return [schemas.Member.model_validate(member) for member in db_members]
