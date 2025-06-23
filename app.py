from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

# Load the recommendations JSON from file
with open('recommendations.json') as f:
    data = json.load(f)

# Simulated mosque lookup (you can make this smarter later)
def get_mosque_near_zip(zip_code):
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

        # Check if it's a masjid-related query
        masjid_keywords = ["jummah", "friday", "masjid", "mosque"]
        is_masjid_query = any(word in query for word in masjid_keywords)

        if is_masjid_query:
            if not zip_code:
                return jsonify({"error": "ZIP code required for masjid-related queries"}), 400
            response = get_mosque_near_zip(zip_code)
        else:
            # Simple keyword scan through loaded JSON
            response = "No result."
            for item in data:
                keywords = item.get("keywords", [])
                if any(kw.lower() in query for kw in keywords):
                    response = item.get("response", "No result.")
                    break

        print("✅ Responding with:", response)
        return jsonify({"response": response})

    except Exception as e:
        print("❌ Error in /recommend:", str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
