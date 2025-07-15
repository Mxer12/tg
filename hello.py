from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import os

# Настройка логов
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")  # Берётся из переменных среды Render!
SECRET_TOKEN = os.getenv("SECRET_TOKEN")  # Добавьте в настройки Render

# Инициализация бота
application = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я работаю через вебхук.")

# Эхо-ответ
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Вебхук
async def set_webhook():
    await application.bot.delete_webhook()  # Сброс старого вебхука
    await application.bot.set_webhook(
        url=f"https://{os.getenv('RENDER_EXTERNAL_URL')}/webhook",
        secret_token=SECRET_TOKEN
    )

if __name__ == "__main__":
    # Только вебхук!
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_URL')}/webhook",
        secret_token=SECRET_TOKEN
    )
