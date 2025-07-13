from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import logging

# Настройка логов (чтобы видеть ошибки)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Токен бота (замените на ваш!)
TOKEN = "8072440393:AAHJloXf5KWoL5sZXLbcIpwmB2Da_xaEUuU"

# Функция для приветствия по команде /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем имя пользователя
    user_name = update.effective_user.first_name
    # Отправляем приветствие
    await update.message.reply_text(
        f"Привет, {user_name}! 😊\n"
        "Я твой тестовый бот.\n"
        "Напиши мне что-нибудь, и я отвечу!"
    )

# Функция для ответа на обычные сообщения
async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты написал: {update.message.text}")

# Главная функция
def main():
    # Создаем приложение бота
    app = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start_command))
    
    # Регистрируем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    # Запускаем бота
    logging.info("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()