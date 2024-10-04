from uuid import UUID
from src.models.ColorModel import Color, ColorCreate, ColorUpdate
from typing import Annotated
from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from src.db import session


class ColorRepo:
    def __init__(self, session: Annotated[Session, Depends(session)]):
        self.session = session

    def save(self, payload: ColorCreate) -> None:
        """
        Persist a new color.
        """
        color = Color(
            name=payload.name,
        )
        self.session.add(color)
        self.session.commit()

    def get(self, color_id: UUID) -> Color:
        """
        Read a single color.
        """
        q = select(Color).where(Color.id == color_id)
        res = self.session.exec(q).first()

        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Color not found"
            )

        return res

    def list(self) -> list[Color]:
        """
        Read all colors.
        """
        q = select(Color)
        res = self.session.exec(q).all()
        return list(res)

    def update(self, color_id: UUID, payload: ColorUpdate) -> None:
        """
        Update a single color.
        """
        color = self.get(color_id)
        src = payload.model_dump(exclude_unset=True)
        color.sqlmodel_update(src)
        self.session.add(color)
        self.session.commit()

    def delete(self, color_id: UUID) -> None:
        """
        Delete a single color.
        """
        color = self.get(color_id)
        self.session.delete(color)
        self.session.commit()
