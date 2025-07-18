from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import os
from flask_cors import CORS

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"

# Инициализация бота
application = Application.builder().token(TOKEN).build()

CORS(app, resources={
  r"/api/*": {"methods": ["GET", "POST", "PUT", "DELETE"]}
})

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        # Проверка секретного токена
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET_TOKEN:
            logger.warning("Invalid secret token")
            return "Forbidden", 403

        try:
            json_data = request.get_json()
            if not json_data:
                return "Bad Request", 400

            # Синхронная обработка
            update = Update.de_json(json_data, application.bot)
            application.update_queue.put(update)  # Добавляем update в очередь
            return "OK", 200
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return f"Error: {str(e)}", 500

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working!")

application.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    # Установка вебхука
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
        webhook_url=WEBHOOK_URL,
        secret_token=SECRET_TOKEN,
        drop_pending_updates=True
    )