import os
from typing import Annotated, Callable

from fastapi import HTTPException, Depends
from fastapi_keycloak import OIDCUser, FastAPIKeycloak
from jwt import InvalidTokenError
from starlette import status

from .repositories import get_member_repository
from .repositories.member import CRUDMember
from . import models

idp = FastAPIKeycloak(
    server_url="https://auth.toskana-fraktion.social/auth",
    client_id="mvg-life",
    client_secret=os.environ.get("KC_CLIENT_SECRET", "").strip(),
    realm="toskana-fraktion",
    admin_client_secret=os.environ.get("KC_ADMIN_SECRET", "").strip(),
    callback_uri=os.environ.get("KC_CALLBACK", "").strip()  # http://localhost:8000/auth/callback
)


async def get_current_user(
    member_repository: Annotated[CRUDMember, Depends(get_member_repository)],
    user: OIDCUser = Depends(idp.get_current_user()),
) -> models.Member:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user_db = member_repository.get_sub(user.sub)
        if user_db is None:
            raise credentials_exception
        return user_db
    except InvalidTokenError:
        raise credentials_exception


def get_current_user_with_roles(
    required_roles: list[str] = []
) -> Callable:
    async def inner(
        member_repository: Annotated[CRUDMember, Depends(get_member_repository)],
        user: OIDCUser = Depends(idp.get_current_user(required_roles=required_roles))
    ) -> models.Member:
        return await get_current_user(member_repository, user)
    return inner
