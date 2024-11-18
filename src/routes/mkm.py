from typing import Annotated, Optional
from fastapi import APIRouter, Depends

from ..repositories.mkm import MKMRepository, get_mkm_repository
from ..schemas import MKMCreate, MKM

router = APIRouter(
    prefix="/mkm",
    tags=["mkm", "mvg"]
)


@router.post("/", response_model=MKM)
async def create_mkm(mkm: MKMCreate, mkm_repo: Annotated[MKMRepository, Depends(get_mkm_repository)]):
    db_mkm = mkm_repo.create(mkm)
    return MKM.model_validate(db_mkm)

