from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import json

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast + accurate for semantic matching

# Load your recommendation data
with open('recommendations.json') as f:
    data = json.load(f)

# Create one combined string per item from keywords for embedding
texts = [" ".join(item["keywords"]) for item in data]
embeddings = model.encode(texts, convert_to_tensor=True)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.json.get("query")
    if not user_input:
        return jsonify({"response": "No input provided."}), 400

    user_embedding = model.encode(user_input, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(user_embedding, embeddings)[0]
    best_match_index = scores.argmax().item()
    best_item = data[best_match_index]

    return jsonify(best_item)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
