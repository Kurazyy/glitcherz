from flask import Flask, request

app = Flask(__name__)

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    data = request.json
    telegram_user_id = data.get('telegram_user_id')
    otp_code = data.get('otp_code')

    # Process the data, e.g., send a message to the Telegram user or log the call status
    print(f"Received webhook for user {telegram_user_id} with OTP: {otp_code}")
    
    return 'OK', 200  # Respond with a 200 OK status

if __name__ == '__main__':
    app.run(debug=True)
