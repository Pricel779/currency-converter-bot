import requests
import json
from config import API_KEY


# Класс для обработки ошибок
class APIException(Exception):
    """Класс для обработки ошибок ввода пользователя."""
    pass


# Класс для получения курса валют
class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        """Метод для получения цены валюты"""
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Количество валюты должно быть числом.")

        base = base.upper()
        quote = quote.upper()

        if base == quote:
            raise APIException("Нельзя конвертировать валюту саму в себя.")

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base}"
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException("Ошибка при получении данных от API.")

        data = json.loads(response.text)

        if "conversion_rates" not in data:
            raise APIException("Некорректный ответ от API.")

        rates = data["conversion_rates"]

        if quote not in rates:
            raise APIException(f"Валюта {quote} не найдена в списке.")

        result = rates[quote] * amount
        return round(result, 2)
