"""Базовые сценарии нагрузки."""


def ping_rps(self):
    """Поиск максимального RPS с простым текстовым ответом."""
    self.client.get("/ping")


def user_data(self):
    """Насыщение данных пользователя текущей датой."""
    user_data = dict(name="An user", email="user@example.com")
    self.client.post("/user", json=user_data)
    # with self.client.post("/user", json=user_data, catch_response=True) as response:
    #     if response.status_code != 200:
    #         response.failure(response.status_code)
