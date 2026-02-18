import requests
import time
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

API_TOKEN = os.getenv("SPORTMONKS_API")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }
        requests.post(url, data=payload)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

def bot_loop():
    print("Bot iniciado com sucesso...")
    while True:
        try:
            print("Rodando verificação...")
            url = f"https://api.sportmonks.com/v3/football/livescores?api_token={API_TOKEN}"
            response = requests.get(url)
            print("API Status:", response.status_code)
        except Exception as e:
            print("Erro:", e)
        time.sleep(60)

@app.route('/')
def home():
    return "Bot rodando!"

if __name__ == "__main__":
    Thread(target=bot_loop).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
