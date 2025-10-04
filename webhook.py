from flask import Flask, request
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

@app.route("/", methods=["GET"])
def home():
    return "🚀 Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = f"""
🚨 *New Signal Alert* 🚨
*Pair:* {data.get('pair')}
type = (data.get("type") or "text").upper()
*Entry:* {data.get('price')}
*SL:* {data.get('sl')}
*TP:* {data.get('tp')}
*R/R:* {data.get('rr')}
"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)
    return {"status": "ok"}, 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
