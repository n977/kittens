from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field

from kittens.models import BaseModel


NAME_MAX_LENGTH = 255


class ColorBase(BaseModel):
    """
    A set of common Color model properties.
    """

    name: str = Field(max_length=NAME_MAX_LENGTH, unique=True, index=True)


class Color(ColorBase, table=True):
    """
    A Color table model.
    """

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)


class ColorRead(ColorBase):
    """
    A Color GET response model.
    """

    id: UUID


class ColorCreate(SQLModel):
    """
    A Color POST request model.
    """

    name: str = Field(max_length=NAME_MAX_LENGTH)


class ColorUpdate(SQLModel):
    """
    A Color PATCH response model.
    """

    name: Optional[str] = Field(default=None, max_length=NAME_MAX_LENGTH)
