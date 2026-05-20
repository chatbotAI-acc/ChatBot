from flask import Flask, request, jsonify
import os

# 🔹 Create Flask app
app = Flask(__name__)

# 🔹 UI Route
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AssistIQ Chatbot</title>
        <style>
            body {
                font-family: Arial;
                text-align: center;
                background-color: #f5f5f5;
            }
            h1 {
                margin-top: 20px;
            }
            .chat-box {
                width: 350px;
                height: 500px;
                border: 1px solid #ccc;
                margin: auto;
                padding: 10px;
                background: white;
                overflow-y: auto;
            }
            .input-box {
                margin-top: 10px;
            }
            input {
                width: 250px;
                padding: 8px;
            }
            button {
                padding: 8px 12px;
            }
        </style>
    </head>
    <body>

        <h1>AssistIQ – AI Chatbot</h1>
        <p>Your intelligent service desk assistant</p>

        <div class="chat-box" id="chat"></div>

        <div class="input-box">
            <input type="text" id="userInput" placeholder="Type your message..." />
            <button onclick="sendMessage()">Send</button>
        </div>

        <script>
            async function sendMessage() {
                let input = document.getElementById("userInput").value;
                let chat = document.getElementById("chat");

                if (!input) return;

                chat.innerHTML += "<p><b>You:</b> " + input + "</p>";

                let response = await fetch("/webhook", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        queryResult: {
                            intent: {
                                displayName: input
                            }
                        }
                    })
                });

                let data = await response.json();

                chat.innerHTML += "<p><b>Bot:</b> " + data.fulfillmentText + "</p>";

                document.getElementById("userInput").value = "";
                chat.scrollTop = chat.scrollHeight;
            }
        </script>

    </body>
    </html>
    """

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