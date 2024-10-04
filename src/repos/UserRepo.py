from uuid import UUID

from passlib.context import CryptContext
from src.models.UserModel import User, UserCreate, UserUpdate
from typing import Annotated
from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from src.db import session
from src.security import crypt


class UserRepo:
    def __init__(
        self,
        session: Annotated[Session, Depends(session)],
        crypt: Annotated[CryptContext, Depends(crypt)],
    ):
        self.session = session
        self.crypt = crypt

    def save(self, payload: UserCreate) -> None:
        """
        Persist a new user.
        """
        hash = self.crypt.hash(payload.password)
        user = User(username=payload.username, password=hash)
        self.session.add(user)
        self.session.commit()

    def get(self, user_id: UUID) -> User:
        """
        Read a single user.
        """
        q = select(User).where(User.id == user_id)
        res = self.session.exec(q).first()

        if not res:
            raise self.error_not_found()

        return res

    def list(self) -> list[User]:
        """
        Read all users.
        """
        q = select(User)
        res = self.session.exec(q).all()
        return list(res)

    def update(self, user_id: UUID, payload: UserUpdate) -> None:
        """
        Update a single user.
        """
        user = self.get(user_id)
        src = payload.model_dump(exclude_unset=True)
        user.sqlmodel_update(src)
        self.session.add(user)
        self.session.commit()

    def delete(self, user_id: UUID) -> None:
        """
        Delete a single user.
        """
        user = self.get(user_id)
        self.session.delete(user)
        self.session.commit()

    def get_by_username(self, username: str) -> User:
        q = select(User).where(User.username == username)
        res = self.session.exec(q).first()

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return res

    def verify(self, user: User, password: str) -> None:
        matches = self.crypt.verify(password, user.password)
        if not matches:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
            )

    @staticmethod
    def error_not_found() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
