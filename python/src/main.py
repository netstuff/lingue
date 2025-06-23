from datetime import datetime

from litestar import Litestar, get, post
from msgspec import Struct, field


class User(Struct):
    """An user data to proceed."""

    name: str
    email: str
    created_at: datetime | None = field(default_factory=datetime.now)


@get("/ping")
async def ping() -> str:
    return "pong"


@post("/user")
async def get_user(data: User) -> User:
    return data


app = Litestar([ping, get_user])
