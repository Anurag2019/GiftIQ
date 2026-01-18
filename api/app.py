from flask import Flask, request, jsonify


from social_extractors import extract_from_instagram, extract_from_twitter
from personality_trait_analyzer import run_full_analysis

app = Flask(__name__)
# Swagger(app)


@app.route("/recommend_gifts", methods=["POST"])
def recommend():
    
    payload = request.get_json()

    source = payload.get("source")
    value = payload.get("value")

    if not source or not value:
        return jsonify({"error": "source and value are required"}), 400

    try:
        # Extract bio text based on source
        if source == "instagram":
            social = extract_from_instagram(value)
            
            # Check for extraction failure
            if not social.get("success", False):
                return jsonify({
                    "success": False,
                    "error": social.get("error", "Failed to extract Instagram data"),
                    "error_type": social.get("error_type", "unknown"),
                    "traits": [],
                    "interests": [],
                    "gifts": []
                }), 400
            
            bio_text = social["bio"] + " " + " ".join(social["posts"])

            
        elif source == "twitter":
            social = extract_from_twitter(value)
            
            # Check for extraction failure
            if not social.get("success", False):
                return jsonify({
                    "success": False,
                    "error": social.get("error", "Failed to extract Twitter data"),
                    "error_type": social.get("error_type", "twitter_error"),
                    "traits": [],
                    "interests": [],
                    "gifts": []
                }), 400
            
            bio_text = social.get("bio", "") + " " + " ".join(social.get("posts", ""))
            
        elif source == "manual":
            bio_text = value

        else:
            return jsonify({"error": "Invalid source"}), 400

        if not bio_text or not bio_text.strip():
            return jsonify({
                "success": False,
                "error": "No bio text extracted from the provided source",
                "error_type": "empty_bio",
                "traits": [],
                "interests": [],
                "gifts": []
            }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "error_type": "server_error",
            "traits": [],
            "interests": [],
            "gifts": []
        }), 500

    # Run full analysis pipeline on the bio text
    analysis_result = run_full_analysis(bio_text)

    return jsonify({
        "source": source,
        "traits": analysis_result["traits"],
        "interests": analysis_result["interests"],
        "gifts": analysis_result["gifts"]
    })


if __name__ == "__main__":
    app.run(debug=True)