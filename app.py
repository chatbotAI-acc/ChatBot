from flask import Flask, request, jsonify, render_template
import os
import random

app = Flask(__name__)

user_state = {}
tickets = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/tickets', methods=['GET'])
def get_tickets():
    return jsonify(tickets)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    text = req['queryResult']['intent']['displayName'].lower()

    session_id = "user1"

    if session_id not in user_state:
        if "login" in text:
            user_state[session_id] = "login"
            reply = "Sure, I can help with login issue. Please describe your problem."

        elif "network" in text or "vpn" in text:
            user_state[session_id] = "network"
            reply = "Network issue detected. Please describe your problem."

        elif "app" in text or "error" in text:
            user_state[session_id] = "application"
            reply = "Application issue detected. Please describe your problem."

        else:
            reply = "Please tell me if your issue is login, network, or application."

    else:
        issue_type = user_state[session_id]

        ticket_id = "TCKT" + str(random.randint(10000, 99999))

        tickets.append({
            "id": ticket_id,
            "type": issue_type
        })

        reply = f"""
Thank you! Your {issue_type} issue has been recorded.
Ticket ID: {ticket_id}
"""

        del user_state[session_id]

    return jsonify({"fulfillmentText": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))