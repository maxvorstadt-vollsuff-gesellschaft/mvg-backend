from fastapi import APIRouter
from passlib.context import CryptContext

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/hash")
def set_password(pw: str):
    return pwd_context.hash(pw)
