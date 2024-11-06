import datetime
import os
from typing import Union, Annotated

from fastapi import HTTPException, Depends
from fastapi_keycloak import OIDCUser
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette import status

from .database import get_db
from . import repositories
from . import models

from fastapi_keycloak import FastAPIKeycloak

idp = FastAPIKeycloak(
    server_url="https://auth.toskana-fraktion.social/auth",
    client_id="mvg-life",
    client_secret=os.environ.get("KC_CLIENT_SECRET", "").strip(),
    realm="toskana-fraktion",
    admin_client_secret=os.environ.get("KC_ADMIN_SECRET", "").strip(),
    callback_uri=os.environ.get("KC_CALLBACK", "").strip() # http://localhost:8000/auth/callback
)


async def get_current_user(
        db: Annotated[Session, Depends(get_db)],
        user: OIDCUser = Depends(idp.get_current_user()),
) -> models.Member:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = repositories.member_repository.get_sub(db, user.sub)
        if user is None:
            raise credentials_exception
        return user
    except InvalidTokenError:
        raise credentials_exception

