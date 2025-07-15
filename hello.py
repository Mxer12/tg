from telegram import Update
from flask import Flask, request
import os
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext
)
import logging

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = "8072440393:AAHJloXf5KWoL5sZXLbcIpwmB2Da_xaEUuU"  # Замените на ваш токен!

# Инициализация бота
application = Application.builder().token(TOKEN).build()

# Обработчики команд
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Привет, {update.effective_user.first_name}! 😊")

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты написал: {update.message.text}")

# Регистрация обработчиков
application.add_handler(CommandHandler("start", start_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

# Режим Webhook (для сервера)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK", 200

def run_polling():
    """Запуск бота в режиме Long Polling (для локального тестирования)"""
    application.run_polling()

def run_webhook():
    """Запуск бота в режиме Webhook (для сервера)"""
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url="https://your-render-url.onrender.com/webhook",
        secret_token="YOUR_SECRET_TOKEN"
    )
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "webhook":
        run_webhook()
    else:
        run_polling()  # По умолчанию для локального тестирования