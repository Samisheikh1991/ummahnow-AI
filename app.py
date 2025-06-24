from flask import Flask, request, jsonify
import json, os
from sentence_transformers import SentenceTransformer, util
import torch

app = Flask(__name__)

# Load recommendations (for non-Hadith simple keyword queries)
with open('assets/bukhari.json') as f:
    bukhari = json.load(f)
    for h in bukhari:
        h['source'] = 'Bukhari'

with open('assets/muslim.json') as f:
    muslim = json.load(f)
    for h in muslim:
        h['source'] = 'Muslim'

with open('assets/recommendations.json') as f:
    data = json.load(f)
    
# Combine all hadiths and embed their English text
combined_hadiths = bukhari + muslim
hadith_texts = [h.get("english", {}).get("text", "") for h in combined_hadiths]

model = SentenceTransformer('all-MiniLM-L6-v2')
hadith_embeddings = model.encode(hadith_texts, convert_to_tensor=True)

# Simulated ZIP masjid finder
def get_mosque_near_zip(zip_code):
    return f"Masjid near {zip_code}: ICNF, Jummah at 1:30 PM"

@app.route("/", methods=["GET"])
def health_check():
    return "✅ AI backend is running", 200

@app.route("/recommend", methods=["POST"])
def recommend():
    print("📩 Received request at /recommend")
    try:
        req_data = request.json or {}
        query = req_data.get("query", "").strip().lower()
        zip_code = req_data.get("zip", "").strip()

        if not query:
            return jsonify({"error": "Missing query"}), 400

        # Check for masjid-related keywords
        masjid_keywords = ["jummah", "friday", "masjid", "mosque"]
        if any(word in query for word in masjid_keywords):
            if not zip_code:
                return jsonify({"error": "ZIP code required for masjid-related queries"}), 400
            return jsonify({"response": get_mosque_near_zip(zip_code)})

        # Perform semantic search on hadiths
        query_embedding = model.encode(query, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, hadith_embeddings)[0]
        top_scores, top_indices = torch.topk(similarities, 3)

        results = []
        for score, idx in zip(top_scores, top_indices):
            if score.item() < 0.15:
                continue
            match = combined_hadiths[idx]
            results.append({
                "source": match.get("source", ""),
                "narrator": match.get("english", {}).get("narrator", "Unknown"),
                "text": match.get("english", {}).get("text", "No text available."),
                "score": round(score.item(), 3)
            })

        if not results:
            return jsonify({"response": "No relevant Hadiths found."})

        print("✅ Responding with", results)
        return jsonify({"matches": results})

    except Exception as e:
        print("❌ Error in /recommend:", str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
