from uuid import UUID
from src.models.BreedModel import Breed, BreedCreate, BreedUpdate
from typing import Annotated
from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from src.db import session


class BreedRepo:
    def __init__(self, session: Annotated[Session, Depends(session)]):
        self.session = session

    def save(self, payload: BreedCreate) -> None:
        """
        Persist a new breed.
        """
        breed = Breed(
            name=payload.name,
        )
        self.session.add(breed)
        self.session.commit()

    def get(self, breed_id: UUID) -> Breed:
        """
        Read a single breed.
        """
        q = select(Breed).where(Breed.id == breed_id)
        res = self.session.exec(q).first()

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Breed not found"
            )

        return res

    def list(self) -> list[Breed]:
        """
        Read all breeds.
        """
        q = select(Breed)
        res = self.session.exec(q).all()
        return list(res)

    def update(self, breed_id: UUID, payload: BreedUpdate) -> None:
        """
        Update a single breed.
        """
        breed = self.get(breed_id)
        src = payload.model_dump(exclude_unset=True)
        breed.sqlmodel_update(src)
        self.session.add(breed)
        self.session.commit()

    def delete(self, breed_id: UUID) -> None:
        """
        Delete a single breed.
        """
        breed = self.get(breed_id)
        self.session.delete(breed)
        self.session.commit()
