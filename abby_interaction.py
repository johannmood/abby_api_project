from pymongo import MongoClient
import openai

# Set up your OpenAI API key here
openai.api_key = "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"  # Replace with your actual OpenAI API key

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["abby_database"]
user_interactions = db["user_interactions"]

# Define default personality traits for ABBY
default_personality_traits = """
You are ABBY, a compassionate, spiritually attuned guide with a warm, poetic, and grounded voice. You combine wisdom from Zen, Toltec philosophies, Carl Jung, Gabor Maté, and Sadhguru. Your responses are calm, nurturing, and non-judgmental, guiding people with clarity and sincerity.
"""

# Function to save interaction data in MongoDB
def save_interaction(user_id, personality_traits, recent_messages, preferences):
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

# Function to load interaction data from MongoDB
def load_interaction(user_id):
    user_data = user_interactions.find_one({"user_id": user_id})
    if user_data:
        return user_data["personality_traits"], user_data["recent_messages"], user_data["preferences"]
    else:
        # Return default values if no data found for this user
        return default_personality_traits, [], ""

# Example user ID
user_id = "user123"

# Load interaction data for the user
personality_traits, recent_messages, preferences = load_interaction(user_id)

# Create prompt for ABBY based on user data
prompt = f"{personality_traits} Your previous messages were: {recent_messages}. User preferences: {preferences}. Now respond to the user's latest request."

# Make API call to OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": personality_traits},
        {"role": "user", "content": "Hello, ABBY! What can I do in Berlin today to connect with like-minded people?"}
    ]
)

# Extract the response text and print it
response_text = response['choices'][0]['message']['content']
print("ABBY's response:", response_text)

# Update recent messages with the new interaction
recent_messages.append({
    "user": "Hello, ABBY! What can I do in Berlin today to connect with like-minded people?",
    "assistant": response_text
})

# Save updated interaction data back to MongoDB
save_interaction(user_id, personality_traits, recent_messages, preferences)