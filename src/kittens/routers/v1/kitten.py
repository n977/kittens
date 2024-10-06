from fastapi import APIRouter, Depends, HTTPException, status

from typing import Optional, Annotated
from uuid import UUID

from kittens.repos.kitten import KittenRepo
from kittens.models.kitten import Kitten, KittenCreate, KittenUpdate, KittenRead
from kittens.models.user import User
from kittens.auth import user, UNAUTHORIZED


KittenRouter = APIRouter(
    prefix="/v1/kittens",
    tags=["kitten"],
)


@KittenRouter.post("/", status_code=status.HTTP_201_CREATED, responses={**UNAUTHORIZED})
def save(
    payload: KittenCreate,
    kittens: Annotated[KittenRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Save a single kitten.
    """

    kittens.save(payload)


@KittenRouter.get("/", response_model=list[KittenRead])
def list(
    kittens: Annotated[KittenRepo, Depends()],
    color_id: Optional[UUID] = None,
    breed_id: Optional[UUID] = None,
) -> list[Kitten]:
    """
    Return all kittens.
    """

    return kittens.list(color_id=color_id, breed_id=breed_id)


@KittenRouter.get("/{kitten_id}", response_model=KittenRead)
def get(kitten_id: UUID, kittens: Annotated[KittenRepo, Depends()]) -> Kitten:
    """
    Return a single kitten.
    """

    kitten = kittens.get(kitten_id)
    if not kitten:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Kitten not found"
        )
    return kitten


@KittenRouter.patch("/{kitten_id}", responses={**UNAUTHORIZED})
def update(
    kitten_id: UUID,
    payload: KittenUpdate,
    kittens: Annotated[KittenRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Update a single kitten.
    """

    kittens.update(kitten_id, payload)


@KittenRouter.delete("/{kitten_id}", responses={**UNAUTHORIZED})
def delete(
    kitten_id: UUID,
    kittens: Annotated[KittenRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Delete a single kitten.
    """

    kittens.delete(kitten_id)
