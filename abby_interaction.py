import openai
from flask import Flask, request, jsonify

# Initialize Flask application
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "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"

@app.route('/ask_abby', methods=['POST'])
def ask_abby():
    # Get the user's input from the request data
    user_input = request.json.get("user_input")

    # Check if user_input is provided
    if not user_input:
        return jsonify({"error": "user_input is required"}), 400

    # Call the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )

        # Extract the assistant's response
        assistant_message = response['choices'][0]['message']['content']

        # Return the assistant's response as JSON
        return jsonify({"assistant_response": assistant_message})

    except Exception as e:
        # Handle any errors from the OpenAI API
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000)