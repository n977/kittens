from fastapi import APIRouter, Depends, status

from typing import Optional, Annotated
from uuid import UUID

from src.repos.KittenRepo import KittenRepo
from src.models.KittenModel import Kitten, KittenCreate, KittenUpdate, KittenRead
from src.models.UserModel import User
from src.auth import user


KittenRouter = APIRouter(
    prefix="/v1/kittens",
    tags=["kitten"],
)


@KittenRouter.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
async def save(
    payload: KittenCreate,
    kittens: Annotated[KittenRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Save a single kitten.
    """
    kittens.save(payload)


@KittenRouter.get("/", response_model=list[KittenRead])
async def list(
    kittens: Annotated[KittenRepo, Depends()],
    color_id: Optional[UUID] = None,
    breed_id: Optional[UUID] = None,
) -> list[Kitten]:
    """
    Return all kittens.
    """
    return kittens.list(color_id=color_id, breed_id=breed_id)


@KittenRouter.get("/{kitten_id}", response_model=KittenRead)
async def get(kitten_id: UUID, kittens: Annotated[KittenRepo, Depends()]) -> Kitten:
    """
    Return a single kitten.
    """
    return kittens.get(kitten_id)


@KittenRouter.patch("/{kitten_id}", response_model=None)
async def update(
    kitten_id: UUID,
    payload: KittenUpdate,
    kittens: Annotated[KittenRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Patch a single kitten.
    """
    kittens.update(kitten_id, payload)


@KittenRouter.delete("/{kitten_id}", response_model=None)
async def delete(
    kitten_id: UUID,
    kittens: Annotated[KittenRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Delete a single kitten.
    """
    kittens.delete(kitten_id)
