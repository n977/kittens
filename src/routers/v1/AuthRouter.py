from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timezone

from fastapi import Depends
from fastapi.routing import APIRouter

from sqlmodel import SQLModel

from src.repos.UserRepo import UserRepo
from src.security import private_key

import jwt as pyjwt

AuthRouter = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
)


class Token(SQLModel):
    access_token: str
    token_type: str


@AuthRouter.post("/login", response_model=Token)
async def login(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    users: Annotated[UserRepo, Depends()],
    private_key: Annotated[str, Depends(private_key)],
) -> Token:
    """
    Issue a fresh access token.
    """
    user = users.get_by_username(payload.username)
    users.verify(user, payload.password)
    jwt = pyjwt.encode(
        {"sub": str(user.id), "iss": str(datetime.now(tz=timezone.utc))},
        private_key,
        algorithm="RS256",
    )
    return Token(access_token=jwt, token_type="Bearer")
