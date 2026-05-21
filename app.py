from flask import Flask, request, jsonify
import os
import random

app = Flask(__name__)

# 🔹 Simple memory for conversation
user_state = {}
tickets = []

# 🔹 UI Route
@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AssistIQ</title>

<style>
body {
    margin: 0;
    font-family: Arial;
    display: flex;
}

/* Sidebar */
.sidebar {
    width: 220px;
    background: #0d6efd;
    color: white;
    height: 100vh;
    padding: 20px;
}

.sidebar h2 {
    margin-bottom: 30px;
}

.sidebar div {
    margin: 15px 0;
}

/* Main Chat Area */
.main {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.header {
    padding: 15px;
    border-bottom: 1px solid #ddd;
    font-size: 20px;
    display: flex;
    justify-content: space-between;
}

.status {
    color: green;
}

/* Chat */
.chat-container {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: #f5f5f5;
}

.message {
    margin: 10px 0;
    max-width: 60%;
    padding: 12px;
    border-radius: 12px;
}

.user {
    background: #0d6efd;
    color: white;
    margin-left: auto;
}

.bot {
    background: white;
    border: 1px solid #ddd;
}

/* Input */
.input-box {
    display: flex;
    padding: 10px;
    border-top: 1px solid #ddd;
}

input {
    flex: 1;
    padding: 10px;
}

button {
    padding: 10px 15px;
    background: #0d6efd;
    color: white;
    border: none;
    cursor: pointer;
}
</style>

</head>

<body>

<!-- Sidebar -->
<div class="sidebar">
    <h2>AssistIQ</h2>
    <div onclick="newChat()">New Conversation</div>
    <div onclick="showTickets()">My Tickets</div>
    <div>Help</div>
</div>

<!-- Main -->
<div class="main">

    <div class="header">
        AssistIQ – AI Chatbot
        <span class="status">● Online</span>
    </div>

    <div id="chat" class="chat-container">
        <div class="message bot">
            Hi! I'm AssistIQ. How can I help you today?
        </div>
    </div>

    <div class="input-box">
        <input id="userInput" placeholder="Type your message..." />
        <button onclick="sendMessage()">Send</button>
    </div>

</div>

<script>
function newChat() {
    document.getElementById("chat").innerHTML =
        '<div class="message bot">Hi! I\\'m AssistIQ. How can I help you?</div>';
}

async function showTickets() {
    let chat = document.getElementById("chat");

    let response = await fetch("/tickets");
    let data = await response.json();

    chat.innerHTML = "<h3>Your Tickets:</h3>";

    if (data.length === 0) {
        chat.innerHTML += "<p>No tickets found</p>";
        return;
    }

    data.forEach(ticket => {
        chat.innerHTML += `
            <div class="message bot">
                Ticket ID: ${ticket.id} <br>
                Type: ${ticket.type}
            </div>
        `;
    });
}

async function sendMessage() {
    let input = document.getElementById("userInput").value;
    let chat = document.getElementById("chat");

    if (!input) return;

    chat.innerHTML += `<div class="message user">${input}</div>`;

    let response = await fetch("/webhook", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            queryResult: {
                intent: { displayName: input.toLowerCase() }
            }
        })
    });

    let data = await response.json();

    chat.innerHTML += `<div class="message bot">${data.fulfillmentText}</div>`;

    document.getElementById("userInput").value = "";
    chat.scrollTop = chat.scrollHeight;
}
</script>

</body>
</html>
"""
# 🔹 API Route to get tickets
@app.route('/tickets', methods=['GET'])
def get_tickets():
    return jsonify(tickets)

# 🔹 Webhook Logic (Conversation Flow)
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    text = req['queryResult']['intent']['displayName'].lower()

    session_id = "user1"

    # Step 1: Identify issue
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

    # Step 2: Create ticket
    else:
        issue_type = user_state[session_id]

        ticket_id = "TCKT" + str(random.randint(10000, 99999))

        tickets.append({
    "id": ticket_id,
    "type": issue_type
})

        reply = f"""
Thank you! Your {issue_type} issue has been recorded.
Our team will get back to you soon.
Ticket ID: {ticket_id}
"""

        del user_state[session_id]

    return jsonify({
        "fulfillmentText": reply
    })


# 🔹 Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))