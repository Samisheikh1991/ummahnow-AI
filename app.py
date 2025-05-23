from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import json
import os

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load static prompts
with open('recommendations.json') as f:
    data = json.load(f)

texts = [" ".join(item.get("keywords", [])) for item in data]
embeddings = model.encode(texts, convert_to_tensor=True)

def get_mosque_near_zip(zip_code):
    # Use a real mosque locator API or placeholder here
    return f"Masjid near {zip_code}: ICNF, Jummah at 1:30 PM"

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        req_data = request.json
        print("Received data:", req_data)

        query = req_data.get("query")
        zip_code = req_data.get("zip")

        if not query or not zip_code:
            return jsonify({"error": "Missing query or zip"}), 400

        user_embedding = model.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(user_embedding, embeddings)[0]
        best_idx = scores.argmax().item()
        match = data[best_idx]

        response = match.get("response", "No result.")
        if "jummah" in query.lower() or "friday" in query.lower():
            response = get_mosque_near_zip(zip_code)

        print("Responding with:", response)
        return jsonify({"response": response})

    except Exception as e:
        print("Error in /recommend:", str(e))
        return jsonify({"error": "Internal server error"}), 500
# Don't run this block on Render
if __name__ == '__main__':
    app.run(debug=True)
