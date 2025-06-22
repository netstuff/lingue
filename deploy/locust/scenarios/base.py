"""Базовые сценарии нагрузки."""

def ping_rps(self):
    """Поиск максимального RPS с простым текстовым ответом."""
    with self.client.get("/ping", catch_response=True) as response:
        if response.status_code != 200:
            response.failure(response.status_code)
