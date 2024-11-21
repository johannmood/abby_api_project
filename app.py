from flask import Flask, request, jsonify
import numpy as np
import base64

app = Flask(__name__)

# Helper function to decompress embeddings
def decompress_embedding(compressed_embedding):
    """
    Decode a compressed embedding from Base64 and convert to a NumPy array.
    """
    try:
        # Decode the Base64 string
        binary_data = base64.b64decode(compressed_embedding)

        # Convert the binary data into a NumPy array of floats
        return np.frombuffer(binary_data, dtype=np.float32)
    except Exception as e:
        raise ValueError(f"Error decompressing embedding: {str(e)}")

@app.route('/calculate_similarity', methods=['POST'])
def calculate_similarity():
    """
    Calculate the cosine similarity between two embeddings.
    """
    try:
        # Parse incoming JSON data
        data = request.json

        # Extract and decompress embeddings
        embedding1 = decompress_embedding(data['embedding1'])
        embedding2 = decompress_embedding(data['embedding2'])

        # Check if embeddings are valid
        if len(embedding1) == 0 or len(embedding2) == 0:
            return jsonify({'error': 'Embeddings must not be empty'}), 400

        # Calculate cosine similarity
        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

        # Convert similarity to standard Python float for JSON serialization
        return jsonify({'similarity': float(similarity)})

    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)