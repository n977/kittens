from fastapi.security import OAuth2PasswordBearer


from functools import cache
from passlib.context import CryptContext
from starlette.config import Config


oauth2_scheme = OAuth2PasswordBearer("/v1/auth/login")


@cache
def crypt() -> CryptContext:
    return CryptContext(schemes=["bcrypt"])


@cache
def private_key() -> str:
    cfg = Config(".env")
    KEY_PRIVATE_PATH = cfg("KEY_PRIVATE_PATH")
    with open(KEY_PRIVATE_PATH) as f:
        return f.read()


@cache
def public_key() -> str:
    cfg = Config(".env")
    KEY_PUBLIC_PATH = cfg("KEY_PUBLIC_PATH")
    with open(KEY_PUBLIC_PATH) as f:
        return f.read()
