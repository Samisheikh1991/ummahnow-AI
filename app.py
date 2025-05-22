import os
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import json

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')

with open('recommendations.json') as f:
    data = json.load(f)

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
    port = int(os.environ.get('PORT', 5000))  # Use Render's dynamic port or fallback to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
