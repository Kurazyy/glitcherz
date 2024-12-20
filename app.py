from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    data = request.json  # Process the incoming JSON data
    print(f"Received webhook: {data}")
    telegram_user_id = data.get('telegram_user_id')
    otp_code = data.get('otp_code')

    # Process the data (e.g., send a message to the Telegram user or log the call status)
    print(f"Telegram User ID: {telegram_user_id}, OTP: {otp_code}")
    return 'OK', 200  # Acknowledge the webhook request

if __name__ == '__main__':
    # Get the port from the environment (Render provides this dynamically)
    port = int(os.getenv('PORT', 5000))  # Default to 5000 if PORT is not set
    # Make Flask listen on all interfaces (0.0.0.0) and the dynamic port
    app.run(host='0.0.0.0', port=port, debug=True)
