from flask import Flask, request, jsonify
import numpy as np
import os

app = Flask(__name__)

@app.route('/calculate_similarity', methods=['POST'])
def calculate_similarity():
    try:
        # Parse and validate JSON payload
        data = request.json

        # Check if the keys 'embedding1' and 'embedding2' exist
        if 'embedding1' not in data or 'embedding2' not in data:
            return jsonify({'error': 'Both embedding1 and embedding2 are required'}), 400

        # Convert embeddings to numpy arrays and ensure numeric values
        try:
            embedding1 = np.array(data['embedding1'], dtype=float)
            embedding2 = np.array(data['embedding2'], dtype=float)
        except ValueError:
            return jsonify({'error': 'Embeddings must be numeric lists'}), 400

        # Validate embedding lengths
        if len(embedding1) != len(embedding2):
            return jsonify({'error': 'Embeddings must have the same length'}), 400

        # Calculate cosine similarity
        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return jsonify({'similarity': similarity})

    except Exception as e:
        # Catch unexpected errors and return as response
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({'message': 'Welcome to Abby API! Use /calculate_similarity for cosine similarity calculations.'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's assigned port
    app.run(host='0.0.0.0', port=port)