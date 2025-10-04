
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = "7990784498:AAF3n3dcRiKVNEK482qeonrnNuctFMMywdw"
CHANNEL_ID = "-1003129159524"

def send_signal_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/gpt-signal', methods=['POST'])
def gpt_signal():
    data = request.json
    text = data.get('text', '')
    result = send_signal_to_telegram(text)
    return jsonify({'status': 'sent', 'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
