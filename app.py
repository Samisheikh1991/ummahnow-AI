from flask import Flask, request, jsonify
import json, os, torch
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

# Load model
print("⚙️ Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load precomputed hadith data
print("🔁 Loading hadith memory...")
checkpoint = torch.load("assets/hadith_data.pt", map_location=torch.device('cpu'))
combined_hadiths = checkpoint["hadiths"]
hadith_embeddings = checkpoint["embeddings"]
print(f"✅ Loaded {len(combined_hadiths)} hadiths into memory.")

# Optional: load recommendations (for non-Hadith fallback)
try:
    with open('assets/recommendations.json') as f:
        recommendations_data = json.load(f)
except:
    recommendations_data = []

def get_masjid_near_zip(zip_code):
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

        # Masjid handling
        if any(word in query for word in ["jummah", "friday", "masjid", "mosque"]):
            if not zip_code:
                return jsonify({"error": "ZIP code required for masjid-related queries"}), 400
            return jsonify({"response": get_masjid_near_zip(zip_code)})

        # Semantic Hadith search
        query_embedding = model.encode(query, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, hadith_embeddings)[0]
        top_scores, top_indices = torch.topk(similarities, 3)

        results = []
        for score, idx in zip(top_scores, top_indices):
            if score.item() < 0.15:
                continue
            h = combined_hadiths[idx]
            results.append({
                "source": h.get("source", ""),
                "narrator": h.get("narrator", "Unknown"),
                "text": h.get("text", "No text available."),
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
