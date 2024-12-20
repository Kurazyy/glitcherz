from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import telnyx

# Load environment variables from .env file
load_dotenv()

# Get API keys from the environment variables
TELNYX_API_KEY = os.getenv("TELNYX_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FROM_NUMBER = os.getenv("FROM_NUMBER")  # If you have the 'FROM_NUMBER' as an environment variable

# Initialize Telnyx with the API key
telnyx.api_key = TELNYX_API_KEY

app = Flask(__name__)

# Sample route for handling the webhook (replace with your actual routes)
@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    data = request.json  # Process incoming JSON data
    print(f"Received webhook: {data}")
    telegram_user_id = data.get('telegram_user_id')
    otp_code = data.get('otp_code')

    # Process the data (e.g., send a message to the Telegram user or log the call status)
    print(f"Telegram User ID: {telegram_user_id}, OTP: {otp_code}")
    return 'OK', 200  # Acknowledge the webhook request

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True)
