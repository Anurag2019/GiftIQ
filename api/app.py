from flask import Flask, request, jsonify
from flasgger import Swagger
from recommender import analyze_profile, generate_gift_links

app = Flask(__name__)

swagger = Swagger(app, template={
    "info": {
        "title": "GIFTIQ API",
        "description": "AI-based gift recommendation API",
        "version": "1.0.0"
    }
})


@app.route("/", methods=["GET"])
def health():
    return {"status": "ok", "service": "GIFTIQ API"}


@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Generate gift recommendations
    ---
    tags:
      - Gift Recommendation
    parameters:
      - in: body
        name: payload
        required: true
        schema:
          type: object
          required:
            - profile_text
          properties:
            profile_text:
              type: string
              example: Gym lover, coffee addict, software developer
    responses:
      200:
        description: Gift recommendations generated
      400:
        description: Invalid input
    """
    data = request.get_json()

    if not data or "profile_text" not in data:
        return jsonify({"error": "profile_text is required"}), 400

    interests = analyze_profile(data["profile_text"])
    gift_links = generate_gift_links(interests)

    return jsonify({
        "interests_detected": interests,
        "recommendations": gift_links
    })


if __name__ == "__main__":
    app.run(debug=True)