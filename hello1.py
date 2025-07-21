from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import os
from flask_cors import CORS

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Конфигурация бота
TOKEN = os.getenv("TOKEN")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"

# Инициализация бота
application = Application.builder().token(TOKEN).build()

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET_TOKEN:
        logger.warning("Invalid secret token")
        return "Forbidden", 403

    try:
        update = Update.de_json(request.get_json(), application.bot)
        application.update_queue.put(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return "Internal Server Error", 500

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working!")

# Добавляем обработчик
application.add_handler(CommandHandler("start", start))

# Функция для установки вебхука (вызывается вручную или при деплое)
async def set_webhook():
    await application.bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=SECRET_TOKEN,
        drop_pending_updates=True
    )

# Запуск Flask и бота
if __name__ == "main":
    # Локально используем polling
    application.run_polling()
else:
    # На Render запускаем Flask и устанавливаем вебхук
    import asyncio
    loop = asyncio.new_event_loop()
    loop.run_until_complete(set_webhook())