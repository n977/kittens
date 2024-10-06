from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from kittens.models import BaseModel


USERNAME_MIN_LENGTH = 1
USERNAME_MAX_LENGTH = 16


class UserBase(BaseModel):
    """
    A set of common User model properties.
    """

    username: str = Field(
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        index=True,
    )
    password: str


class User(UserBase, table=True):
    """
    A User table model.
    """

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)


class UserRead(UserBase):
    """
    A User get response model.
    """

    id: UUID


class UserCreate(SQLModel):
    username: str = Field(
        min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH
    )
    password: str


class UserUpdate(SQLModel):
    username: Optional[str] = Field(
        default=None, min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH
    )
    password: Optional[str]
