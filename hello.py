import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Конфигурация
TOKEN = os.getenv("TOKEN")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")  # Автоматически в Render
WEBHOOK_URL = f"https://{RENDER_HOST}/webhook"

# Проверка переменных
if not all([TOKEN, SECRET_TOKEN, RENDER_HOST]):
    raise ValueError("Missing environment variables!")

# Инициализация бота
application = Application.builder().token(TOKEN).build()

# Роут для проверки работы сервера
@app.route("/")
def home():
    return "Bot is ready!", 200

# Вебхук-роут
@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET_TOKEN:
        return "Forbidden", 403
    
    json_data = await request.get_json()
    update = Update.de_json(json_data, application.bot)
    await application.process_update(update)
    return "OK", 200

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is alive via webhook!")

application.add_handler(CommandHandler("start", start))

async def setup_webhook():
    await application.bot.delete_webhook()
    await application.bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=SECRET_TOKEN
    )
    logger.info(f"Webhook set to: {WEBHOOK_URL}")

if __name__ == "__main__":
    import asyncio
    loop = asyncio.new_event_loop()
    loop.run_until_complete(setup_webhook())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
