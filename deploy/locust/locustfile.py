import os

from locust import HttpUser, constant

from scenarios.base import ping_rps

class Litestar(HttpUser):
    """Python Litestar web-service."""

    port = os.getenv("PORT_PYTHON")
    host = f"http://localhost:{port}"
    tasks = [ping_rps]
    wait_time = constant(0)


class Gin(HttpUser):
    """Golang Gin web-service"""

    port = os.getenv("PORT_GOLANG")
    host = f"http://localhost:{port}"
    tasks = [ping_rps]
    wait_time = constant(0)
