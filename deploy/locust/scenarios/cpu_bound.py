"""Сценарии сетевой нагрузки."""

def encode_text(self):
    """Кодирование текста в base64."""
    self.client.get("/encode", params={"text": "Lorem ipsum dolor sit amet"})


def sum_sqrt_list(self):
    """Сумма корней элементов массива."""
    self.client.get("/sqrt_sum", params={"size": 1_000_000})
