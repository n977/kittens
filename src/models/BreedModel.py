from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4

from src.models import BaseModel


NAME_MAX_LENGTH = 255


class BreedBase(BaseModel):
    """
    A set of common Breed model properties.
    """

    name: str = Field(max_length=NAME_MAX_LENGTH, unique=True, index=True)


class Breed(BreedBase, table=True):
    """
    A Breed table model.
    """

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)


class BreedRead(BreedBase):
    """
    A Breed GET response model.
    """

    id: UUID


class BreedCreate(SQLModel):
    """
    A Breed POST request model.
    """

    name: str = Field(max_length=NAME_MAX_LENGTH)


class BreedUpdate(SQLModel):
    """
    A Breed PATCH request model.
    """

    name: Optional[str] = Field(default=None, max_length=NAME_MAX_LENGTH)
