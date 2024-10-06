import pytest
import sqlalchemy as sa
from typing import Generator
from sqlalchemy import Engine, RootTransaction
from starlette.config import Config
from sqlmodel import SQLModel, Session, create_engine
from passlib.context import CryptContext
from kittens.db import url
from kittens.models.kitten import Kitten
from kittens.models.color import Color
from kittens.models.breed import Breed
from kittens.models.user import User
from kittens.repos.color import ColorRepo
from kittens.repos.breed import BreedRepo
from kittens.repos.kitten import KittenRepo
from kittens.repos.user import UserRepo


@pytest.fixture(scope="session")
def engine() -> Engine:
    cfg = Config(".env.test")
    u = url(cfg)
    return create_engine(u)


@pytest.fixture(scope="session")
def tables(engine: Engine) -> Generator[None, None, None]:
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def session(engine: Engine, tables: None) -> Generator[Session, None, None]:
    conn = engine.connect()
    transaction = conn.begin()
    session = Session(bind=conn)

    nested = conn.begin_nested()

    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(_session: Session, _transaction: RootTransaction):
        nonlocal nested
        if not nested.is_active:
            nested = conn.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    conn.close()


@pytest.fixture
def crypt() -> CryptContext:
    return CryptContext(schemes=["bcrypt"])


@pytest.fixture
def colors(session: Session) -> ColorRepo:
    return ColorRepo(session)


@pytest.fixture
def breeds(session: Session) -> BreedRepo:
    return BreedRepo(session)


@pytest.fixture
def kittens(session: Session) -> KittenRepo:
    return KittenRepo(session)


@pytest.fixture
def users(session: Session, crypt: CryptContext) -> UserRepo:
    return UserRepo(session, crypt)
