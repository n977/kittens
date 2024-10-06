from fastapi import Depends, HTTPException
from fastapi import status
from typing import Annotated
from uuid import UUID
from kittens.security import public_key, oauth2_scheme
from kittens.repos.user import UserRepo
import jwt as pyjwt


def user(
    token: Annotated[str, Depends(oauth2_scheme)],
    users: Annotated[UserRepo, Depends()],
    public_key: Annotated[str, Depends(public_key)],
):
    try:
        payload = pyjwt.decode(token, public_key, algorithms=["RS256"])
        user = users.get(UUID(payload["sub"]))
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid access token")


UNAUTHORIZED = {status.HTTP_401_UNAUTHORIZED: {"description": "Authentication Error"}}
