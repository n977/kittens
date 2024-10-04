from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from typing import Optional

from src.models import BaseModel

DESCRIPTION_MAX_LENGTH = 255


class KittenBase(BaseModel):
    """
    A set of common Kitten model properties.
    """

    color_id: UUID = Field(foreign_key="color.id", index=True, ondelete="CASCADE")
    age: int = Field(index=True)
    breed_id: UUID = Field(foreign_key="breed.id", index=True, ondelete="CASCADE")
    description: str = Field(max_length=DESCRIPTION_MAX_LENGTH)


class Kitten(KittenBase, table=True):
    """
    A Kitten table model.
    """

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)


class KittenRead(KittenBase):
    """
    A Kitten GET response model.
    """

    id: UUID


class KittenCreate(SQLModel):
    """
    A Kitten POST request model.
    """

    color_id: UUID
    age: int
    breed_id: UUID
    description: str = Field(max_length=DESCRIPTION_MAX_LENGTH)


class KittenUpdate(SQLModel):
    """
    A Kitten PATCH request model.
    """

    color_id: Optional[UUID] = None
    age: Optional[int] = None
    breed_id: Optional[UUID] = None
    description: Optional[str] = Field(default=None, max_length=DESCRIPTION_MAX_LENGTH)
