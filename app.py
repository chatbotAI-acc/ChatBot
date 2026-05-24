from flask import Flask, request, jsonify, render_template
import os
import random
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Connection String Update with your credentials
client = MongoClient("mongodb+srv://admin:MvbFgc!39CW223_@ticketsclstr.tfudn33.mongodb.net/")
db = client["chatbot"]
tickets_collection = db["tickets"]

# Home page route for the dashboard
@app.route('/')
def home():
    return render_template("index.html")

# Get Tickets API
@app.route('/tickets', methods=['GET'])
def get_tickets():
    tickets = list(tickets_collection.find({}, {"_id": 0}))
    return jsonify(tickets)

# Update Ticket Status
@app.route('/update_ticket', methods=['POST'])
def update_ticket():
    data = request.json
    ticket_id = data['id']
    status = data['status']

    tickets_collection.update_one(
        {"id": ticket_id},
        {"$set": {"status": status}}
    )

    return jsonify({"message": "Updated"})

# Webhook (Dialogflow) to handle user queries and create tickets
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    intent = req['queryResult']['intent']['displayName']
    text = req['queryResult']['queryText'].lower()

    # Create Ticket based on Intent or Keywords
    if intent == "Escalation":
        ticket_id = "TCKT" + str(random.randint(10000, 99999))

        ticket = {
            "id": ticket_id,
            "type": text,
            "status": "Open"
        }

        tickets_collection.insert_one(ticket)

        reply = f"""
        Your issue has been escalated.

        Ticket ID: {ticket_id}
        Status: Open
        """
        return jsonify({"fulfillmentText": reply})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))