from uuid import UUID
from src.models.KittenModel import Kitten, KittenCreate, KittenUpdate
from typing import Optional, Annotated
from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from src.db import session


class KittenRepo:
    def __init__(self, session: Annotated[Session, Depends(session)]):
        self.session = session

    def save(self, payload: KittenCreate) -> None:
        """
        Persist a new kitten.
        """
        kitten = Kitten(
            color_id=payload.color_id,
            age=payload.age,
            breed_id=payload.breed_id,
            description=payload.description,
        )
        self.session.add(kitten)
        self.session.commit()

    def get(self, kitten_id: UUID) -> Kitten:
        """
        Read a single kitten.
        """
        q = select(Kitten).where(Kitten.id == kitten_id)
        res = self.session.exec(q).first()

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Kitten not found"
            )

        return res

    def list(self, color_id: Optional[UUID], breed_id: Optional[UUID]) -> list[Kitten]:
        """
        Read many kittens.
        """
        q = select(Kitten)
        if color_id:
            q = q.where(Kitten.color_id == color_id)
        if breed_id:
            q = q.where(Kitten.breed_id == breed_id)

        res = self.session.exec(q).all()
        return list(res)

    def update(self, kitten_id: UUID, payload: KittenUpdate) -> None:
        """
        Update a single kitten.
        """
        kitten = self.get(kitten_id)
        src = payload.model_dump(exclude_unset=True)
        kitten.sqlmodel_update(src)
        self.session.add(kitten)
        self.session.commit()

    def delete(self, kitten_id: UUID) -> None:
        """
        Delete a single kitten.
        """
        kitten = self.get(kitten_id)
        self.session.delete(kitten)
        self.session.commit()
