from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import os
import asyncio

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")  # Берётся из переменных среды Render!
SECRET_TOKEN = os.getenv("SECRET_TOKEN")  # Добавьте в настройки Render
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")  # URL вашего сервиса в Render

if not all([TOKEN, SECRET_TOKEN, RENDER_EXTERNAL_URL]):
    raise ValueError("Не заданы все необходимые переменные окружения!")

# Инициализация бота
application = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает через вебхук!")

# Эхо-ответ
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

async def setup_webhook():
    await application.bot.delete_webhook()  # Сброс старого вебхука
    webhook_url = f"https://{RENDER_EXTERNAL_URL}/webhook"
    logger.info(f"Устанавливаю вебхук на: {webhook_url}")
    await application.bot.set_webhook(
        url=webhook_url,
        secret_token=SECRET_TOKEN
    )

if __name__ == "__main__":
    # Установка вебхука перед запуском
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_webhook())
    
    # Запуск приложения
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"https://{RENDER_EXTERNAL_URL}/webhook",
        secret_token=SECRET_TOKEN,
        cert=None,  # В Render SSL уже настроен
        drop_pending_updates=True
    )
