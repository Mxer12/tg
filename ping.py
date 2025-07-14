from flask import Flask, request
import threading
import time

app = Flask(__name__)

# Обязательный эндпоинт для проверки работоспособности
@app.route('/')
def home():
    return "Bot is alive!", 200

# Эндпоинт для Telegram Webhook (если используется)
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # ... ваша логика обработки сообщений ...
    return "OK", 200

    # Рекомендуемые параметры для Render
app.run(host='0.0.0.0', port=8080, debug=False)