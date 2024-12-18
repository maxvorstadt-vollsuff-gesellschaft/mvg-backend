from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..repositories import get_kicker_match_repository, CRUDKickerMatch

router = APIRouter(
    prefix="/goal_tracker",
    tags=["kicker", "mvg"]
)

@router.post("/matches", response_model=schemas.KickerMatch, operation_id="create_match")
def create_match(
    match: schemas.KickerMatchCreate,
    match_repository: CRUDKickerMatch = Depends(get_kicker_match_repository)
) -> schemas.KickerMatch:
    db_match = match_repository.create(match)
    return schemas.KickerMatch.model_validate(db_match)

@router.get("/matches", response_model=List[schemas.KickerMatch], operation_id="list_matches")
def list_matches(
    skip: int = 0,
    limit: int = 10,
    match_repository: CRUDKickerMatch = Depends(get_kicker_match_repository)
) -> List[schemas.KickerMatch]:
    db_matches = match_repository.get_multi(skip=skip, limit=limit)
    return [schemas.KickerMatch.model_validate(match) for match in db_matches]