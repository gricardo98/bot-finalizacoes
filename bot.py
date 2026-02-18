import requests
import time
import os

API_TOKEN = os.getenv("SPORTMONKS_API")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_live_games():
    url = f"https://api.sportmonks.com/v3/football/livescores?api_token={API_TOKEN}&include=statistics"
    response = requests.get(url)
    return response.json()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def analyze_games():
    data = get_live_games()

    if "data" not in data:
        return

    for game in data["data"]:
        minute = game["time"]["minute"]
        home_score = game["scores"]["home"]
        away_score = game["scores"]["away"]

        if minute and minute > 55:
            if home_score < away_score:
                message = f"🚨 Alerta\n{game['name']}\nMinuto: {minute}\nTime da casa atrás no placar."
                send_telegram_message(message)

while True:
    analyze_games()
    time.sleep(60)
