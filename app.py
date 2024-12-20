from flask import Flask, request

app = Flask(__name__)

@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    # Process the incoming webhook data
    data = request.json
    print(data)
    return 'OK', 200  # Respond with a 200 status to acknowledge the webhook

if __name__ == '__main__':
    app.run(debug=True)
