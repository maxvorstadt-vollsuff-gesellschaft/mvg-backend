from typing import Annotated, List, Tuple

from fastapi import APIRouter, Depends, HTTPException
from fastapi_keycloak import OIDCUser
from .. import models, schemas
from ..auth_utils import get_current_user
from ..repositories import get_quote_repository
from ..repositories.quote import CRUDQuote

router = APIRouter(
    prefix="/quotes",
    tags=["quotes", "mvg"]
)


@router.get("", operation_id="list_quotes")
def get_quotes(
    quote_repository: Annotated[CRUDQuote, Depends(get_quote_repository)],
    skip: int = 0,
    limit: int = 10,
) -> List[schemas.Quote]:
    db_quotes = quote_repository.get_multi(skip=skip, limit=limit)
    return [schemas.Quote.model_validate(db_quote) for db_quote in db_quotes]


@router.post("", response_model=schemas.Quote, operation_id="create_quote")
def create_quote(
    quote: schemas.QuoteCreate,
    _user_info: Annotated[Tuple[OIDCUser, models.Member], Depends(get_current_user)],
    quote_repository: Annotated[CRUDQuote, Depends(get_quote_repository)]
) -> schemas.Quote:
    db_quote = quote_repository.create(quote)
    return schemas.Quote.model_validate(db_quote)


@router.get("/random_quote", operation_id="get_random_quote")
def quote_of_the_day(
    quote_repository: Annotated[CRUDQuote, Depends(get_quote_repository)]
) -> schemas.Quote:
    db_quote = quote_repository.get_random()
    if db_quote is None:
        raise HTTPException(status_code=204, detail="There are no quotes yet")
    return schemas.Quote.model_validate(db_quote)
