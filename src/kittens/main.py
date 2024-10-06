from fastapi import FastAPI
from starlette.config import Config
from kittens.routers.v1.breed import BreedRouter
from kittens.routers.v1.color import ColorRouter
from kittens.routers.v1.kitten import KittenRouter
from kittens.routers.v1.auth import AuthRouter


cfg = Config(".env")

app = FastAPI(
    title=cfg("APP_NAME"),
    docs_url=None,
    redoc_url=cfg("REDOC_URL"),
)

app.include_router(KittenRouter)
app.include_router(BreedRouter)
app.include_router(ColorRouter)
app.include_router(AuthRouter)
