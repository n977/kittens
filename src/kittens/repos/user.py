from uuid import UUID
from passlib.context import CryptContext
from kittens.models.user import User, UserCreate, UserUpdate
from typing import Annotated, Optional
from fastapi import Depends
from sqlmodel import Session, select
from kittens.db import session
from kittens.security import crypt


class UserRepo:
    def __init__(
        self,
        session: Annotated[Session, Depends(session)],
        crypt: Annotated[CryptContext, Depends(crypt)],
    ):
        self.session = session
        self.crypt = crypt

    def save(self, payload: UserCreate) -> bool:
        """
        Save a single user.
        """

        hash = self.crypt.hash(payload.password)
        user = User(username=payload.username, password=hash)
        try:
            self.session.add(user)
            self.session.commit()
        except Exception:
            return False
        return True

    def get(self, key: UUID | str) -> Optional[User]:
        """
        Read a single user.
        """

        q = select(User)

        if isinstance(key, str):
            q = q.where(User.username == key)
        else:
            q = q.where(User.id == key)

        try:
            return self.session.exec(q).first()
        except Exception:
            return None

    def list(self) -> list[User]:
        """
        Read all users.
        """

        try:
            return list(self.session.exec(select(User)))
        except Exception:
            return []

    def update(self, user_id: UUID, payload: UserUpdate) -> bool:
        """
        Update a single user.
        """

        user = self.get(user_id)
        if not user:
            return False
        src = payload.model_dump(exclude_unset=True)
        try:
            user.sqlmodel_update(src)
            self.session.add(user)
            self.session.commit()
        except Exception:
            return False
        return True

    def delete(self, user_id: UUID) -> bool:
        """
        Delete a single user.
        """

        user = self.get(user_id)
        if not user:
            return False
        try:
            self.session.delete(user)
            self.session.commit()
        except Exception:
            return False
        return True

    def verify(self, user: User, password: str) -> bool:
        """
        Compare a user's hashed password with the plaintext one.
        """

        return self.crypt.verify(password, user.password)
