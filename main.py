# main.py

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from extensions import start, values, help, button, keyboard_handler
from config import TOKEN, API_KEY  # Используем TOKEN вместо TELEGRAM_TOKEN

def main():
    application = Application.builder().token(TOKEN).build()  # Здесь заменили TELEGRAM_TOKEN на TOKEN

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("values", values))
    application.add_handler(CommandHandler("help", help))

    # Регистрируем обработчики инлайн-кнопок
    application.add_handler(CallbackQueryHandler(button))

    # Регистрируем обработчик сообщений с клавиатуры
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, keyboard_handler))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
