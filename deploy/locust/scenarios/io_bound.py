"""Сценарии сетевой нагрузки."""

def insert_postgres(self):
    """Создание пользователя."""
    user_data = dict(name="An user", email="user@example.com")
    self.client.post("/insert", json=user_data)
    # with self.client.post("/user", json=user_data, catch_response=True) as response:
    #     if response.status_code != 200:
    #         response.failure(response.status_code)
