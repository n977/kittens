from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from uuid import UUID
from kittens.repos.breed import BreedRepo
from kittens.models.breed import Breed, BreedCreate, BreedUpdate, BreedRead
from kittens.models.user import User
from kittens.auth import user, UNAUTHORIZED


BreedRouter = APIRouter(
    prefix="/v1/breeds",
    tags=["breed"],
)


@BreedRouter.post("/", status_code=status.HTTP_201_CREATED, responses={**UNAUTHORIZED})
def save(
    payload: BreedCreate,
    breeds: Annotated[BreedRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Save a single breed.
    """

    breeds.save(payload)


@BreedRouter.get("/", response_model=list[BreedRead])
def list(breeds: Annotated[BreedRepo, Depends()]) -> list[Breed]:
    """
    Return all breeds.
    """

    return breeds.list()


@BreedRouter.get("/{breed_id}", response_model=BreedRead)
def get(breed_id: UUID, breeds: Annotated[BreedRepo, Depends()]) -> Breed:
    """
    Return a single breed.
    """

    breed = breeds.get(breed_id)
    if not breed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Breed not found"
        )
    return breed


@BreedRouter.patch("/{breed_id}", responses={**UNAUTHORIZED})
def update(
    breed_id: UUID,
    payload: BreedUpdate,
    breeds: Annotated[BreedRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Update a single breed.
    """

    breeds.update(breed_id, payload)


@BreedRouter.delete("/{breed_id}", responses={**UNAUTHORIZED})
def delete(
    breed_id: UUID,
    breeds: Annotated[BreedRepo, Depends()],
    _: Annotated[User, Depends(user)],
) -> None:
    """
    Delete a single breed.
    """

    breeds.delete(breed_id)
