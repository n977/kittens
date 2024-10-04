from typing import Annotated
from fastapi import APIRouter, Depends, status
from uuid import UUID
from src.repos.ColorRepo import ColorRepo
from src.models.ColorModel import Color, ColorCreate, ColorUpdate, ColorRead
from src.models.UserModel import User
from src.auth import user


ColorRouter = APIRouter(
    prefix="/v1/colors",
    tags=["color"],
)


@ColorRouter.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
async def save(
    payload: ColorCreate,
    colors: Annotated[ColorRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Save a single color.
    """
    colors.save(payload)


@ColorRouter.get("/", response_model=list[ColorRead])
async def list(colors: Annotated[ColorRepo, Depends()]) -> list[Color]:
    """
    Return all colors.
    """
    return colors.list()


@ColorRouter.get("/{color_id}", response_model=ColorRead)
async def get(color_id: UUID, colors: Annotated[ColorRepo, Depends()]) -> Color:
    """
    Return a single color.
    """
    return colors.get(color_id)


@ColorRouter.patch("/{color_id}", response_model=None)
async def update(
    color_id: UUID,
    payload: ColorUpdate,
    colors: Annotated[ColorRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Update a single color.
    """
    colors.update(color_id, payload)


@ColorRouter.delete("/{color_id}", response_model=None)
async def delete(
    color_id: UUID,
    colors: Annotated[ColorRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Delete a single color.
    """
    colors.delete(color_id)
