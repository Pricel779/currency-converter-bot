import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


# Команда /start и /help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    text = (
        "Добро пожаловать! Я бот для конвертации валют.\n"
        "Используйте команду в формате:\n"
        "<валюта1> <валюта2> <количество>\n\n"
        "Пример: USD RUB 100\n"
        "Чтобы узнать список доступных валют, используйте /values."
    )
    bot.reply_to(message, text)


# Команда /values
@bot.message_handler(commands=["values"])
def send_values(message):
    text = "Доступные валюты: USD, EUR, RUB и другие."
    bot.reply_to(message, text)


# Обработчик конвертации валют
@bot.message_handler(content_types=["text"])
def convert_currency(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Неправильный формат. Используйте: <валюта1> <валюта2> <количество>")

        base, quote, amount = values
        result = CurrencyConverter.get_price(base, quote, amount)
        response = f"{amount} {base.upper()} = {result} {quote.upper()}"
        bot.reply_to(message, response)

    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")

    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка: {e}")


if __name__ == "__main__":
    bot.polling(none_stop=True)
