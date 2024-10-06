from uuid import UUID
from kittens.models.breed import Breed, BreedCreate, BreedUpdate
from typing import Annotated, Optional
from fastapi import Depends
from sqlmodel import Session, select
from kittens.db import session


class BreedRepo:
    def __init__(self, session: Annotated[Session, Depends(session)]):
        self.session = session

    def save(self, payload: BreedCreate) -> bool:
        """
        Save a single breed.
        """

        breed = Breed(
            name=payload.name,
        )
        try:
            self.session.add(breed)
            self.session.commit()
        except Exception:
            return False
        return True

    def get(self, breed_id: UUID) -> Optional[Breed]:
        """
        Read a single breed.
        """

        try:
            return self.session.exec(select(Breed).where(Breed.id == breed_id)).first()
        except Exception:
            return None

    def list(self) -> list[Breed]:
        """
        Read all breeds.
        """

        try:
            return list(self.session.exec(select(Breed)))
        except Exception:
            return []

    def update(self, breed_id: UUID, payload: BreedUpdate) -> bool:
        """
        Update a single breed.
        """

        breed = self.get(breed_id)
        if not breed:
            return False
        src = payload.model_dump(exclude_unset=True)
        try:
            breed.sqlmodel_update(src)
            self.session.add(breed)
            self.session.commit()
        except Exception:
            return False
        return True

    def delete(self, breed_id: UUID) -> bool:
        """
        Delete a single breed.
        """

        breed = self.get(breed_id)
        if not breed:
            return False
        try:
            self.session.delete(breed)
            self.session.commit()
        except Exception:
            return False
        return True
