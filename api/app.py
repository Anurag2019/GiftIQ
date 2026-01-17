from flask import Flask, request, jsonify
from flasgger import Swagger
from matcher import load_data, detect_interests, match_products
from social_extractors import extract_from_instagram, extract_from_twitter

app = Flask(__name__)
Swagger(app)


@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Gift Recommendation API
    ---
    tags:
      - Recommendation
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: payload
        required: true
        schema:
          type: object
          required:
            - source
            - value
          properties:
            source:
              type: string
              example: twitter
            value:
              type: string
              example: soumyaRNayak
    responses:
      200:
        description: Successful response
    """
    payload = request.get_json()

    source = payload.get("source")
    value = payload.get("value")

    if not source or not value:
        return jsonify({"error": "source and value are required"}), 400

    data = load_data()

    try:
        if source == "instagram":
            social = extract_from_instagram(value)
            text = social["bio"] + " " + " ".join(social["posts"])

        elif source == "twitter":
            social = extract_from_twitter(value)
            text = " ".join(social.get("posts", ""))
            if not text:
                text = value   # fallback to manual text

        elif source == "manual":
            text = value

        else:
            return jsonify({"error": "Invalid source"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    interests = detect_interests(text, data["interest_map"])
    products = match_products(interests, data["products"])

    return jsonify({
        "source": source,
        "detected_interests": interests,
        "products": products
    })


if __name__ == "__main__":
    app.run(debug=True)