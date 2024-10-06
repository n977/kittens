from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from kittens.repos.color import ColorRepo
from kittens.models.color import Color, ColorCreate, ColorUpdate, ColorRead
from kittens.models.user import User
from kittens.auth import user, UNAUTHORIZED


ColorRouter = APIRouter(
    prefix="/v1/colors",
    tags=["color"],
)


@ColorRouter.post("/", status_code=status.HTTP_201_CREATED, responses={**UNAUTHORIZED})
def save(
    payload: ColorCreate,
    colors: Annotated[ColorRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Save a single color.
    """

    colors.save(payload)


@ColorRouter.get("/", response_model=list[ColorRead])
def list(colors: Annotated[ColorRepo, Depends()]) -> list[Color]:
    """
    Return all colors.
    """

    return colors.list()


@ColorRouter.get("/{color_id}", response_model=ColorRead)
def get(color_id: UUID, colors: Annotated[ColorRepo, Depends()]) -> Color:
    """
    Return a single color.
    """

    color = colors.get(color_id)
    if not color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Color not found"
        )
    return color


@ColorRouter.patch("/{color_id}", responses={**UNAUTHORIZED})
def update(
    color_id: UUID,
    payload: ColorUpdate,
    colors: Annotated[ColorRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Update a single color.
    """

    colors.update(color_id, payload)


@ColorRouter.delete("/{color_id}", responses={**UNAUTHORIZED})
def delete(
    color_id: UUID,
    colors: Annotated[ColorRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Delete a single color.
    """

    colors.delete(color_id)
