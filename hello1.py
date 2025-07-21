from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import os
import asyncio

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Конфигурация бота
TOKEN = os.getenv("TOKEN")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"

# Инициализация бота
application = Application.builder().token(TOKEN).build()

# Эндпоинт для вебхука
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

# Эндпоинт для пингов от Cron-job.org
@app.route("/ping", methods=["GET"])
def ping():
    return "Bot is alive!", 200

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я работаю на Render!")

# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))

# Установка вебхука
async def set_webhook():
    await application.bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=SECRET_TOKEN,
        drop_pending_updates=True
    )

# Запуск Flask и бота
if __name__ == "__main__":
    # На Render: запускаем Flask и устанавливаем вебхук
    from threading import Thread
    def run_flask():
        app.run(host="0.0.0.0", port=10000)
    
    def run_bot():
        loop = asyncio.new_event_loop()
        loop.run_until_complete(set_webhook())
    
    Thread(target=run_flask).start()
    Thread(target=run_bot).start()