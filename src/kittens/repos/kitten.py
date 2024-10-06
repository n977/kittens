from uuid import UUID
from kittens.models.kitten import Kitten, KittenCreate, KittenUpdate
from typing import Optional, Annotated
from fastapi import Depends
from sqlmodel import Session, select
from kittens.db import session


class KittenRepo:
    def __init__(self, session: Annotated[Session, Depends(session)]):
        self.session = session

    def save(self, payload: KittenCreate) -> bool:
        """
        Save a single kitten.
        """

        kitten = Kitten(
            color_id=payload.color_id,
            age=payload.age,
            breed_id=payload.breed_id,
            description=payload.description,
        )
        try:
            self.session.add(kitten)
            self.session.commit()
        except Exception:
            return False
        return True

    def get(self, kitten_id: UUID) -> Optional[Kitten]:
        """
        Read a single kitten.
        """

        try:
            return self.session.exec(
                select(Kitten).where(Kitten.id == kitten_id)
            ).first()
        except Exception:
            return None

    def list(
        self, *, color_id: Optional[UUID] = None, breed_id: Optional[UUID] = None
    ) -> list[Kitten]:
        """
        Read many kittens.
        """

        q = select(Kitten)
        if color_id:
            q = q.where(Kitten.color_id == color_id)
        if breed_id:
            q = q.where(Kitten.breed_id == breed_id)

        try:
            return list(self.session.exec(q))
        except Exception:
            return []

    def update(self, kitten_id: UUID, payload: KittenUpdate) -> bool:
        """
        Update a single kitten.
        """

        kitten = self.get(kitten_id)
        if not kitten:
            return False
        src = payload.model_dump(exclude_unset=True)
        try:
            kitten.sqlmodel_update(src)
            self.session.add(kitten)
            self.session.commit()
        except Exception:
            return False
        return True

    def delete(self, kitten_id: UUID) -> bool:
        """
        Delete a single kitten.
        """

        kitten = self.get(kitten_id)
        if not kitten:
            return False
        try:
            self.session.delete(kitten)
            self.session.commit()
        except Exception:
            return False
        return True
