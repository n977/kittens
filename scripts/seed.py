import os
import sys

# Include the current directory in PYTHONPATH to make the main package visible.
sys.path.insert(0, os.getcwd())

import logging

# Provide the basic configuration to the logger.
logging.basicConfig()

import csv

from uuid import UUID
from typing import TextIO
from collections.abc import Callable

from passlib.context import CryptContext
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.dialects import postgresql

from starlette.config import Config
from src.models.UserModel import User
from src.models.ColorModel import Color
from src.models.BreedModel import Breed
from src.models.KittenModel import Kitten
from src.db import url

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PREFIX = "csv"

cfg = Config(".env")
engine = create_engine(url(cfg))
session = Session(engine)
crypt = CryptContext(schemes=["bcrypt"])


def insert_if_not_exists(session: Session, model: SQLModel) -> None:
    st = (
        postgresql.insert(model.__class__)
        .values(**model.model_dump(exclude_unset=True))
        .on_conflict_do_nothing()
    )
    session.exec(st)


def proc(path: str, proc: Callable[[TextIO], None], required: bool = False) -> None:
    try:
        with open(path) as f:
            proc(f)
    except FileNotFoundError as e:
        if required:
            raise e
        else:
            logger.warning(f"Ignoring missing file '{path}'")
    # except:
    #     logger.error("Encountered an unknown error during file processing")


def seed() -> None:
    def users(f: TextIO) -> None:
        for id, username, password in csv.reader(f):
            hash = crypt.hash(password)
            user = User(id=UUID(id), username=username, password=hash)
            insert_if_not_exists(session, user)

    def colors(f: TextIO) -> None:
        for id, name in csv.reader(f):
            color = Color(id=UUID(id), name=name)
            insert_if_not_exists(session, color)

    def breeds(f: TextIO) -> None:
        for id, name in csv.reader(f):
            breed = Breed(id=UUID(id), name=name)
            insert_if_not_exists(session, breed)

    def kittens(f: TextIO) -> None:
        for id, color_id, age, breed_id, description in csv.reader(f):
            kitten = Kitten(
                id=UUID(id),
                color_id=UUID(color_id),
                age=int(age),
                breed_id=UUID(breed_id),
                description=description,
            )
            insert_if_not_exists(session, kitten)

    proc(f"{PREFIX}/users.csv", users, required=True)
    proc(f"{PREFIX}/colors.csv", colors)
    proc(f"{PREFIX}/breeds.csv", breeds)
    proc(f"{PREFIX}/kittens.csv", kittens)

    session.commit()
    logger.info("OK")


if __name__ == "__main__":
    seed()
