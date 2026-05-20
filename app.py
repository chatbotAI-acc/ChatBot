from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    intent = req['queryResult']['intent']['displayName']

    if intent == "Login Issue":
        reply = "Your login issue has been recorded. Please reset your password or wait for support."

    elif intent == "Network Issue":
        reply = "Your network issue has been noted. Please check your connection or try again later."

    elif intent == "Application Issue":
        reply = "Your application issue has been recorded. Please restart the application."

    else:
        reply = "Your request has been received."

    return jsonify({
        "fulfillmentText": reply
    })

@app.route('/')
def home():
    return "AssistIQ Chatbot is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))