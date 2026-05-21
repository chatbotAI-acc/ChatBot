from flask import Flask, request, jsonify
import os

# 🔹 Create Flask app
app = Flask(__name__)

# 🔹 UI Route
# 🔹 Temporary memory (simple)
user_state = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    text = req['queryResult']['intent']['displayName'].lower()

    # Simulate user session (basic)
    session_id = "user1"

    # Step 1: Detect issue type
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

    # Step 2: User describes issue
    else:
        issue_type = user_state[session_id]

        import random
        ticket_id = "TCKT" + str(random.randint(10000, 99999))

        reply = f"""
        Thank you! Your {issue_type} issue has been recorded.
        Our team will get back to you soon.
        Ticket ID: {ticket_id}
        """

        # Reset state
        del user_state[session_id]

    return jsonify({
        "fulfillmentText": reply
    })

# 🔹 Webhook Route
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    intent = req['queryResult']['intent']['displayName']

    if intent == "Login Issue":
        reply = "Your login issue has been recorded. Please reset your password."

    elif intent == "Network Issue":
        reply = "Your network issue has been noted. Please check your connection."

    elif intent == "Application Issue":
        reply = "Your application issue has been recorded. Please restart the app."

    else:
        reply = "Please type: Login Issue, Network Issue, or Application Issue"

    return jsonify({
        "fulfillmentText": reply
    })

# 🔹 Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))