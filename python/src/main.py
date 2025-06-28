import math
import os
from base64 import b64encode
from contextlib import asynccontextmanager
from datetime import datetime

import asyncpg
from litestar import Litestar, get, post
from litestar.datastructures import State
from msgspec import Struct, field


class DbConf(Struct):
    """Database configuration."""

    host: str = field(default=os.getenv("DB_HOST", "localhost"))
    port: int = field(default=os.getenv("DB_PORT", 5432))
    name: str = field(default=os.getenv("DB_NAME", "lingue"))
    username: str = field(default=os.getenv("DB_USER", "myuser"))
    password: str = field(default=os.getenv("DB_PASS", "mypass"))

    @property
    def dsn(self):
        return "postgresql://{0.username}:{0.password}@{0.host}:{0.port}/{0.name}".format(self)


class User(Struct):
    """An user data to proceed."""

    name: str
    email: str
    created_at: datetime | None = field(default_factory=datetime.now)


@get("/ping")
async def ping() -> str:
    """Ping-pong healthcheck."""
    return "pong"


@get("/encode")
async def base64_encode(text: str) -> bytes:
    return b64encode(text.encode("ascii"))


@get("/sqrt_sum")
async def sum_sqrt(size: int) -> float:
    result = 0.0
    for i in range(size):
        result += math.sqrt(i)
    return result


@post("/user")
async def get_user(data: User) -> User:
    """Processing JSON with current datetime."""
    return data


@post("/insert")
async def sql_insert(state: State, data: User) -> int:
    """Simple SQL query to insert."""
    id = await state.dbconn.execute(
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id",
        data.name, data.email
    )

    return id


@asynccontextmanager
async def db_connection(app: Litestar):
    """Get database connection."""
    db_conf = DbConf()
    conn = getattr(app.state, "dbconn", None)

    if conn is None:
        conn = await asyncpg.connect(db_conf.dsn)
        app.state.dbconn = conn

    print("Connected to Postgres!")

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
    			id		serial		PRIMARY KEY,
    			name	char(128)   NOT NULL,
    			email	char(128)   NOT NULL
    		)
    """)

    print("Users table has created.")

    try:
        yield
    finally:
        await conn.close()


app = Litestar(
    [ping, base64_encode, sum_sqrt, get_user, sql_insert],
    lifespan=[db_connection]
)
