from flask import Flask, request, jsonify
import numpy as np
import os

app = Flask(__name__)

@app.route('/calculate_similarity', methods=['POST'])
def calculate_similarity():
    data = request.json
    embedding1 = np.array(data['embedding1'])
    embedding2 = np.array(data['embedding2'])

    # Calculate cosine similarity
    similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return jsonify({'similarity': similarity})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's assigned port
    app.run(host='0.0.0.0', port=port)