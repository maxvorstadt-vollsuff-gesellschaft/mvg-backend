from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from .. import models
from ..auth_utils import get_current_user
from .. import repositories
from .. import schemas
from ..database import get_db

router = APIRouter(
    prefix="/quotes",
    tags=["quotes"]
)


@router.get("")
def get_quotes(limit: int = 10, skip: int = 0, db=Depends(get_db)):
    db_quotes = repositories.quote_repository.get_multi(db, limit=limit, skip=skip)
    return [schemas.Quote.model_validate(db_quote) for db_quote in db_quotes]


@router.post("", response_model=schemas.Quote)
def create_quote(
        quote: schemas.QuoteCreate,
        _current_user: Annotated[models.Member, Depends(get_current_user)],
        db=Depends(get_db)
) -> schemas.Quote:
    db_quote = repositories.quote_repository.create(db, quote)
    return schemas.Quote.from_orm(db_quote)


@router.get("/random_quote")
def quote_of_the_day(db=Depends(get_db)) -> schemas.Quote:
    db_quote = repositories.quote_repository.get_random(db)
    if db_quote is None:
        raise HTTPException(status_code=204, detail="There are no quotes yet")
    return schemas.Quote.model_validate(db_quote)

