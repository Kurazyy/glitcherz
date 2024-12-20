from flask import Flask, request

app = Flask(__name__)

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    # Process the incoming webhook data
    data = request.json
    print(data)
    return 'OK', 200  # Respond with a 200 status to acknowledge the webhook

if __name__ == '__main__':
    port = os.getenv('PORT', 10000)  # Get the port from the environment or default to 10000
    app.run(host='0.0.0.0', port=port)  # Bind to all IPs and the correct port
