from functools import cache
from typing import Generator
from starlette.config import Config
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.dialects import postgresql


def url(cfg: Config) -> str:
    DB_PROTO = cfg("DB_PROTO")
    DB_HOST = cfg("DB_HOST")
    DB_PORT = cfg("DB_PORT")
    DB_DATABASE = cfg("DB_DATABASE")
    DB_USER = cfg("DB_USER")
    DB_PASSWORD = cfg("DB_PASSWORD")

    return f"{DB_PROTO}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"


@cache
def engine():
    cfg = Config(".env")
    return create_engine(url(cfg))


def session() -> Generator[Session, None, None]:
    with Session(engine()) as session:
        yield session


def insert_if_not_exists(session: Session, model: SQLModel) -> None:
    st = (
        postgresql.insert(model.__class__)
        .values(**model.model_dump(exclude_unset=True))
        .on_conflict_do_nothing()
    )
    session.exec(st)
