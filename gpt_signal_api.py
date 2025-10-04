import os
from flask import Flask, request, jsonify
import requests
import openai

app = Flask(__name__)

# تلگرام
BOT_TOKEN = ""7990784498:AAF3n3dcRiKVNEK482qeonrnNuctFMMywdw"
CHANNEL_ID = "-1003129159524"

# GPT
openai.api_key = "Pw_k3av2oleMk5RzHCCAWVZn8arlgHNdu8jjBTRQn1kYiM97ckTXnEqAEbW0LQ4eYgh1qDHTyET3BlbkFJvCWD7I_3WyWpnmxeGpEuWGApZF4TqKbB3YHyURmm32O1LAZ0fKRadctVvJn4m0YJGLDqZXVKgA"

def send_signal_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

def generate_gpt_analysis(coin_name):
    prompt = f"Give a short crypto trading analysis for {coin_name} based on EMA9, EMA20, RSI14."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional crypto analyst."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

@app.route('/gpt-signal', methods=['POST'])
def gpt_signal():
    data = request.json
    coin = data.get('text', '').upper()

    if not coin:
        return jsonify({'status': 'error', 'message': 'No coin provided'})

    analysis = generate_gpt_analysis(coin)
    telegram_message = f"📊 GPT Analysis for *{coin}*:\n\n{analysis}"

    result = send_signal_to_telegram(telegram_message)
    return jsonify({'status': 'sent', 'result': result})
