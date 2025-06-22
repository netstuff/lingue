from litestar import Litestar, get


@get("/ping")
async def liveness() -> str:
    return "pong"


app = Litestar([liveness])
