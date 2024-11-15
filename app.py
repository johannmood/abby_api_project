from flask import Flask, request, jsonify
import numpy as np

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
    app.run(host='0.0.0.0', port=5000)