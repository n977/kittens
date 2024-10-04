from fastapi import Depends, HTTPException

from typing import Annotated
from uuid import UUID

from src.security import public_key, oauth2_scheme
from src.repos.UserRepo import UserRepo

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
    except:
        raise HTTPException(status_code=401, detail="Invalid access token")
