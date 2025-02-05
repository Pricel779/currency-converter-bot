# extensions.py

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from config import API_KEY


# Функция получения курсов валют
def get_exchange_rate(base_currency: str) -> dict:
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates']
    return None


# Команда /start
async def start(update: Update, context: CallbackContext):
    inline_keyboard = [
        [InlineKeyboardButton("Start", callback_data="start")],
        [InlineKeyboardButton("Values", callback_data="values")],
        [InlineKeyboardButton("Help", callback_data="help")]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    reply_keyboard = [
        ["Start", "Values", "Help"]
    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Я могу помочь вам конвертировать валюты. "
        "Нажмите на кнопку 'Start' для начала, 'Values' для просмотра курсов валют, "
        "или 'Help' для получения помощи.",
        reply_markup=reply_markup
    )


# Команда /values (обновленная версия, без ограничения на 10 валют)
async def values(update: Update, context: CallbackContext):
    base_currency = "USD"
    rates = get_exchange_rate(base_currency)

    if rates:
        rate_message = f"Курсы валют относительно {base_currency}:\n"
        for currency, rate in rates.items():  # Теперь показываются все валюты
            rate_message += f"{currency}: {rate:.2f}\n"
        await update.message.reply_text(rate_message)
    else:
        await update.message.reply_text("Не удалось получить курсы валют. Попробуйте позже.")


# Команда /help
async def help(update: Update, context: CallbackContext):
    help_message = (
        "Введите команду в формате: <валюта1> <валюта2> <количество>\n\n"
        "Пример: 'USD EUR 100' — переведет 100 долларов в евро.\n"
        "Если хотите увидеть все доступные валюты, нажмите 'Values'."
    )
    await update.message.reply_text(help_message)


# Обработчик нажатий инлайн-кнопок
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "start":
        await query.message.reply_text(
            "Привет! Я могу помочь вам конвертировать валюты. "
            "Нажмите на кнопку 'Start' для начала, 'Values' для просмотра курсов валют, "
            "или 'Help' для получения помощи."
        )
    elif query.data == "values":
        await values(query, context)
    elif query.data == "help":
        await help(query, context)


# Обработчик команд с клавиатуры (ReplyKeyboardMarkup)
async def keyboard_handler(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if text == "start":
        await start(update, context)
    elif text == "values":
        await values(update, context)
    elif text == "help":
        await help(update, context)
    else:
        await convert(update, context)  # Если это не команда, пробуем обработать как конвертацию


# Обработчик конвертации валют
async def convert(update: Update, context: CallbackContext):
    user_input = update.message.text.split()

    if len(user_input) != 3:
        await update.message.reply_text("Введите команду в формате: <валюта1> <валюта2> <количество>")
        return

    try:
        base_currency = user_input[0].upper()
        target_currency = user_input[1].upper()
        amount = float(user_input[2])

        rates = get_exchange_rate(base_currency)

        if rates and target_currency in rates:
            converted_amount = rates[target_currency] * amount
            await update.message.reply_text(f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
        else:
            await update.message.reply_text(f"Не удалось найти курс для {base_currency} в {target_currency}.")
    except ValueError:
        await update.message.reply_text("Ошибка! Убедитесь, что количество перевода указано числом.")
