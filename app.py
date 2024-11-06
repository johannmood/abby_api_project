from flask import Flask, request, jsonify
from pymongo import MongoClient
import openai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize MongoDB and OpenAI with environment variables
client = MongoClient(os.getenv("MONGO_URI"))
db = client["abby_database"]
user_interactions = db["user_interactions"]
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load interaction function
def load_interaction(user_id):
    user_data = user_interactions.find_one({"user_id": user_id})
    if user_data:
        return user_data["personality_traits"], user_data["recent_messages"], user_data["preferences"]
    else:
        default_personality_traits = """
        You are ABBY, a compassionate, spiritually attuned guide with a warm, poetic, and grounded voice...
        """
        return default_personality_traits, [], ""

# Save interaction function
def save_interaction(user_id, personality_traits, recent_messages, preferences):
    user_interactions.update_one(
        {"user_id": user_id},
        {"$set": {
            "personality_traits": personality_traits,
            "recent_messages": recent_messages,
            "preferences": preferences
        }},
        upsert=True
    )

# Route to handle user queries at the root endpoint
@app.route("/ask_abby", methods=["POST"])
def ask_abby():
    data = request.get_json()
    user_id = data.get("user_id", "guest")
    user_message = data["message"]

    # Load interaction data
    personality_traits, recent_messages, preferences = load_interaction(user_id)

    # API call to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": personality_traits},
            {"role": "user", "content": user_message}
        ]
    )
    response_text = response['choices'][0]['message']['content']

    # Update and save interaction data
    recent_messages.append({"user": user_message, "assistant": response_text})
    save_interaction(user_id, personality_traits, recent_messages, preferences)

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)