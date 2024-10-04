from fastapi import FastAPI

from starlette.config import Config

from src.routers.v1.BreedRouter import BreedRouter
from src.routers.v1.ColorRouter import ColorRouter
from src.routers.v1.KittenRouter import KittenRouter
from src.routers.v1.AuthRouter import AuthRouter


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
