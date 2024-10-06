from uuid import UUID
from kittens.models.color import Color, ColorCreate, ColorUpdate
from typing import Annotated, Optional
from fastapi import Depends
from sqlmodel import Session, select
from kittens.db import session


class ColorRepo:
    def __init__(self, session: Annotated[Session, Depends(session)]):
        self.session = session

    def save(self, payload: ColorCreate) -> bool:
        """
        Save a single color.
        """

        color = Color(
            name=payload.name,
        )
        try:
            self.session.add(color)
            self.session.commit()
        except Exception:
            return False
        return True

    def get(self, color_id: UUID) -> Optional[Color]:
        """
        Read a single color.
        """

        try:
            return self.session.exec(select(Color).where(Color.id == color_id)).first()
        except Exception:
            return None

    def list(self) -> list[Color]:
        """
        Read all colors.
        """

        try:
            return list(self.session.exec(select(Color)))
        except Exception:
            return []

    def update(self, color_id: UUID, payload: ColorUpdate) -> bool:
        """
        Update a single color.
        """

        color = self.get(color_id)
        if not color:
            return False
        src = payload.model_dump(exclude_unset=True)
        try:
            color.sqlmodel_update(src)
            self.session.add(color)
            self.session.commit()
        except Exception:
            return False
        return True

    def delete(self, color_id: UUID) -> bool:
        """
        Delete a single color.
        """

        color = self.get(color_id)
        if not color:
            return False
        try:
            self.session.delete(color)
            self.session.commit()
        except Exception:
            return False
        return True
