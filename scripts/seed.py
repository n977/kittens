import logging
import csv
from uuid import UUID
from typing import TextIO
from collections.abc import Callable
from passlib.context import CryptContext
from sqlmodel import create_engine, Session
from starlette.config import Config
from kittens.models.color import Color
from kittens.models.breed import Breed
from kittens.models.kitten import Kitten
from kittens.models.user import User
from kittens.db import url, insert_if_not_exists

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PREFIX = "csv"

cfg = Config(".env")
engine = create_engine(url(cfg))
session = Session(engine)
crypt = CryptContext(schemes=["bcrypt"])


def proc(path: str, proc: Callable[[TextIO], None], required: bool = False) -> None:
    try:
        with open(path) as f:
            proc(f)
    except FileNotFoundError as e:
        if required:
            raise e
        else:
            logger.warning(f"Ignoring missing file '{path}'")
    except Exception:
        logger.error("Encountered an unknown error during file processing")


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
