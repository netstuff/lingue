import os

from locust import HttpUser, constant

from scenarios.base import ping_rps, user_data
from scenarios.cpu_bound import encode_text, sum_sqrt_list
from scenarios.io_bound import insert_postgres


class BaseUser(HttpUser):
    abstract = True
    tasks = [
        ping_rps,
        user_data,
        encode_text,
        sum_sqrt_list,
        insert_postgres,
    ]


class Litestar(BaseUser):
    """Python Litestar web-service."""

    port = os.getenv("PORT_PYTHON", "8000")
    host = f'http://{os.getenv("HOST_PYTHON", "localhost")}:{port}'
    wait_time = constant(0)


class Gin(BaseUser):
    """Golang Gin web-service"""

    port = os.getenv("PORT_GOLANG", "8080")
    host = f'http://{os.getenv("HOST_GOLANG", "localhost")}:{port}'
    wait_time = constant(0)
