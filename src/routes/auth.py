from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
import jwt

from ..models import Member
from ..database import get_db
from ..auth_utils import idp
from ..repositories import member_repository
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/login")
def login_redirect():
    return RedirectResponse(idp.login_uri)


@router.get("/callback")
def callback(session_state: str, code: str, db=Depends(get_db)):
    token = idp.exchange_authorization_code(session_state=session_state, code=code)
    user_info = jwt.decode(token.access_token, options={"verify_signature": False})
    user_sub = user_info.get('sub')
    username = user_info.get('preferred_username')

    if member_repository.get_sub(db, user_sub) is None:
        member_repository.create(db, Member(user_sub=user_sub, name=username))

    return token