from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import json, os

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load recommendations
with open('recommendations.json') as f:
    data = json.load(f)

texts = [" ".join(item.get("keywords", [])) for item in data]
embeddings = model.encode(texts, convert_to_tensor=True)

def get_mosque_near_zip(zip_code):
    # Replace this with real logic or API
    return f"Masjid near {zip_code}: ICNF, Jummah at 1:30 PM"

@app.route("/", methods=["GET"])
def health_check():
    return "AI backend is running", 200

@app.route('/recommend', methods=['POST'])
def recommend():
    print("📩 Received request at /recommend")
    try:
        req_data = request.json or {}
        print("📦 Received data:", req_data)

        query = req_data.get("query", "").strip().lower()
        zip_code = req_data.get("zip", "").strip()

        if not query:
            return jsonify({"error": "Missing query"}), 400

        masjid_keywords = ["jummah", "friday", "masjid", "mosque", "prayer near me"]
        is_masjid_query = any(word in query for word in masjid_keywords)

        if is_masjid_query:
            if not zip_code:
                return jsonify({"error": "ZIP code required for masjid-related queries"}), 400
            response = get_mosque_near_zip(zip_code)
        else:
            user_embedding = model.encode(query, convert_to_tensor=True)
            scores = util.pytorch_cos_sim(user_embedding, embeddings)[0]
            best_idx = scores.argmax().item()
            match = data[best_idx]
            response = match.get("response", "No relevant result found.")

        print("✅ Responding with:", response)
        return jsonify({"response": response})

    except Exception as e:
        print("❌ Error in /recommend:", str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
