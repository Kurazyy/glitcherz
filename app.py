from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received Webhook:", data)
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    # For production deployment, use this instead of app.run
    app.run(host='0.0.0.0', port=5000)
