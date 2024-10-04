from fastapi import APIRouter, Depends, status

from typing import Annotated
from uuid import UUID

from src.repos.BreedRepo import BreedRepo
from src.models.BreedModel import Breed, BreedCreate, BreedUpdate, BreedRead
from src.models.UserModel import User
from src.auth import user


BreedRouter = APIRouter(
    prefix="/v1/breeds",
    tags=["breed"],
)


@BreedRouter.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
async def save(
    payload: BreedCreate,
    breeds: Annotated[BreedRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Save a single breed.
    """
    breeds.save(payload)


@BreedRouter.get("/", response_model=list[BreedRead])
async def list(breeds: Annotated[BreedRepo, Depends()]) -> list[Breed]:
    """
    Return all breeds.
    """
    return breeds.list()


@BreedRouter.get("/{breed_id}", response_model=BreedRead)
async def get(breed_id: UUID, breeds: Annotated[BreedRepo, Depends()]) -> Breed:
    """
    Return a single breed.
    """
    return breeds.get(breed_id)


@BreedRouter.patch("/{breed_id}", response_model=None)
async def update(
    breed_id: UUID,
    payload: BreedUpdate,
    breeds: Annotated[BreedRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Update a single breed.
    """
    breeds.update(breed_id, payload)


@BreedRouter.delete("/{breed_id}", response_model=None)
async def delete(
    breed_id: UUID,
    breeds: Annotated[BreedRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Delete a single breed.
    """
    breeds.delete(breed_id)
