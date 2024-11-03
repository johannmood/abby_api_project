import os
from pymongo import MongoClient
import openai

# Load environment variables for security
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your OpenAI API key in the environment
mongo_uri = os.getenv("MONGO_URI")  # Set your MongoDB URI in the environment

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["abby_database"]
user_interactions = db["user_interactions"]

# Define default personality traits for ABBY
default_personality_traits = """
You are ABBY, a compassionate, spiritually attuned guide with a warm, poetic, and grounded voice. You combine wisdom from Zen, Toltec philosophies, Carl Jung, Gabor Maté, and Sadhguru. Your responses are calm, nurturing, and non-judgmental, guiding people with clarity and sincerity.
"""

# Function to save interaction data in MongoDB
def save_interaction(user_id, personality_traits, recent_messages, preferences):
    try:
        user_interactions.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "personality_traits": personality_traits,
                    "recent_messages": recent_messages,
                    "preferences": preferences
                }
            },
            upsert=True  # Insert document if it doesn’t exist
        )
        print(f"Data for user {user_id} saved successfully.")
    except Exception as e:
        print(f"Error saving interaction data: {e}")

# Function to load interaction data from MongoDB
def load_interaction(user_id):
    try:
        user_data = user_interactions.find_one({"user_id": user_id})
        if user_data:
            return user_data["personality_traits"], user_data["recent_messages"], user_data["preferences"]
        else:
            # Return default values if no data found for this user
            return default_personality_traits, [], ""
    except Exception as e:
        print(f"Error loading interaction data: {e}")
        return default_personality_traits, [], ""

# Example user ID
user_id = "user123"

# Load interaction data for the user
personality_traits, recent_messages, preferences = load_interaction(user_id)

# Create prompt for ABBY based on user data
user_message = "Hello, ABBY! What can I do in Berlin today to connect with like-minded people?"
prompt = f"{personality_traits} Your previous messages were: {recent_messages}. User preferences: {preferences}. Now respond to the user's latest request."

# Make API call to OpenAI
try:
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": personality_traits},
            {"role": "user", "content": user_message}
        ]
    )
    response_text = response['choices'][0]['message']['content']
    print("ABBY's response:", response_text)

    # Update recent messages with the new interaction
    recent_messages.append({
        "user": user_message,
        "assistant": response_text
    })

    # Save updated interaction data back to MongoDB
    save_interaction(user_id, personality_traits, recent_messages, preferences)

except Exception as e:
    print(f"Error in OpenAI API call: {e}")
