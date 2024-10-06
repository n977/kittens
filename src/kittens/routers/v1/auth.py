from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlmodel import SQLModel
from kittens.repos.user import UserRepo
from kittens.security import private_key
from kittens.auth import UNAUTHORIZED
import jwt as pyjwt

AuthRouter = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
)


class Token(SQLModel):
    access_token: str
    token_type: str


@AuthRouter.post("/login", response_model=Token, responses={**UNAUTHORIZED})
def login(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    users: Annotated[UserRepo, Depends()],
    private_key: Annotated[str, Depends(private_key)],
) -> Token:
    """
    Issue a fresh access token.
    """
    user = users.get(payload.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not users.verify(user, payload.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    jwt = pyjwt.encode(
        {"sub": str(user.id), "iss": str(datetime.now(tz=timezone.utc))},
        private_key,
        algorithm="RS256",
    )
    return Token(access_token=jwt, token_type="Bearer")
