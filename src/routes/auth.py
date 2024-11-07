from typing import Annotated
from fastapi import APIRouter, Depends, Request, HTTPException
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
import jwt
from pydantic import BaseModel
import requests
from starlette.responses import JSONResponse

from ..models import Member
from ..database import get_db
from ..auth_utils import idp
from ..repositories import member_repository
from .. import schemas
from .. import models
from ..auth_utils import get_current_user
router = APIRouter(
    prefix="/auth",
    tags=["auth", "mvg"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/login", operation_id="redirect_to_login")
def login_redirect():
    return RedirectResponse(idp.login_uri)


@router.get("/callback", operation_id="process_oauth_callback")
def callback(session_state: str, code: str, db=Depends(get_db)):
    token = idp.exchange_authorization_code(session_state=session_state, code=code)
    user_info = jwt.decode(token.access_token, options={"verify_signature": False})
    user_sub = user_info.get('sub')
    username = user_info.get('preferred_username')

    if member_repository.get_sub(db, user_sub) is None:
        member_repository.create(db, Member(user_sub=user_sub, name=username))

    return token


class TokenRefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", operation_id="refresh_access_token")
def refresh_token(
    token_data: TokenRefreshRequest,
):
    token = token_data.refresh_token

    response = requests.post(idp.token_uri, data={
        'client_id': idp.client_id,
        'client_secret': idp.client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': token
    })

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    if not refresh_token:
        raise HTTPException(status_code=401, detail=response.text)

    token_response = response.json()
    return JSONResponse(content={
        "access_token": token_response['access_token'],
        "refresh_token": token_response.get('refresh_token', refresh_token),
    })


@router.post("/logout", operation_id="logout_user")
def logout():
    idp.logout_uri

@router.get("/me", operation_id="read_current_user")
async def read_users_me(
    current_user: Annotated[models.Member, Depends(get_current_user)]
) -> schemas.Member:
    return schemas.Member.model_validate(current_user)
